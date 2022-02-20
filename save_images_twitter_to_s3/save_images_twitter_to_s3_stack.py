import os

import aws_cdk as cdk
from aws_cdk import (
    aws_lambda as lambda_,
    aws_logs as logs,
    aws_iam as iam,
    Stack,
)
from constructs import Construct


PROJECT_NAME = "SaveImagesTwitterToS3"
DESCRIPTION = "An application that periodically saves liked images to S3."

def build_resource_name(resource_name: str, service_name: str) -> str:
    """リソース名を組み立てる関数.

    Args:
        resource_name (str): AWSリソース名(例: lmd)
        service_name (str): サービス固有名(例: xxx_service)

    Returns:
        str: 組み立てたリソース名 (例: lmd_xxx_service_cdk)
    """
    return f"{resource_name}_{service_name}_cdk"


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

        lambda_.Function(
            self, build_resource_name("lmd", PROJECT_NAME),
            code=lambda_.Code.from_asset(os.path.join("deploy", PROJECT_NAME)),
            handler="lambda_function.handler",
            runtime=lambda_.Runtime.PYTHON_3_9,
            function_name=build_resource_name("lmd", PROJECT_NAME),
            # environment=environment,
            description=DESCRIPTION,
            timeout=cdk.Duration.seconds(300),
            memory_size=512,
            log_retention=logs.RetentionDays.THREE_MONTHS,
            role=lmd_role,
        )
