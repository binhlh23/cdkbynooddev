from aws_cdk import core as cdk
import aws_cdk.aws_ec2 as ec2

VPC = 'HDBankVPC'

VPC_CIDR = '10.0.0.0/16'

AZ_1 = 'ap-southeast-1a'
AZ_2 = 'ap-southeast-1b'
AZ_3 = 'ap-southeast-1c'

INTERNET_GATEWAY = 'Internet GW'
NAT_GATEWAY = 'NAT GW'
EIP_NAT_GW = 'eipalloc-0f53fb48bec107a3c'

ROUTE_TABLES = {
    'Pulic_To_Internet': [{
        'destination_cidr_block': '0.0.0.0/0',
        'gateway_id': INTERNET_GATEWAY,
        'router_type': ec2.RouterType.GATEWAY
    }],
    'Private_To_Internet':[{
        'destination_cidr_block': '0.0.0.0/0',
        'nat_gateway_id': NAT_GATEWAY,
        'router_type': ec2.RouterType.NAT_GATEWAY
    }],
    'Local':[{
        'router_type': 'None'
    }]
}
