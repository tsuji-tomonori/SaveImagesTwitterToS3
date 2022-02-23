import os
from pathlib import Path

import aws_cdk as cdk
from aws_cdk import (
    aws_lambda as lambda_,
    aws_logs as logs,
    aws_iam as iam,
    aws_dynamodb as dynamodb,
    aws_s3 as s3,
    aws_ssm as ssm,
    Stack,
)
from constructs import Construct
import yaml


PROJECT_NAME = "SaveImagesTwitterToS3"
DESCRIPTION = "An application that periodically saves liked images to S3."

with open(str(Path.cwd() / "lambda_env.yaml"), "r", encoding="utf-8") as f:
    LAMBDA_ENV = yaml.safe_load(f)


def build_resource_name(resource_name: str, service_name: str) -> str:
    """リソース名を組み立てる関数.

    Args:
        resource_name (str): AWSリソース名(例: lmd)
        service_name (str): サービス固有名(例: xxx_service)

    Returns:
        str: 組み立てたリソース名 (例: lmd_xxx_service_cdk)
    """
    return f"{resource_name}_{service_name}_cdk"


def build_resource_name_s3(service_name: str) -> str:
    """リソース名を組み立てる関数(S3用).
    ※ S3バケット名は「_」, 大文字が使えなかったため

    Args:
        service_name (str): サービス固有名(例: xxx_service)

    Returns:
        str: 組み立てたリソース名 (例: s3s-xxx-service-cdk)
    """
    return f"s3s-{service_name.lower()}-cdk"


class SaveImagesTwitterToS3Stack(Stack):

    def __init__(self, scope: Construct, construct_id: str, **kwargs) -> None:
        super().__init__(scope, construct_id, **kwargs)

        lmd_role = iam.Role(
            self, build_resource_name("iam", PROJECT_NAME),
            assumed_by=iam.ServicePrincipal("lambda.amazonaws.com"),
            managed_policies=[
                iam.ManagedPolicy.from_aws_managed_policy_name(
                    "service-role/AWSLambdaBasicExecutionRole")
            ],
            role_name=build_resource_name("iam", PROJECT_NAME),
            description=DESCRIPTION
        )

        lmd = lambda_.Function(
            self, build_resource_name("lmd", PROJECT_NAME),
            code=lambda_.Code.from_asset(os.path.join("deploy", PROJECT_NAME)),
            handler="lambda_function.handler",
            runtime=lambda_.Runtime.PYTHON_3_9,
            function_name=build_resource_name("lmd", PROJECT_NAME),
            environment=LAMBDA_ENV[PROJECT_NAME],
            description=DESCRIPTION,
            timeout=cdk.Duration.seconds(300),
            memory_size=2048,
            log_retention=logs.RetentionDays.THREE_MONTHS,
            role=lmd_role,
        )

        table = dynamodb.Table(
            self,
            build_resource_name("dyn", PROJECT_NAME),
            table_name=build_resource_name("dyn", PROJECT_NAME),
            billing_mode=dynamodb.BillingMode.PROVISIONED,
            read_capacity=1,
            write_capacity=1,
            removal_policy=cdk.RemovalPolicy.DESTROY,
            partition_key=dynamodb.Attribute(
                name="partition_key",
                type=dynamodb.AttributeType.STRING,
            ),
        )
        table.grant_read_write_data(lmd_role)
        lmd.add_environment(
            key="DB_NAME",
            value=table.table_name,
        )

        bucket = s3.Bucket(
            self,
            build_resource_name_s3(PROJECT_NAME),
            bucket_name=build_resource_name_s3(PROJECT_NAME)
        )
        bucket.grant_put(lmd_role)
        lmd.add_environment(
            key="BUCKET_NAME",
            value=bucket.bucket_name,
        )

        ssm_twitter_api_key = ssm.StringParameter.from_secure_string_parameter_attributes(
            self, "twitter_api_key",
            version=1,
            parameter_name="twitter_api_key",
        )
        ssm_twitter_api_key.grant_read(lmd_role)
        ssm_twitter_api_secret_key = ssm.StringParameter.from_secure_string_parameter_attributes(
            self, "twitter_api_secret_key",
            version=1,
            parameter_name="twitter_api_secret_key",
        )
        ssm_twitter_api_secret_key.grant_read(lmd_role)
        ssm_twitter_access_token = ssm.StringParameter.from_secure_string_parameter_attributes(
            self, "twitter_access_token",
            version=1,
            parameter_name="twitter_access_token",
        )
        ssm_twitter_access_token.grant_read(lmd_role)
        ssm_twitter_access_token_secret = ssm.StringParameter.from_secure_string_parameter_attributes(
            self, "twitter_access_token_secret",
            version=1,
            parameter_name="twitter_access_token_secret",
        )
        ssm_twitter_access_token_secret.grant_read(lmd_role)
