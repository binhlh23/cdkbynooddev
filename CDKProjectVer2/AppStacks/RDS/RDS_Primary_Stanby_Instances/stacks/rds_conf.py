
STACK = 'DBHDBank'

AZ_1 = 'ap-southeast-1a'
AZ_2 = 'ap-southeast-1b'
AZ_3 = 'ap-southeast-1c'

VPC_ID = 'vpc-0d5fa16a59668d675'
DBSubnet_1 = 'subnet-04f7a0b1c50f56fc2'
DBSubnet_2 = 'subnet-0513d70079a381e71'

DBPrimary_Name = 'DBHDBankPrimary'
DBStanby_Name = 'DBHDBankStanby'

DBInstance_Group = {
    DBPrimary_Name : {
        'availability_zone':AZ_1
    },
    DBStanby_Name : {
        'availability_zone':AZ_2
    }
}


