# -*- coding: utf-8 -*-
# snapshottest: v1 - https://goo.gl/zC4yUc
from __future__ import unicode_literals

from snapshottest import Snapshot


snapshots = Snapshot()

snapshots['test_snapshot 1'] = {
    'Parameters': {
        'BootstrapVersion': {
            'Default': '/cdk-bootstrap/hnb659fds/version',
            'Description': 'Version of the CDK Bootstrap resources in this environment, automatically retrieved from SSM Parameter Store. [cdk:skip]',
            'Type': 'AWS::SSM::Parameter::Value<String>'
        }
    },
    'Resources': {
        'LogRetentionaae0aa3c5b4d4f87b02d85b201efdd8aFD4BFC8A': {
            'DependsOn': [
                'LogRetentionaae0aa3c5b4d4f87b02d85b201efdd8aServiceRoleDefaultPolicyADDA7DEB',
                'LogRetentionaae0aa3c5b4d4f87b02d85b201efdd8aServiceRole9741ECFB'
            ],
            'Properties': {
                'Code': {
                    'S3Bucket': {
                        'Fn::Sub': 'cdk-hnb659fds-assets-${AWS::AccountId}-${AWS::Region}'
                    },
                    'S3Key': '6c0316fef24d0df8a9a705c77052001217d864f49af386539d01df54618cd131.zip'
                },
                'Handler': 'index.handler',
                'Role': {
                    'Fn::GetAtt': [
                        'LogRetentionaae0aa3c5b4d4f87b02d85b201efdd8aServiceRole9741ECFB',
                        'Arn'
                    ]
                },
                'Runtime': 'nodejs14.x'
            },
            'Type': 'AWS::Lambda::Function'
        },
        'LogRetentionaae0aa3c5b4d4f87b02d85b201efdd8aServiceRole9741ECFB': {
            'Properties': {
                'AssumeRolePolicyDocument': {
                    'Statement': [
                        {
                            'Action': 'sts:AssumeRole',
                            'Effect': 'Allow',
                            'Principal': {
                                'Service': 'lambda.amazonaws.com'
                            }
                        }
                    ],
                    'Version': '2012-10-17'
                },
                'ManagedPolicyArns': [
                    {
                        'Fn::Join': [
                            '',
                            [
                                'arn:',
                                {
                                    'Ref': 'AWS::Partition'
                                },
                                ':iam::aws:policy/service-role/AWSLambdaBasicExecutionRole'
                            ]
                        ]
                    }
                ]
            },
            'Type': 'AWS::IAM::Role'
        },
        'LogRetentionaae0aa3c5b4d4f87b02d85b201efdd8aServiceRoleDefaultPolicyADDA7DEB': {
            'Properties': {
                'PolicyDocument': {
                    'Statement': [
                        {
                            'Action': [
                                'logs:PutRetentionPolicy',
                                'logs:DeleteRetentionPolicy'
                            ],
                            'Effect': 'Allow',
                            'Resource': '*'
                        }
                    ],
                    'Version': '2012-10-17'
                },
                'PolicyName': 'LogRetentionaae0aa3c5b4d4f87b02d85b201efdd8aServiceRoleDefaultPolicyADDA7DEB',
                'Roles': [
                    {
                        'Ref': 'LogRetentionaae0aa3c5b4d4f87b02d85b201efdd8aServiceRole9741ECFB'
                    }
                ]
            },
            'Type': 'AWS::IAM::Policy'
        },
        'dynSaveImagesTwitterToS3cdkDD520877': {
            'DeletionPolicy': 'Delete',
            'Properties': {
                'AttributeDefinitions': [
                    {
                        'AttributeName': 'partition_key',
                        'AttributeType': 'S'
                    }
                ],
                'KeySchema': [
                    {
                        'AttributeName': 'partition_key',
                        'KeyType': 'HASH'
                    }
                ],
                'ProvisionedThroughput': {
                    'ReadCapacityUnits': 1,
                    'WriteCapacityUnits': 1
                },
                'TableName': 'dyn_SaveImagesTwitterToS3_cdk'
            },
            'Type': 'AWS::DynamoDB::Table',
            'UpdateReplacePolicy': 'Delete'
        },
        'iamSaveImagesTwitterToS3cdk2A5C9215': {
            'Properties': {
                'AssumeRolePolicyDocument': {
                    'Statement': [
                        {
                            'Action': 'sts:AssumeRole',
                            'Effect': 'Allow',
                            'Principal': {
                                'Service': 'lambda.amazonaws.com'
                            }
                        }
                    ],
                    'Version': '2012-10-17'
                },
                'Description': 'An application that periodically saves liked images to S3.',
                'ManagedPolicyArns': [
                    {
                        'Fn::Join': [
                            '',
                            [
                                'arn:',
                                {
                                    'Ref': 'AWS::Partition'
                                },
                                ':iam::aws:policy/service-role/AWSLambdaBasicExecutionRole'
                            ]
                        ]
                    }
                ],
                'RoleName': 'iam_SaveImagesTwitterToS3_cdk'
            },
            'Type': 'AWS::IAM::Role'
        },
        'iamSaveImagesTwitterToS3cdkDefaultPolicy2CAC5940': {
            'Properties': {
                'PolicyDocument': {
                    'Statement': [
                        {
                            'Action': [
                                'dynamodb:BatchGetItem',
                                'dynamodb:GetRecords',
                                'dynamodb:GetShardIterator',
                                'dynamodb:Query',
                                'dynamodb:GetItem',
                                'dynamodb:Scan',
                                'dynamodb:ConditionCheckItem',
                                'dynamodb:BatchWriteItem',
                                'dynamodb:PutItem',
                                'dynamodb:UpdateItem',
                                'dynamodb:DeleteItem'
                            ],
                            'Effect': 'Allow',
                            'Resource': [
                                {
                                    'Fn::GetAtt': [
                                        'dynSaveImagesTwitterToS3cdkDD520877',
                                        'Arn'
                                    ]
                                },
                                {
                                    'Ref': 'AWS::NoValue'
                                }
                            ]
                        },
                        {
                            'Action': [
                                's3:GetObject*',
                                's3:GetBucket*',
                                's3:List*',
                                's3:DeleteObject*',
                                's3:PutObject',
                                's3:Abort*'
                            ],
                            'Effect': 'Allow',
                            'Resource': [
                                {
                                    'Fn::GetAtt': [
                                        's3ssaveimagestwittertos3cdkB0DA6082',
                                        'Arn'
                                    ]
                                },
                                {
                                    'Fn::Join': [
                                        '',
                                        [
                                            {
                                                'Fn::GetAtt': [
                                                    's3ssaveimagestwittertos3cdkB0DA6082',
                                                    'Arn'
                                                ]
                                            },
                                            '/*'
                                        ]
                                    ]
                                }
                            ]
                        }
                    ],
                    'Version': '2012-10-17'
                },
                'PolicyName': 'iamSaveImagesTwitterToS3cdkDefaultPolicy2CAC5940',
                'Roles': [
                    {
                        'Ref': 'iamSaveImagesTwitterToS3cdk2A5C9215'
                    }
                ]
            },
            'Type': 'AWS::IAM::Policy'
        },
        'lmdSaveImagesTwitterToS3cdk7AEC5642': {
            'DependsOn': [
                'iamSaveImagesTwitterToS3cdkDefaultPolicy2CAC5940',
                'iamSaveImagesTwitterToS3cdk2A5C9215'
            ],
            'Properties': {
                'Code': {
                    'S3Bucket': {
                        'Fn::Sub': 'cdk-hnb659fds-assets-${AWS::AccountId}-${AWS::Region}'
                    },
                    'S3Key': '9c11adf9d414fd3a2ccd07f440a2c221d3a8ee38ec15e06d8ad11be240f21cd9.zip'
                },
                'Description': 'An application that periodically saves liked images to S3.',
                'Environment': {
                    'Variables': {
                        'BUCKET_NAME': {
                            'Ref': 's3ssaveimagestwittertos3cdkB0DA6082'
                        },
                        'DB_NAME': {
                            'Ref': 'dynSaveImagesTwitterToS3cdkDD520877'
                        }
                    }
                },
                'FunctionName': 'lmd_SaveImagesTwitterToS3_cdk',
                'Handler': 'lambda_function.handler',
                'MemorySize': 2048,
                'Role': {
                    'Fn::GetAtt': [
                        'iamSaveImagesTwitterToS3cdk2A5C9215',
                        'Arn'
                    ]
                },
                'Runtime': 'python3.9',
                'Timeout': 300
            },
            'Type': 'AWS::Lambda::Function'
        },
        'lmdSaveImagesTwitterToS3cdkLogRetentionD29BF9C9': {
            'Properties': {
                'LogGroupName': {
                    'Fn::Join': [
                        '',
                        [
                            '/aws/lambda/',
                            {
                                'Ref': 'lmdSaveImagesTwitterToS3cdk7AEC5642'
                            }
                        ]
                    ]
                },
                'RetentionInDays': 90,
                'ServiceToken': {
                    'Fn::GetAtt': [
                        'LogRetentionaae0aa3c5b4d4f87b02d85b201efdd8aFD4BFC8A',
                        'Arn'
                    ]
                }
            },
            'Type': 'Custom::LogRetention'
        },
        's3ssaveimagestwittertos3cdkB0DA6082': {
            'DeletionPolicy': 'Retain',
            'Properties': {
                'BucketName': 's3s-saveimagestwittertos3-cdk'
            },
            'Type': 'AWS::S3::Bucket',
            'UpdateReplacePolicy': 'Retain'
        }
    },
    'Rules': {
        'CheckBootstrapVersion': {
            'Assertions': [
                {
                    'Assert': {
                        'Fn::Not': [
                            {
                                'Fn::Contains': [
                                    [
                                        '1',
                                        '2',
                                        '3',
                                        '4',
                                        '5'
                                    ],
                                    {
                                        'Ref': 'BootstrapVersion'
                                    }
                                ]
                            }
                        ]
                    },
                    'AssertDescription': "CDK bootstrap stack version 6 required. Please run 'cdk bootstrap' with a recent version of the CDK CLI."
                }
            ]
        }
    }
}
