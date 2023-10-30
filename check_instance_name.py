from aws_connection import account_service


def execute_commands_on_instances(client, commands, instance_ids, platform):
    
    if platform == "Windows":
        document_name ="AWS-RunPowerShellScript"
    else:
        document_name = "AWS-RunShellScript"
    
    resp = client.send_command(
        InstanceIds = [instance_ids],
        DocumentName = document_name,
        Parameters = {'commands': [commands]}
    )
   
    return resp["Command"]["CommandId"]


def invoke_command(instance_id, command, platform, ssm_client):
    try:
        command_id = execute_commands_on_instances(ssm_client, command, instance_id, platform)

        waiter = ssm_client.get_waiter("command_executed")
        waiter.wait(
            InstanceId=instance_id,
            CommandId=command_id
        )

        output = ssm_client.get_command_invocation(
            CommandId=command_id,
            InstanceId=instance_id,
        )
        host_name = output['StandardOutputContent'].strip()
        print(f"\tretrieved {host_name} from {instance_id}".expandtabs(4))

        return host_name
    except:
        print(f"\t{instance_id} doesn't have ssm agent.".expandtabs(4))

    return "No-ssm-agent"


def get_instance_hostname(objects):
    
    # command to get host name
    command = {
        "Linux": "hostname",
        "Windows": "(Get-WmiObject Win32_Computersystem).name"
    }
    # Get instance name from the instance objects
    for object in objects:
        ssm_client = account_service(account_name=object.account, service_name="ssm")
        
        for content in object.contents:

            instance_id = content["id"]
            if content["platform"] == "Windows":
                platform = content["platform"]
            else:
                platform = "Linux"

            print("Checking...", object.account, content["name"], platform)

            content["instance_hostname"] = invoke_command(
                instance_id=instance_id, 
                command=command[platform], 
                platform=platform, 
                ssm_client=ssm_client
                )