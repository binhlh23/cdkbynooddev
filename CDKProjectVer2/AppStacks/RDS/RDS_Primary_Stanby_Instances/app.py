from aws_cdk import core
from stacks import rds_conf
from stacks.rds_stack import EC2RDSStack

app = core.App()
rds_construct_id = rds_conf.STACK
rds_primary = EC2RDSStack(app, rds_construct_id)
app.synth()
