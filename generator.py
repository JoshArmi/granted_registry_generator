from typing import List, Tuple

import boto3


def get_instance_arn() -> str:
    ssoadmin = boto3.client("sso-admin")
    return ssoadmin.list_instances()["Instances"][0]["InstanceArn"]


def get_instance_store_id() -> str:
    ssoadmin = boto3.client("sso-admin")
    return ssoadmin.list_instances()["Instances"][0]["IdentityStoreId"]


def get_region() -> str:
    return boto3.session.Session().region_name


def get_accounts_in_organization() -> List[Tuple[str, str]]:
    organizations = boto3.client("organizations")
    paginator = organizations.get_paginator("list_accounts")

    return [
        (account["Id"], account["Name"])
        for page in paginator.paginate()
        for account in page["Accounts"]
    ]


def run() -> None:
    ssoadmin = boto3.client("sso-admin")
    paginator = ssoadmin.get_paginator("list_permission_sets_provisioned_to_account")

    instance_arn = get_instance_arn()
    instance_store_id = get_instance_store_id()
    region = get_region()

    with open("config", "w") as file:
        for account_id, account_name in get_accounts_in_organization():
            for page in paginator.paginate(
                InstanceArn=instance_arn, AccountId=account_id
            ):
                if "PermissionSets" in page:
                    for permission_set in page["PermissionSets"]:
                        sso_role_name = ssoadmin.describe_permission_set(
                            InstanceArn=instance_arn,
                            PermissionSetArn=permission_set,
                        )["PermissionSet"]["Name"]
                        profile = f"""
[profile {account_name}_{sso_role_name}]
sso_start_url  = https://{instance_store_id}.awsapps.com/start
sso_region     = {region}
sso_account_id = {account_id}
sso_role_name  = {sso_role_name}
region         = {region}
output         = json 
"""
                        file.write(profile)


if __name__ == "__main__":
    run()
