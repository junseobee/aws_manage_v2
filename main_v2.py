from cloudwatch_alarm_v2 import set_cloudwatch_alarm
from instance_details_v2 import get_ec2_instances, get_ec2_instance
from check_instance_name import get_instance_hostname
from aws_connection import accounts
import csv


# test account and instnace_id
# avon_pci i-037ca96836068da8a"

# initiate avon's aws accounts
index = 1
account_list = dict()
for account in accounts.keys():
    if account.startswith("avon"):
        account_list[str(index)] = account
        index += 1

def save_csv(data):
    header = ["account_name", "instance_id", "instance_name", "host_name", "OS"]

    filename = "./output/instance_name.csv"

    # Write data to the CSV file
    with open(filename, 'w', newline='') as csvfile:
        writer = csv.writer(csvfile)
        
        # Write the header
        writer.writerow(header)
        
        # Write the data
        writer.writerows(data)

    print(f"Data written to {filename}")


if __name__ == "__main__":

    print("=*=*=" * 20)
    print("Which work do you want?")
    print("\t1. set alarm".expandtabs(4))
    print("\t2. get ec2 instnace tag name and host name".expandtabs(4))
    work_type = input("Enter the number: ")
    print("=" * 90)

    # when applying whole ec2 instances running only in an account or accounts,
    # you should select account that you want.
    # if you want to call a specific instance, you can select an account and an instance_id.
    print("Do you want whole instnaces in account(s)?")
    print("\t1. Yes".expandtabs(4))
    print("\t2. No. I just want to check an instance in an account.".expandtabs(4))
    scope_account = input("Enter the number: ")
    
    if scope_account == "1":
        print("Account list")
        for acct_index, acct_name in account_list.items():
            print(f"\t{acct_index}. {acct_name}".expandtabs(4))
        print("Which account(s) do you want?")
        print("\tYou can enter the number. If you want multiple accounts then you can enter the number with a space.".expandtabs(2))
        print("\ti.e. 1 3 4 for 1, 3 and 4 accounts".expandtabs(2))
        print("\tIf you get instances all account, then enter a.".expandtabs(2))
        
        selected_index = ((input("Enter the number or a: ")).strip()).split()
        #TODO: needs to verify the selected accounts whether the accounts are involved in the account_list
        if "a" in selected_index:
            selected_accounts = [v for k, v in account_list.items()]
        else:
            selected_accounts = [v for k, v in account_list.items() if k in selected_index]
    
        account_objects = get_ec2_instances(selected_accounts)

        print("=" * 90)
        print("EC2 instances lists")
        print("=" * 90)
        for object in account_objects:
            for content in object.contents:
                print(object.account, content["id"], content["platform"])
        print("=" * 90)

        if work_type == "1":
            # Update alarms for multi-accounts
            set_cloudwatch_alarm(account_objects)
        elif work_type == "2":
            get_instance_hostname(account_objects)
            instance_name_data = []
            for object in account_objects:
                for content in object.contents:
                    instance_name_data.append([object.account, content["id"], content["name"], content["instance_hostname"], content["platform"]])
                    print(object.account, content["id"], content["name"], content["instance_hostname"], content["platform"])

            save_csv(instance_name_data)
    
    else:
        print("Account list")
        for acct_index, acct_name in account_list.items():
            print(f"\t{acct_index}. {acct_name}")

        selected_index = (input("Enter the number: ")).strip()
        selected_account = account_list[selected_index]

        print("You can input more than one for instance id with comma(,)")
        selected_instance_ids = (input("Enter the instance id: ")).strip().split(",")

        for instance_id in selected_instance_ids:
            
            # Update alarms for single account
            instance = (selected_account, instance_id) # tuple for account and instance id

            account_objects = get_ec2_instance(instance)

            if work_type == "1":
                set_cloudwatch_alarm(account_objects)

            elif work_type == "2":
                get_instance_hostname(account_objects)
                for object in account_objects:
                    for content in object.contents:
                        print(object.account, content["id"], content["name"], content["instance_hostname"], content["platform"])
