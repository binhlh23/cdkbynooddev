from aws_cdk import core as cdk
import aws_cdk.aws_ec2 as ec2


AZ_1 = 'ap-southeast-1a'
AZ_2 = 'ap-southeast-1b'
AZ_3 = 'ap-southeast-1c'

InternetGW_ID = 'igw-0061752684e58a97b'
NATGW_ID = 'nat-08a35c8c298641913'

Local_ID = 'rtb-0d434878cbf4762f0'
PrivateToInternet_ID = 'rtb-0e1e1ca4c4f1c52e3'
PulicToInternet_ID = 'rtb-047b6614746ce2415'

VPC_ID = 'vpc-0d5fa16a59668d675'

VPC_CIDR = '10.0.0.0/16'

PUBLIC_ROUTE_TABLE = 'PUBLIC_RTB'
PRIVATE_ROUTE_TABLE = 'PRIVATE_RTB'

ROUTE_TABLES = {
    PUBLIC_ROUTE_TABLE,
    PRIVATE_ROUTE_TABLE
}

SUBNET_CONFIGURATION = {
    'Private_1': {
        'availability_zone': AZ_1, 'cidr_block': '10.0.1.0/24','route_table_id': PrivateToInternet_ID
    },
    'Private_2': {
        'availability_zone': AZ_1, 'cidr_block': '10.0.3.0/24','route_table_id': PrivateToInternet_ID
    },
    'Public_1': {
        'availability_zone': AZ_1, 'cidr_block': '10.0.2.0/24','route_table_id': PulicToInternet_ID
    },
    'Public_2': {
        'availability_zone': AZ_1, 'cidr_block': '10.0.4.0/24','route_table_id': PulicToInternet_ID
    },
    'Private_DB_1': {
        'availability_zone': AZ_1, 'cidr_block': '10.0.5.0/24','route_table_id': PrivateToInternet_ID
    },
    'Private_DB_2': {
        'availability_zone': AZ_2, 'cidr_block': '10.0.7.0/24','route_table_id': PrivateToInternet_ID
    }
}
