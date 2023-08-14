import boto3
import sys
import configparser

def load_config():
    config = configparser.ConfigParser()
    config.read('config.ini')

    aws_config = {
        'aws_access_key': None,  # Default to None
        'aws_secret_key': None,
        'region': None
    }

    # Only load values from config if they exist, otherwise keep None
    if 'AWS' in config:
        aws_config['aws_access_key'] = config['AWS'].get('aws_access_key')
        aws_config['aws_secret_key'] = config['AWS'].get('aws_secret_key')
        aws_config['region'] = config['AWS'].get('region')

    return aws_config

def list_instances(aws_config):
    ec2 = boto3.resource('ec2', 
                         region_name=aws_config['region'],
                         aws_access_key_id=aws_config.get('aws_access_key'),
                         aws_secret_access_key=aws_config.get('aws_secret_key'))
    for instance in ec2.instances.all():
        print(f"ID: {instance.id}, State: {instance.state['Name']}, Type: {instance.instance_type}")

def start_instance(instance_id, aws_config):
    ec2 = boto3.client('ec2', 
                       region_name=aws_config['region'],
                       aws_access_key_id=aws_config.get('aws_access_key'),
                       aws_secret_access_key=aws_config.get('aws_secret_key'))
    response = ec2.start_instances(InstanceIds=[instance_id])
    print(f"Starting instance: {instance_id}")

def stop_instance(instance_id, aws_config):
    ec2 = boto3.client('ec2', 
                       region_name=aws_config['region'],
                       aws_access_key_id=aws_config.get('aws_access_key'),
                       aws_secret_access_key=aws_config.get('aws_secret_key'))
    response = ec2.stop_instances(InstanceIds=[instance_id])
    print(f"Stopping instance: {instance_id}")

if __name__ == "__main__":
    aws_config = load_config()

    if len(sys.argv) < 2:
        print("Usage: script.py <command> [<instance_id>]")
        print("Commands: list, start, stop")
        sys.exit(1)

    command = sys.argv[1].lower()

    if command == "list":
        list_instances(aws_config)
    elif command == "start":
        if len(sys.argv) != 3:
            print("Please provide an instance ID to start.")
            sys.exit(1)
        instance_id = sys.argv[2]
        start_instance(instance_id, aws_config)
    elif command == "stop":
        if len(sys.argv) != 3:
            print("Please provide an instance ID to stop.")
            sys.exit(1)
        instance_id = sys.argv[2]
        stop_instance(instance_id, aws_config)
    else:
        print("Unknown command. Available commands: list, start, stop")