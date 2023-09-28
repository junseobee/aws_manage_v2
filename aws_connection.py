import boto3
import credentials.credentials as credentials
from aws_account import AwsAccount


topic_arns = {
    "avon_pci": "arn:aws:sns:us-east-1:594604260993:SNS-SNOW-CRITICAL-ECOM-PROD-ALARM",
    "avon_qde": "arn:aws:sns:us-east-1:984259802673:SNS-SNOW-CRITICAL-QDE",
    "avon_npci": "arn:aws:sns:us-east-1:151100372060:SNS-SNOW-CRITICAL-NPCI-PROD-ALARM",
    "avon_shrd": "arn:aws:sns:us-east-1:524593013124:SNS-SNOW-CRITICAL-SHRD",
    "avon_dmz": "arn:aws:sns:us-east-1:881758745010:SNS-SNOW-CRITICAL-DMZ",
    "avon_infra": "arn:aws:sns:us-east-1:651352415523:SNS-SNOW-CRITICA-INFRA",
    "avon_nonprod": "arn:aws:sns:us-east-1:295326379942:SNS-SNOW-CRITICAL-NONPROD",
    "avon_prod": "arn:aws:sns:us-east-1:496688516476:SNS-SNOW-CRITICAL-PROD"
}


# make aws console session by view-only role using mzcread user
def make_session(role):
    mzcread_sess = boto3.session.Session(profile_name="mfa")

    sts = mzcread_sess.client("sts")
    # response = switch_role(credentials."avon_qde)
    response = sts.assume_role(
        RoleArn=role['arn'],
        RoleSessionName=role['name']
    )

    return response


# switch role to access to other accounts
def switch_session(assume_role):
    switch_role_sess = boto3.Session(aws_access_key_id=assume_role['Credentials']['AccessKeyId'],
                      aws_secret_access_key=assume_role['Credentials']['SecretAccessKey'],
                      aws_session_token=assume_role['Credentials']['SessionToken'])
    
    return switch_role_sess


def account_service(account_name, service_name, region="us-east-1"):
    role = credentials.accounts[account_name]
    assume_role = make_session(role)
    switch_role_sess = switch_session(assume_role)
    aws_service = switch_role_sess.client(service_name=service_name, region_name=region)
    account_object = AwsAccount(account_name, aws_service)
    return account_object

