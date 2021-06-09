from aws_cdk import core
from stacks import custom_conf
from stacks.custom_stack import CustomStack

app = core.App()
construct_id = custom_conf.STACK
custom_stack = CustomStack(app, construct_id)
app.synth()
