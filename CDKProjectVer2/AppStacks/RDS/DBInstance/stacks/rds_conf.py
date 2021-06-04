from aws_cdk import core as cdk
import aws_cdk.aws_rds as rds

AZ_1 = 'ap-southeast-1a'
AZ_2 = 'ap-southeast-1b'
AZ_3 = 'ap-southeast-1c'

DBInstance = {
    'allocated_storage': 100,
    'allow_major_version_upgrade': True,
    'availability_zone': AZ_1,
    'db_instance_class': 'db.t2.micro',
    'copy_tags_to_snapshot': True,
    

}
