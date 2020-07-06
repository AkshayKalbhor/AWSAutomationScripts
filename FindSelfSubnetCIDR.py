import boto3
from urllib.request import urlopen
import logging
logging.basicConfig(filename='/Script/log/FindSelfSubnetCIDR.log',level=logging.INFO)

#Service reference
client = boto3.client('ec2')

#Find self instance id
instance_id = urlopen('http://169.254.169.254/latest/meta-data/instance-id').read().decode("utf-8")

logging.info("Found instance id is {}".format(instance_id))

instance = client.describe_instances(
    Filters=[
        {
            'Name': 'instance-id',
            'Values': [
                instance_id,
            ]
        }
    ]
)
logging.debug("Fetched instance details is {}".format(instance))

targetSubnetID = instance['Reservations'][0]['Instances'][0]['SubnetId']
logging.debug("Target Subnet id is {}".format(targetSubnetID))

subnet = client.describe_subnets(
    Filters=[
        {
            'Name': 'subnet-id',
            'Values': [
                targetSubnetID,
            ]
        }
    ]
)
logging.debug("Fetched Subnet details are {}".format(subnet))
cidr = subnet['Subnets'][0]['CidrBlock']
logging.info("Expected CIDR Information is {}".format(cidr))
return cidr
