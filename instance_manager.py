import boto3
import sys
import configparser

# Load AWS configurations from the .ini file
def load_config():
    config = configparser.ConfigParser()
    config.read('config.ini')

    # Check if the necessary section and keys exist in the config file
    if 'AWS' not in config:
        raise Exception('Config file missing or "AWS" section not found in config.ini')

    return {
        'aws_access_key': config['AWS']['aws_access_key'],
        'aws_secret_key': config['AWS']['aws_secret_key'],
        'region': config['AWS']['region']
    }

# List all the EC2 instances along with their details
def list_instances(aws_config):
    ec2 = boto3.resource('ec2', region_name=aws_config['region'],
                         aws_access_key_id=aws_config['aws_access_key'],
                         aws_secret_access_key=aws_config['aws_secret_key'])
    for instance in ec2.instances.all():
        print(f"ID: {instance.id}, State: {instance.state['Name']}, Type: {instance.instance_type}")

# Start the specified EC2 instance
def start_instance(instance_id, aws_config):
    ec2 = boto3.client('ec2', region_name=aws_config['region'],
                       aws_access_key_id=aws_config['aws_access_key'],
                       aws_secret_access_key=aws_config['aws_secret_key'])
    response = ec2.start_instances(InstanceIds=[instance_id])
    print(f"Starting instance: {instance_id}")

# Stop the specified EC2 instance
def stop_instance(instance_id, aws_config):
    ec2 = boto3.client('ec2', region_name=aws_config['region'],
                       aws_access_key_id=aws_config['aws_access_key'],
                       aws_secret_access_key=aws_config['aws_secret_key'])
    response = ec2.stop_instances(InstanceIds=[instance_id])
    print(f"Stopping instance: {instance_id}")

if __name__ == "__main__":
    # Load AWS configurations from the .ini file
    aws_config = load_config()

    # Check for the presence of command line arguments
    if len(sys.argv) < 2:
        print("Usage: script.py <command> [<instance_id>]")
        print("Commands: list, start, stop")
        sys.exit(1)

    command = sys.argv[1].lower()

    # Handle different commands: list, start, stop
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
