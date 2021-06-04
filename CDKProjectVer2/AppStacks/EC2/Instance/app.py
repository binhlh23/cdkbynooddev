#!/usr/bin/env python3

# For consistency with TypeScript code, `cdk` is the preferred import name for
# the CDK's core module.  The following line also imports it as `core` for use
# with examples from the CDK Developer's Guide, which are in the process of
# being updated to use `cdk`.  You may delete this import if you don't need it.
from aws_cdk import core
from stacks.instance_stack import EC2InstanceStack
import json

def _parse_json(path):
    file_object = open(path,"r")
    json_data = json.load(file_object)
    file_object.close()
    return json_data

app = core.App()
instance_name = _parse_json(".\\stacks\\instance_dynamic_params.json")['instance_name']
vpc = EC2InstanceStack(app, instance_name)
app.synth()
