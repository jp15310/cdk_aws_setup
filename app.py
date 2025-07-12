#!/usr/bin/env python3
"""Module providing function ...."""
import os
import logging
import aws_cdk as cdk
from cdk_aws_setup.cdk_aws_setup_stack import CdkAwsSetupStack

# Setup logging
logging.basicConfig(
    format='%(asctime)s [%(levelname)5s] %(message)s',
    datefmt='%Y-%m-%dT%H:%M:%S',
    level=logging.NOTSET)

app = cdk.App()
# target = "build"
env_build = cdk.Environment(
    account=os.environ['CDK_DEFAULT_ACCOUNT'],
    region=os.environ['CDK_DEFAULT_REGION'])

msg = f"app: CDK_DEFAULT_ACCOUNT: {env_build.account} - CDK_DEFAULT_REGION: {env_build.region}"
logging.info(msg)

CdkAwsSetupStack(app, "CdkAwsSetupStack", env_build)
# If you don't specify 'env', this stack will be environment-agnostic.
# Account/Region-dependent features and context lookups will not work,
# but a single synthesized template can be deployed anywhere.
# Uncomment the next line to specialize this stack for the AWS Account
# and Region that are implied by the current CLI configuration.
#env=cdk.Environment(account=os.getenv('CDK_DEFAULT_ACCOUNT'), region=os.getenv('CDK_DEFAULT_REGION')),
# Uncomment the next line if you know exactly what Account and Region you
# want to deploy the stack to. */
#env=cdk.Environment(account='123456789012', region='us-east-1'),
# For more information, see https://docs.aws.amazon.com/cdk/latest/guide/environments.html

app.synth()
