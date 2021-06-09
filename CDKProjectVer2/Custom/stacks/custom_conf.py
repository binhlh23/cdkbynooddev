import aws_cdk.aws_ec2 as ec2

STACK = 'HDBank'

AZ_GROUP = {
    'AZ_1': 'ap-southeast-1a',
    'AZ_2': 'ap-southeast-1b'
}

INTERNET_GATEWAY = 'Internet GW'
NAT_GATEWAY = {
    'NATGW_1': {
        'EIP':'eipalloc-0f53fb48bec107a3c',
        'AZ': 'AZ_1',
        'public_subnet':'Public_1'
    },
}

VPC_CIDR = "10.0.0.0/16"

PUB_TO_NET = 'Pulic_To_Internet'
PRI_TO_NET = 'Private_To_Internet'
LOCAL = 'Local'

ROUTE_TABLES = {
    PUB_TO_NET: [{
        'destination_cidr_block': '0.0.0.0/0',
        'gateway_id': INTERNET_GATEWAY,
        'router_type': ec2.RouterType.GATEWAY
    }],
    PRI_TO_NET:[{
        'destination_cidr_block': '0.0.0.0/0',
        'nat_gateway_id': NAT_GATEWAY,
        'router_type': ec2.RouterType.NAT_GATEWAY
    }],
    LOCAL:[{
        'router_type': 'None'
    }]
}

SUBNET_CONFIGURATION = {
    'Private_1': {
        'availability_zone': AZ_GROUP['AZ_1'], 'cidr_block': '10.0.1.0/24','route_table_id': PRI_TO_NET
    },
    'Private_2': {
        'availability_zone': AZ_GROUP['AZ_1'], 'cidr_block': '10.0.3.0/24','route_table_id': PRI_TO_NET
    },
    'Public_1': {
        'availability_zone': AZ_GROUP['AZ_1'], 'cidr_block': '10.0.2.0/24','route_table_id': PUB_TO_NET
    },
    'Public_2': {
        'availability_zone': AZ_GROUP['AZ_2'], 'cidr_block': '10.0.4.0/24','route_table_id': PUB_TO_NET
    },
    'Private_DB_1': {
        'availability_zone': AZ_GROUP['AZ_1'], 'cidr_block': '10.0.5.0/24','route_table_id': LOCAL
    },
    'Private_DB_2': {
        'availability_zone': AZ_GROUP['AZ_2'], 'cidr_block': '10.0.7.0/24','route_table_id': LOCAL
    }
}

AMZ_LINUX = {
    'cpu_type': ec2.AmazonLinuxCpuType.X86_64,
    'edition': ec2.AmazonLinuxEdition.STANDARD,
    'generation': ec2.AmazonLinuxGeneration.AMAZON_LINUX_2,
    'storage': ec2.AmazonLinuxStorage.GENERAL_PURPOSE,
    'virtualization': ec2.AmazonLinuxVirt.HVM
}
INSTANCE_A = 'HDBank-A'
INSTANCE_B = 'HDBank-B'

INSTANCE_CONFIGURATION = {
    INSTANCE_A : {
        'subnet': 'Private_1',
        'image': AMZ_LINUX,
        'type': 't2.micro',
        'key_pair': 'key',
        'pri_ip': '10.0.1.10',
        'availability_zone': AZ_GROUP['AZ_1'],
    },
    INSTANCE_B : {
        'subnet': 'Private_2',
        'image': AMZ_LINUX,
        'type': 't2.micro',
        'key_pair': 'key',
        'pri_ip': '10.0.3.10',
        'availability_zone': AZ_GROUP['AZ_1'],
    }
}

DBPRI = 'DBPrimary'
DBSTA = 'DBStanby'

DB_CONFIGURATION = {
    DBPRI : {
        'availability_zone':AZ_GROUP['AZ_1'],
    },
    DBSTA : {
        'availability_zone':AZ_GROUP['AZ_2'],
    }
}

if __name__ == "__main__":
    count = 0
    for natgw_id, natgw_conf in NAT_GATEWAY.items():
        print(natgw_conf['EIP'])