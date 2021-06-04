
from aws_cdk import core as cdk
import aws_cdk.aws_ec2 as ec2
from . import vpc_conf

class EC2VpcStack(cdk.Stack):
    def __init__(self, scope: cdk.Construct, construct_id: str, **kwargs) -> None:
        super().__init__(scope, construct_id, **kwargs)

        self.vpc = ec2.Vpc(self, vpc_conf.VPC,
                           max_azs=2,
                           cidr=vpc_conf.VPC_CIDR,
                           subnet_configuration=[],
                           nat_gateways=0
        )
        self.IGW = self.create_internet_gateway_and_attach_to_VPC()
        self.NGW = self.create_nat_gateway_for_VPC()
        self.route_tables = self.create_route_tables()
        self.add_internet_routes_to_route_table()

        cdk.CfnOutput(self, "VPC_ID",value=self.vpc.vpc_id)
        cdk.CfnOutput(self, "Internet_GW_ID",value=self.IGW.ref)
        cdk.CfnOutput(self, "NAT_GW_ID",value=self.NGW.ref)
        for rtb_id in vpc_conf.ROUTE_TABLES:
            cdk.CfnOutput(self, rtb_id + "_ID",value=self.route_tables[rtb_id].ref)

    def create_internet_gateway_and_attach_to_VPC(self) -> ec2.CfnInternetGateway:
        internet_gateway = ec2.CfnInternetGateway(self, vpc_conf.INTERNET_GATEWAY)
        vpc_gw_attachment = ec2.CfnVPCGatewayAttachment(self,
                                    vpc_conf.INTERNET_GATEWAY + "-ATTACHMENT",
                                    vpc_id=self.vpc.vpc_id,
                                    internet_gateway_id=internet_gateway.ref
        )
#        Add this to retain resource when deleting stack
#        internet_gateway.apply_removal_policy(policy=cdk.RemovalPolicy.RETAIN)
#        vpc_gw_attachment.apply_removal_policy(policy=cdk.RemovalPolicy.RETAIN)
        return internet_gateway

    def create_nat_gateway_for_VPC(self) -> ec2.CfnNatGateway:
        nat_gateway_name = vpc_conf.NAT_GATEWAY
        subnet = ec2.CfnSubnet(self,
                               'NAT_SUBNET',
                               vpc_id=self.vpc.vpc_id,
                               cidr_block='10.0.255.0/24',
                               availability_zone=vpc_conf.AZ_1,
                               tags=[{'key': 'Name', 'value': 'NAT_SUBNET'}]
        )
        nat_gateway = ec2.CfnNatGateway(self,
                                        vpc_conf.NAT_GATEWAY,
                                        allocation_id=vpc_conf.EIP_NAT_GW,
                                        subnet_id=subnet.ref,
                                        tags=[{'key': 'Name', 'value': vpc_conf.NAT_GATEWAY}]
        )
#        Add this to retain resource when deleting stack
#        subnet.apply_removal_policy(policy=cdk.RemovalPolicy.RETAIN)
#        nat_gateway.apply_removal_policy(policy=cdk.RemovalPolicy.RETAIN)
        return nat_gateway

    def create_route_tables(self):
        route_tables = {}
        for rtb_id in vpc_conf.ROUTE_TABLES:
            route_tables[rtb_id] = ec2.CfnRouteTable(self,
                                                     rtb_id,
                                                     vpc_id=self.vpc.vpc_id,
                                                     tags=[{'key': 'Name', 'value': rtb_id}]
            )
        return route_tables
    def add_internet_routes_to_route_table(self):
        for rtb_id, routes in vpc_conf.ROUTE_TABLES.items():
            for i in range(len(routes)):
                route = routes[i]
                if route['router_type'] != 'None':
                    params = {
                        'route_table_id': self.route_tables[rtb_id].ref,
                        **route,
                    }
                    if route['router_type'] == ec2.RouterType.GATEWAY:
                        params['gateway_id'] = self.IGW.ref
                    else:
                        params['nat_gateway_id'] = self.NGW.ref
                    del params['router_type']

                    #Specifies a route in a route table within a VPC.
                    #Read more: https://docs.aws.amazon.com/cdk/api/latest/python/aws_cdk.aws_ec2/CfnRoute.html
                    ec2.CfnRoute(self, f'{rtb_id}-route-{i}', **params)
