import boto3
from tabulate import tabulate

def list_instance_types():
    ec2s = boto3.client('ec2', region_name='us-east-1')
    try: 
        response = ec2s.describe_instances()
        instances = []
        for reservation in response['Reservations']:
            for instance in reservation['Instances']:
                instances.append({
                    'InstanceId': instance['InstanceId'],
                    'State': instance['State']['Name'],
                    'InstanceType': instance['InstanceType'],
                    'vCPU': get_cpu_usage(instance['InstanceType'])
                })
        print(tabulate(instances, headers='keys',tablefmt='grid'))

    except Exception as e:
        print(f"Error retrieving instances: {e}")

def get_cpu_usage(instance_type):
    ec2s = boto3.client('ec2', region_name='us-east-1')
    try:
        type_info = ec2s.describe_instance_types(InstanceTypes=[instance_type])
        vcpus = type_info['InstanceTypes'][0]['VCpuinfo']['DefaultVCpus']
        return vcpus
    except Exception as e:
        print("Error retrieving instance type: {e}")

def main():
    list_instance_types()

if __name__ == "__main__":
    main()

#Testing