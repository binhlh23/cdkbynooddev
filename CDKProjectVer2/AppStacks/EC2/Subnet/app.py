
from aws_cdk import core
from stacks import subnet_conf
from stacks.subnet_stack import EC2VpcStack

app = core.App()
vpc = EC2VpcStack(app, 'HDBankSubnet')
app.synth()
