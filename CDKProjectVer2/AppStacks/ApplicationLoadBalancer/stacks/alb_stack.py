from aws_cdk import core as cdk
import aws_cdk.aws_ec2 as ec2
import aws_cdk.aws_elasticloadbalancingv2 as alb
from . import alb_conf

class ALBStack(cdk.Stack):
    def __init__(self, scope: cdk.Construct, construct_id: str, **kwargs) -> None:
        super().__init__(scope, construct_id, **kwargs)

        subnetid1 = ec2.Subnet.from_subnet_attributes(self,'subnetid1', availability_zone=alb_conf.AZ_1, subnet_id=alb_conf.ALBSUBNET)
        vpc_subnets_selection = ec2.SubnetSelection(subnets=[subnetid1])

        self.alb = alb.ApplicationLoadBalancer(
            self,
            construct_id,
            load_balancer_name=construct_id,
            vpc=ec2.Vpc.from_vpc_attributes(self, construct_id + 'VPC',vpc_id=alb_conf.VPC_ID, availability_zones=cdk.Fn.get_azs()),
            vpc_subnets=vpc_subnets_selection,
            internet_facing=True
        )

        targets = {}

        self.alb.connections.allow_from_any_ipv4(ec2.Port.tcp(80), "Internet access ALB.")
        #listener = self.alb.add_listener("ListenPort80", port=80, open=True)
        #listener.add_targets("AddTargetsToListener", port=80, targets=[targets])
