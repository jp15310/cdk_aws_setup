#!/usr/bin/env python
"""Module providing function ...."""

import logging
import aws_cdk as cdk
# from constructs import Construct
from cdk_aws_setup.cdk_aws_setup_stack import CdkAwsSetupStack


class CdkAwsSetupStage(cdk.Stage):
    def __init__(
        self, scope, construct_id, env=None, prefix=None, **kwargs
    ):
        super().__init__(scope, construct_id, env=env, **kwargs)

        # Setup logging
        logging.basicConfig(
            format='%(asctime)s [%(levelname)5s] %(message)s',
            datefmt='%Y-%m-%dT%H:%M:%S',
            level=logging.NOTSET
        )

        msg = f"CdkAwsSetupStage: CDK_DEFAULT_ACCOUNT: {env.account} - CDK_DEFAULT_REGION: {env.region} - PREFIX: {prefix}"
        logging.info(msg)

        CdkAwsSetupStack(self, 'hpsi-CdkAwsSetupStack', env, prefix)
