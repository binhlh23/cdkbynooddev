
from aws_cdk import core as cdk
import aws_cdk.aws_ec2 as ec2

from . import subnet_conf

class EC2VpcStack(cdk.Stack):
    def __init__(self, scope: cdk.Construct, construct_id: str, **kwargs) -> None:
        super().__init__(scope, construct_id, **kwargs)

        self.vpc_id = subnet_conf.VPC_ID

        self.subnets = {}
        self.create_subnets()
        self.attach_subnet_to_internet_route_table()


    def create_subnets(self):
        for subnet_id, subnet_config in subnet_conf.SUBNET_CONFIGURATION.items():
            self.subnets[subnet_id] = ec2.CfnSubnet(self,
                                                    subnet_id,
                                                    vpc_id=self.vpc_id,
                                                    cidr_block=subnet_config['cidr_block'],
                                                    availability_zone=subnet_config['availability_zone'],
                                                    tags=[{'key': 'Name', 'value': subnet_id}]
            )
#            Add this to retain resource when deleting stack
#            self.subnets[subnet_id].apply_removal_policy(policy=cdk.RemovalPolicy.RETAIN)


    def attach_subnet_to_internet_route_table(self):
        for subnet_id, subnet_config in subnet_conf.SUBNET_CONFIGURATION.items():
            rtb_id = subnet_config['route_table_id']
            subnet_rtb_association = ec2.CfnSubnetRouteTableAssociation(self,
                                                subnet_id + '-Net',
                                                subnet_id=self.subnets[subnet_id].ref,
                                                route_table_id=rtb_id
            )
#            Add this to retain resource when deleting stack
#            subnet_rtb_association.apply_removal_policy(policy=cdk.RemovalPolicy.RETAIN)
    def attach_subnet_to_local_route_table(self):
        rtb_id = subnet_conf.Local_ID
        for subnet_id, subnet_config in subnet_conf.SUBNET_CONFIGURATION.items():
            subnet_rtb_association = ec2.CfnSubnetRouteTableAssociation(self,
                                                subnet_id + '-Local',
                                                subnet_id=self.subnets[subnet_id].ref,
                                                route_table_id=rtb_id
            )
#            Add this to retain resource when deleting stack
#            subnet_rtb_association.apply_removal_policy(policy=cdk.RemovalPolicy.RETAIN)
