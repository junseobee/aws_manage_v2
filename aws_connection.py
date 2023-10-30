import boto3
from aws_account import AwsAccount


accounts = {"avon_pci"      : {"arn":"arn:aws:iam::594604260993:role/pci-admin", "name":"pci-session", "profile":"mfa"},
            "avon_qde"      : {"arn":"arn:aws:iam::984259802673:role/qde-admin", "name":"qde-session", "profile":"mfa"},
            "avon_npci"     : {"arn":"arn:aws:iam::151100372060:role/npci-admin", "name":"npci-session", "profile":"mfa"},
            "avon_shrd"     : {"arn":"arn:aws:iam::524593013124:role/shared-admin", "name":"shrd-session", "profile":"mfa"},
            "avon_dmz"      : {"arn":"arn:aws:iam::881758745010:role/network-admin", "name":"dmz-session", "profile":"mfa"},
            "avon_log"      : {"arn":"arn:aws:iam::851453209151:role/log-admin", "name":"log-session", "profile":"mfa"},
            "avon_infra"    : {"arn":"arn:aws:iam::651352415523:role/infra-admin", "name":"infra-session", "profile":"mfa"},
            "avon_nonprod"  : {"arn":"arn:aws:iam::295326379942:role/nonprod-admin", "name":"nonprod-session", "profile":"mfa"},
            "avon_prod"     : {"arn":"arn:aws:iam::496688516476:role/prod-admin", "name":"prod-session", "profile":"mfa"},
            "mzc_acct": {"arn": "arn:aws:iam::420194459472:role/admin-role", "name":"mzc-session", "profile":"my-aws"}
            }

accounts_viewoly = {
            "avon_pci"      : {"arn":"arn:aws:iam::594604260993:role/pci-viewonly", "name":"pci-session"},
            "avon_qde"      : {"arn":"arn:aws:iam::984259802673:role/qde-viewonly", "name":"qde-session"},
            "avon_npci"     : {"arn":"arn:aws:iam::151100372060:role/npci-viewonly", "name":"npci-session"},
            "avon_shrd"     : {"arn":"arn:aws:iam::524593013124:role/shared-viewonly", "name":"shrd-session"},
            "avon_dmz"      : {"arn":"arn:aws:iam::881758745010:role/network-viewonly", "name":"dmz-session"},
            "avon_log"      : {"arn":"arn:aws:iam::851453209151:role/log-viewonly", "name":"log-session"},
            "avon_infra"    : {"arn":"arn:aws:iam::651352415523:role/avon-infra-viewonly", "name":"infra-session"},
            "avon_nonprod"  : {"arn":"arn:aws:iam::295326379942:role/avon-nonprod-viewonly", "name":"nonprod-session"},
            "avon_prod"     : {"arn":"arn:aws:iam::496688516476:role/avon-prod-viewonly", "name":"prod-session"}
            }

topic_arns = {
    "avon_pci": "arn:aws:sns:us-east-1:594604260993:SNS-SNOW-CRITICAL-ECOM-PROD-ALARM",
    "avon_qde": "arn:aws:sns:us-east-1:984259802673:SNS-SNOW-CRITICAL-QDE",
    "avon_npci": "arn:aws:sns:us-east-1:151100372060:SNS-SNOW-CRITICAL-NPCI-PROD-ALARM",
    "avon_shrd": "arn:aws:sns:us-east-1:524593013124:SNS-SNOW-CRITICAL-SHRD",
    "avon_dmz": "arn:aws:sns:us-east-1:881758745010:SNS-SNOW-CRITICAL-DMZ",
    "avon_infra": "arn:aws:sns:us-east-1:651352415523:SNS-SNOW-CRITICA-INFRA",
    "avon_nonprod": "arn:aws:sns:us-east-1:295326379942:SNS-SNOW-CRITICAL-NONPROD",
    "avon_prod": "arn:aws:sns:us-east-1:496688516476:SNS-SNOW-CRITICAL-PROD",
    "mzc_acct": "arn:aws:sns:us-east-1:420194459472:SNS-ALARM"
}


# make aws console session by view-only role using mzcread user
def make_session(role):
    # Profile will be set from the accounts dic which is predefined as a profile key.
    profile_session = boto3.session.Session(profile_name=role["profile"])

    sts = profile_session.client("sts")
    # response = switch_role(credentials."avon_qde)
    response = sts.assume_role(
        RoleArn=role["arn"],
        RoleSessionName=role["name"]
    )

    return response


# switch role to access to other accounts
def switch_session(assume_role):
    switch_role_sess = boto3.Session(aws_access_key_id=assume_role['Credentials']['AccessKeyId'],
                      aws_secret_access_key=assume_role['Credentials']['SecretAccessKey'],
                      aws_session_token=assume_role['Credentials']['SessionToken'])
    
    return switch_role_sess


def account_service(account_name, service_name, region="us-east-1"):
    role = accounts[account_name]
    assume_role = make_session(role)
    switch_role_sess = switch_session(assume_role)
    aws_service = switch_role_sess.client(service_name=service_name, region_name=region)
    # don't need the object to use the client like cw, ssm, but just use the client directly
    # account_object = AwsAccount(account_name, aws_service)
    return aws_service

