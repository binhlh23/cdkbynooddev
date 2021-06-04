from aws_cdk import core as cdk
import aws_cdk.aws_ec2 as ec2



# Must change
VPC_ID = 'vpc-0d5fa16a59668d675'
SUBNET_ID = 'subnet-0456df90955262fe4'
PRIVATE_IP = '10.0.1.11'
# Must change

#instance type free
INSTANCE_TYPE = 't2.micro'

#Key pair file's name
KEY_NAME = 'key'

#Image free
AMZ_LINUX = {
    'cpu_type': ec2.AmazonLinuxCpuType.X86_64,
    'edition': ec2.AmazonLinuxEdition.STANDARD,
    'generation': ec2.AmazonLinuxGeneration.AMAZON_LINUX_2,
    'storage': ec2.AmazonLinuxStorage.GENERAL_PURPOSE,
    'virtualization': ec2.AmazonLinuxVirt.HVM
}


SEC_GRP_PROP = {
    'vpc_id': VPC_ID,
    'group_description': 'Security group for ',
    'group_name': 'None',
    'security_group_ingress': [
        ec2.CfnSecurityGroup.IngressProperty(
            ip_protocol='TCP', cidr_ip='0.0.0.0/0', from_port=80, to_port=80
        )
    ]

}
