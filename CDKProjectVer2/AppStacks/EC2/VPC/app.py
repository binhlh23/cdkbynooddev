
from aws_cdk import core
from stacks import vpc_conf
from stacks.vpc_stack import EC2VpcStack

app = core.App()
vpc_name = vpc_conf.VPC
vpc = EC2VpcStack(app, vpc_name)
app.synth()
