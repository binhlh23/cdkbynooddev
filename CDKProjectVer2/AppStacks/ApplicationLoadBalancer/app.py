from aws_cdk import core
from stacks import alb_conf
from stacks.alb_stack import ALBStack

app = core.App()
alb_id = alb_conf.STACK
alb = ALBStack(app, alb_id)
app.synth()
