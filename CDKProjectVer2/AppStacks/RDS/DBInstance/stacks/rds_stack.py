
from aws_cdk import core as cdk
import aws_cdk.aws_rds as rds
from . import rds_conf

class EC2RDSStack(cdk.Stack):
    def __init__(self, scope: cdk.Construct, construct_id: str, **kwargs) -> None:
        super().__init__(scope, construct_id, **kwargs)

        self.db = rds.DatabaseInstance(self, construct_id)
