from cloudwatch_alarm_v2 import set_cloudwatch_alarm
from client_details_v2 import get_ec2_instances, get_ec2_instance


muti_accounts = True
# accounts = [
#     "avon_pci", "avon_npci", "avon_shrd", "avon_qde", "avon_dmz",   #old landingzone
#     "avon_infra", "avon_nonprod", "avon_prod"                       #new landingzone
# ]
accounts = ["avon_pci", "avon_npci", "avon_shrd", "avon_qde", "avon_dmz"]

# CRITICAL-EC2LP-MDWDB01-DISK-i-0a177cf72eb932828-mapper/oradatavg-cacdwlv
# The alarm's threshold has been modified to 93 from 90.

single_account = "avon_pci"
# You can set an alarm or alarms in an aws account.
instance_ids = ["i-037ca96836068da8a"]


if __name__ == "__main__":
    
    if muti_accounts:
        # Update alarms for multi-accounts
        account_objects = get_ec2_instances(accounts)

        print("=" * 100)
        print("EC2 instances lists to be set alarm")
        print("=" * 100)
        for object in account_objects:
            for content in object.contents:
                print(object.account, content["id"], content["platform"])

        set_cloudwatch_alarm(account_objects)
    else:
        for instance_id in instance_ids:
            
            # Update alarms for single account
            instance = (single_account, instance_id) # tuple for account and instance id

            account_objects = get_ec2_instance(instance)
            set_cloudwatch_alarm(account_objects)
    