from aws_cdk import core as cdk
import aws_cdk.aws_rds as rds
import aws_cdk.aws_ec2 as ec2
import aws_cdk.aws_elasticloadbalancingv2 as alb

import base64
from . import custom_conf

with open('.\stacks\lamp_stack.sh') as f:
    user_data = f.read()

class CustomStack(cdk.Stack):
    def __init__(self, scope: cdk.Construct, construct_id: str, **kwargs) -> None:
        super().__init__(scope, construct_id, **kwargs)

######## Create VPC
        self.vpc = ec2.Vpc(self, construct_id + "VPC",
                           max_azs=2,
                           cidr=custom_conf.VPC_CIDR,
                           subnet_configuration=[],
                           nat_gateways=0
        )

######## Call function to create Subnets
        self.subnets = self.create_subnets()

######## Create Application Load Balancer       
        subnetid1 = ec2.Subnet.from_subnet_attributes(self,'albsubnetid1', availability_zone=custom_conf.AZ_GROUP['AZ_1'], subnet_id=self.subnets['Public_1'].ref)
        subnetid2 = ec2.Subnet.from_subnet_attributes(self,'albsubnetid2', availability_zone=custom_conf.AZ_GROUP['AZ_2'], subnet_id=self.subnets['Public_2'].ref)
        vpc_subnets_selection = ec2.SubnetSelection(subnets=[subnetid1, subnetid2])

        self.alb = alb.ApplicationLoadBalancer(self, "HDBankALB",
                                          vpc=self.vpc,
                                          vpc_subnets=vpc_subnets_selection,
                                          internet_facing=True,
                                          load_balancer_name="HDBankALB"
                                          )

######## Call function to create Internet GW, Nat GW, Route tables, v.v.
        self.IGW = self.create_internet_gateway_and_attach_to_VPC()
        self.NGW = self.create_nat_gateway_for_VPC()
        self.route_tables = self.create_route_tables()
        self.add_internet_routes_to_route_table()
        self.associate_subnet_to_internet_route_table()
        self.instances = self.create_instance()
        self.db_instances = self.create_database()

######## Register ALB      
        self.alb.connections.allow_from_any_ipv4(ec2.Port.tcp(80), "Any access ALB 80")
        self.listener = self.alb.add_listener("listen_80",port=80,open=True)
        self.targets = []
        for instance_id in self.instances:
            self.targets.append(alb.InstanceTarget(instance_id=self.instances[instance_id].instance_id, port=80))
        
        self.listener.add_targets("addTargetGroup",port=80,targets=self.targets)

######## Create Internet GW and attach to VPC
    def create_internet_gateway_and_attach_to_VPC(self) -> ec2.CfnInternetGateway:
        internet_gateway = ec2.CfnInternetGateway(self, custom_conf.INTERNET_GATEWAY)
        vpc_gw_attachment = ec2.CfnVPCGatewayAttachment(self,
                                    custom_conf.INTERNET_GATEWAY + "-ATTACHMENT",
                                    vpc_id=self.vpc.vpc_id,
                                    internet_gateway_id=internet_gateway.ref
        )
        #Add this to retain resource when deleting stack
        #internet_gateway.apply_removal_policy(policy=cdk.RemovalPolicy.RETAIN)
        #vpc_gw_attachment.apply_removal_policy(policy=cdk.RemovalPolicy.RETAIN)
        return internet_gateway

######## Create NAT Subnet, NAT GW for VPC
    def create_nat_gateway_for_VPC(self) -> ec2.CfnNatGateway:    
        for natgw_id, natgw_conf in custom_conf.NAT_GATEWAY.items():
            nat_gateway = ec2.CfnNatGateway(self,
                                            natgw_id,
                                            allocation_id=natgw_conf['EIP'],
                                            subnet_id=self.subnets[natgw_conf['public_subnet']].ref,
                                            tags=[{'key': 'Name', 'value': natgw_id}]
            )
            #Add this to retain resource when deleting stack
            #nat_gateway.apply_removal_policy(policy=cdk.RemovalPolicy.RETAIN)
        return nat_gateway

######## Create Route Tables    
    def create_route_tables(self):
        route_tables = {}
        for rtb_id in custom_conf.ROUTE_TABLES:
            route_tables[rtb_id] = ec2.CfnRouteTable(self,
                                                     rtb_id,
                                                     vpc_id=self.vpc.vpc_id,
                                                     tags=[{'key': 'Name', 'value': rtb_id}]
            )
            #Add this to retain resource when deleting stack
            #route_tables[rtb_id].apply_removal_policy(policy=cdk.RemovalPolicy.RETAIN)
        return route_tables

######## Attach Internet route to corresponding Route Table
    def add_internet_routes_to_route_table(self):
        for rtb_id, routes in custom_conf.ROUTE_TABLES.items():
            for i in range(len(routes)):
                route = routes[i]
                if route['router_type'] != 'None':
                    params = {
                        'route_table_id': self.route_tables[rtb_id].ref,
                        **route,
                    }
                    if route['router_type'] == ec2.RouterType.GATEWAY:
                        params['gateway_id'] = self.IGW.ref
                    elif route['router_type'] == ec2.RouterType.NAT_GATEWAY:
                        params['nat_gateway_id'] = self.NGW.ref
                    else:
                        pass
                    del params['router_type']
                    ec2.CfnRoute(self, f'{rtb_id}-route-{i}', **params)

######## Create Subnets
    def create_subnets(self):
        subnets = {}
        for subnet_id, subnet_config in custom_conf.SUBNET_CONFIGURATION.items():
            subnets[subnet_id] = ec2.CfnSubnet(self,
                                            subnet_id,
                                            vpc_id=self.vpc.vpc_id,
                                            cidr_block=subnet_config['cidr_block'],
                                            availability_zone=subnet_config['availability_zone'],
                                            tags=[{'key': 'Name', 'value': subnet_id}]
            )
            #Add this to retain resource when deleting stack
            #self.subnets[subnet_id].apply_removal_policy(policy=cdk.RemovalPolicy.RETAIN)
        return subnets

######## Associate to route talbes
    def associate_subnet_to_internet_route_table(self):
        for subnet_id, subnet_config in custom_conf.SUBNET_CONFIGURATION.items():
            rtb_id = subnet_config['route_table_id']
            subnet_rtb_association = ec2.CfnSubnetRouteTableAssociation(self,
                                                                        subnet_id + '-Association',
                                                                        subnet_id=self.subnets[subnet_id].ref,
                                                                        route_table_id=self.route_tables[rtb_id].ref
            )

######## Create Instances
    def create_instance(self):
        instances = {}
        for instance_id, instance_conf in custom_conf.INSTANCE_CONFIGURATION.items():
            instance = ec2.Instance(self, instance_id,
                                         instance_type=ec2.InstanceType(instance_type_identifier=instance_conf['type']),
                                         instance_name=instance_id,
                                         machine_image =ec2.MachineImage.latest_amazon_linux(**instance_conf['image']),
                                         vpc=self.vpc,
                                         vpc_subnets=ec2.SubnetSelection(subnets=[ec2.Subnet.from_subnet_attributes(self,
                                                                                                                    instance_id + "-Subnet", 
                                                                                                                    availability_zone=instance_conf['availability_zone'], 
                                                                                                                    subnet_id=self.subnets[instance_conf['subnet']].ref)
                                         ]),
                                         key_name=instance_conf['key_pair'],
                                         private_ip_address=instance_conf['pri_ip'],
                                         user_data=ec2.UserData.custom(user_data),
                                         availability_zone=instance_conf['availability_zone'],
            )
            instance.connections.allow_from_any_ipv4(ec2.Port.tcp(80), "Any access 80")
            instance.connections.allow_from_any_ipv4(ec2.Port.tcp(22), "Any access SSH")
            instance.connections.allow_from(self.alb, ec2.Port.tcp(80), "ALB access 80")
            instance.connections.allow_from(self.alb, ec2.Port.tcp(22), "ALB access 22")
            instances[instance_id] = instance
            #Add this to retain resource when deleting stack
            #instances[instance_id].apply_removal_policy(policy=cdk.RemovalPolicy.RETAIN)
        return instances

######## Create RDS Instances  
    def create_database(self):
        subnetid1 = ec2.Subnet.from_subnet_attributes(self,'subnetid1', availability_zone=custom_conf.AZ_GROUP['AZ_1'], subnet_id=self.subnets['Private_DB_1'].ref)
        subnetid2 = ec2.Subnet.from_subnet_attributes(self,'subnetid2', availability_zone=custom_conf.AZ_GROUP['AZ_2'], subnet_id=self.subnets['Private_DB_2'].ref)
        vpc_subnets_selection = ec2.SubnetSelection(subnets=[subnetid1, subnetid2])
        db_instances = {}
        for db_id, db_conf in custom_conf.DB_CONFIGURATION.items():
            db_instances[db_id] = rds.DatabaseInstance(self, 
                                        db_id,
                                        instance_identifier=db_id,
                                        engine=rds.DatabaseInstanceEngine.MYSQL,
                                        database_name=db_id,
                                        instance_type=ec2.InstanceType('t2.micro'),
                                        allocated_storage=20,
                                        storage_type=rds.StorageType.GP2,
                                        backup_retention=cdk.Duration.days(7),
                                        vpc=self.vpc,
                                        availability_zone=db_conf['availability_zone'],
                                        vpc_subnets=vpc_subnets_selection
            )
            #Add this to retain resource when deleting stack
            #db_instances[db_id].apply_removal_policy(policy=cdk.RemovalPolicy.RETAIN)
        return db_instances