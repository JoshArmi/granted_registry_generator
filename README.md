# Granted Registry Generator

This repository has a Python script that automatically generates an AWS config file based on the current account assignments in AWS Identity Center (nee SSO), to be paired with Common Fate's [profile registries](https://docs.commonfate.io/granted/usage/profile-registry).

## Run

`pipenv run python generator.py`

**NB.** If you haven't previously installed the dependencies

`pipenv install`

## Minimal AWS Policy

```json
{
    "Version": "2012-10-17",
    "Statement": [
        {
            "Sid": "Organizations",
            "Effect": "Allow",
            "Action": [
                "organizations:ListAccounts"
            ],
            "Resource": "*"
        },
        {
            "Sid": "IdentityCenter",
            "Effect": "Allow",
            "Action": [
                "sso:ListPermissionSetsProvisionedToAccount",
                "sso:ListInstances",
                "sso:DescribePermissionSet"
            ],
            "Resource": "*"
        }
    ]
}
```

## Known Current Limitations

1. Uses active AWS profile region to set both SSO region and profile region.
2. Writes to a file called `config` in the present working directory.
