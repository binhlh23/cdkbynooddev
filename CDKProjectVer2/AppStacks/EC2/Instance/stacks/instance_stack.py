#Importing cdk core API
from aws_cdk import core as cdk

#Importing cdk ec2 API
import aws_cdk.aws_ec2 as ec2

from . import instance_conf

class EC2InstanceStack(cdk.Stack):

    def __init__(self, scope: cdk.Construct, construct_id: str, **kwargs) -> None:
        super().__init__(scope, construct_id, **kwargs)

#        self.vpc_id = ec2.VpcLookupOptions(vpc_name='HDBANKVPC')
        self.instance_id = construct_id
        self.subnet_id = instance_conf.SUBNET_ID
        self.amz_linux_image = ec2.MachineImage.latest_amazon_linux(**instance_conf.AMZ_LINUX)
        self.instance_type = instance_conf.INSTANCE_TYPE
        self.key_pair = instance_conf.KEY_NAME
        self.private_ip = instance_conf.PRIVATE_IP
        self.security_group_prop = instance_conf.SEC_GRP_PROP
        self.security_group = self.create_security_group()
        instance = self.create_instance()


    def create_instance(self) -> ec2.CfnInstance:
        instance = ec2.CfnInstance(self, self.instance_id,
                                         instance_type=self.instance_type,
                                         image_id=self.amz_linux_image.get_image(self).image_id,
                                         subnet_id=self.subnet_id,
                                         key_name=self.key_pair,
                                         private_ip_address=self.private_ip,
                                         security_group_ids=[self.security_group.ref],
                                         tags=[{'key': 'Name', 'value': self.instance_id}]
        )
        return instance

    def create_security_group(self) -> ec2.CfnSecurityGroup:
        sec_grp_name = self.instance_id + 'SecurityGroup'
        self.security_group_prop['group_name'] = sec_grp_name
        self.security_group_prop['group_description'] = 'Security Group for ' + self.instance_id
        security_group = ec2.CfnSecurityGroup(self,sec_grp_name,**self.security_group_prop)
        return security_group
