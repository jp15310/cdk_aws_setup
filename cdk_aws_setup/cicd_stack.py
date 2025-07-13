#!/usr/bin/env python
"""Module providing function ...."""

import logging
import aws_cdk as cdk
# import aws_cdk.aws_iam as _iam
# import aws_cdk.aws_sns as _sns
# import aws_cdk.aws_chatbot as _chatbot
# import aws_cdk.aws_codecommit as _ccommit
# import aws_cdk.aws_codestarnotifications as _notifications
from aws_cdk.pipelines import (
    CodePipeline,
    CodePipelineSource,
    ShellStep,
    # ManualApprovalStep
)
from cdk_aws_setup.cdk_aws_setup_stage import CdkAwsSetupStage


class CICDStack(cdk.Stack):
    """Module providing function ...."""

    def __init__(self, scope, construct_id, env=None, **kwargs):
        super().__init__(scope, construct_id, env=env, **kwargs)

        # Setup logging
        logging.basicConfig(format='%(asctime)s [%(levelname)5s] %(message)s',
                            datefmt='%Y-%m-%dT%H:%M:%S',
                            level=logging.NOTSET)

        msg = f"CICDStack: CDK_DEFAULT_ACCOUNT: {env.account} - CDK_DEFAULT_REGION: {env.region}"
        logging.info(msg)

        # Create reference to GitHub repository
        # pipeline_repo = _ccommit.Repository.from_repository_name(
        #     self,
        #     'cdk_aws_setup',
        #     repository_name='cdk_aws_setup'
        # )

        # Create CodePipeline and add stage to deploy network pipeline
        cicd_pipeline = CodePipeline(
            self,
            id='hpsi-network-cicd-pipeline',
            cross_account_keys=True,
            pipeline_name='hpsi-network-cicd-pipeline',
            docker_enabled_for_synth=True,
            self_mutation=True,
            synth=ShellStep(
                id='Synth',
                input=CodePipelineSource.connection(
                    'jp15310/cdk_aws_setup',
                    branch='main',
                    connection_arn='arn:aws:codeconnections:us-east-1:005713840833:connection/072c0496-0509-4e3f-822d-0b70ec5a3c8b'
                ),
                install_commands=["npm install -g aws-cdk"],
                commands=[
                    "gem install cfn-nag",
                    "make install",  # Install necessary dependencies
                    "make lint",  # Run linting checks using flake8
                    "cdk synth",  # "make synth" Generate CloudFormation template
                    "mkdir cfnnag_output",
                    "for template in $(find ./cdk.out -type f -maxdepth 2 -name '*.template.json'); do cp $template cfnnag_output; done",
                    "cfn_nag_scan --input-path cfnnag_output || true"
                ]
            )
        )

        # Dev Environment
        prefix = "hpsi-dev-"
        dev_account = self.node.try_get_context("DevAccountID")
        dev_region = self.node.try_get_context("DevRegion")
        # dev_vpc = self.node.try_get_context("DevVpcId")
        env_dev = cdk.Environment(account=dev_account, region=dev_region)
        cicd_pipeline.add_stage(
            CdkAwsSetupStage(self, "hpsi-DevStage", env_dev, prefix)
        )

        # dev_account = self.node.try_get_context("DevAccountID")
        # dev_region = self.node.try_get_context("DevRegion")
        # env_dev = cdk.Environment(account=dev_account, region=dev_region)
        # cicd_pipeline.add_stage(CdkAwsSetupStage(self, 'hpsi-DevStage', env_dev, prefix))

        # Prod Environment
        # prefix = "hpsi-prod-"
        # prod_account = self.node.try_get_context("ProdAccountID")
        # prod_region = self.node.try_get_context("ProdRegion")
        # env_prod = cdk.Environment(account=prod_account, region=prod_region)
        # cicd_pipeline.add_stage(
        #     CdkAwsSetupStage(
        #         self,
        #         'hpsi-ProdStage',
        #         env_prod, prefix),
        #     pre=[ManualApprovalStep('PromoteToProd')]
        # )

        cicd_pipeline.build_pipeline()

        # Add e-mail notifications
        # slack = _chatbot.SlackChannelConfiguration(self, 'stb-SlackChannel',
        #                                            slack_channel_configuration_name='aws_apm_elk',
        #                                            slack_workspace_id='TNJ0STUMA',
        #                                            slack_channel_id='CPVNT34G1')

        # slack.role.attach_inline_policy(_iam.Policy(self, 'stb-slack_policy',
        #                                             statements=[_iam.PolicyStatement(effect=_iam.Effect.ALLOW,
        #                                                                              actions=['chatbot:*'],
        #                                                                              resources=['*'])]))

        # topic = _sns.Topic(self, "stb-topic")

        # rule = _notifications.NotificationRule(
        #     self, 'stb-NotificationRule',
        #     source=cicd_pipeline.pipeline,
        #     detail_type=_notifications.DetailType.FULL,
        #     events=['codepipeline-pipeline-pipeline-execution-started',
        #             'codepipeline-pipeline-pipeline-execution-succeeded',
        #             'codepipeline-pipeline-pipeline-execution-failed',
        #             'codepipeline-pipeline-manual-approval-needed'],
        #     targets=[topic])

        # rule.add_target(slack)
