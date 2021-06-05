from aws_cdk import core as cdk
import aws_cdk.aws_rds as rds
import aws_cdk.aws_ec2 as ec2
from . import rds_conf

class EC2RDSStack(cdk.Stack):
    def __init__(self, scope: cdk.Construct, construct_id: str, **kwargs) -> None:
        super().__init__(scope, construct_id, **kwargs)

        subnetid1 = ec2.Subnet.from_subnet_attributes(self,'subnetid1', availability_zone=rds_conf.AZ_1, subnet_id=rds_conf.DBSubnet_1)
        subnetid2 = ec2.Subnet.from_subnet_attributes(self,'subnetid2', availability_zone=rds_conf.AZ_2, subnet_id=rds_conf.DBSubnet_2)
        vpc_subnets_selection = ec2.SubnetSelection(subnets=[subnetid1, subnetid2])
        db_group = rds_conf.DBInstance_Group
        self.db_instances = {}
        for db_id in db_group:
            self.db_instances[db_id] = rds.DatabaseInstance(self, 
                                        db_id,
                                        instance_identifier=db_id,
                                        engine=rds.DatabaseInstanceEngine.MYSQL,
                                        database_name=db_id,
                                        instance_type=ec2.InstanceType('t2.micro'),
                                        allocated_storage=20,
                                        storage_type=rds.StorageType.GP2,
                                        backup_retention=cdk.Duration.days(7),
                                        vpc=ec2.Vpc.from_vpc_attributes(self, "VPC",vpc_id=rds_conf.VPC_ID, availability_zones=cdk.Fn.get_azs()),
                                        availability_zone=db_id['availability_zone'],
                                        vpc_subnets=vpc_subnets_selection
            )