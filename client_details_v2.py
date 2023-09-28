from aws_connection import  account_service


def get_ec2_desc(instance):
    
    if instance["State"]["Name"] == "running":
        instance_id = instance["InstanceId"]
        image_id = instance["ImageId"]
        instance_type = instance["InstanceType"]
        platform = instance["PlatformDetails"]
        
        try:
            for tag in instance["Tags"]:
                if tag["Key"] == "Name":
                    instance_name = tag["Value"]
                    # print(instance_id, instance_name, platform)
                    return {
                        "id": instance_id, 
                        "name": instance_name, 
                        "image_id": image_id,
                        "instance_type": instance_type,
                        "platform": platform
                        }
        except:
            pass
            # print(f"{account.account}'s {instance_id} don't have name tag.")    
    return False


# gather ec2 instances which are running state.
def get_ec2_instances(accounts):
    account_objs = []
    for account in accounts:
        account_obj = account_service(account_name=account, service_name="ec2")
        paginator = account_obj.service.get_paginator("describe_instances")
        response_iterator = paginator.paginate()

        instance_contents = []
        for instances in response_iterator:
            for instance in instances["Reservations"]:
                instance_details = instance["Instances"][0]

                result = get_ec2_desc(instance_details)

                if result:
                    account_obj.contents = result
                    instance_contents.append(result)
                    
            account_obj.contents = instance_contents
        account_objs.append(account_obj)

    return account_objs


def get_ec2_instance(instance):
    account_name = instance[0]
    instance_id = instance[1]
    instance = [instance_id,]
    result = None
    account_obj = account_service(account_name, "ec2")
    instance_details = account_obj.service.describe_instances(InstanceIds=instance)["Reservations"][0]["Instances"][0]

    result = get_ec2_desc(instance_details)
    account_obj.contents = [result]

    return [account_obj]

