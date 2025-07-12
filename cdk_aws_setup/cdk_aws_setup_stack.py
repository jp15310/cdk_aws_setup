#!/usr/bin/env python
"""Module providing function ...."""

import logging
# import cdk_nag
import aws_cdk as cdk
import aws_cdk.aws_ec2 as _ec2
# from constructs import Construct


class CdkAwsSetupStack(cdk.Stack):
    """Class representing the data pipeline definition for CPKC Networking on AWS"""

    def __init__(self, scope, construct_id, env=None, prefix=None, **kwargs):
        super().__init__(scope, construct_id, env=env, **kwargs)

        # Setup logging
        logging.basicConfig(
            format='%(asctime)s [%(levelname)5s] %(message)s',
            datefmt='%Y-%m-%dT%H:%M:%S',
            level=logging.NOTSET)

        msg = f"CdkAwsSetupStack: CDK_DEFAULT_ACCOUNT: {env.account} - CDK_DEFAULT_REGION: {env.region} - PREFIX: {prefix}"
        logging.info(msg)

        # TODO - Implement Aspect to Supress the CDK Nag warnings
        # cdk.Aspects.of(self).add(cdk_nag.AwsSolutionsChecks())

        #
        # Creaye KMS key to encrypt secrets for CDK Deployment - Enable if need to use secret inside CDK
        #
        # MyCdkKey = _kms.Key(self, "KmsKeyCdk")

        #
        # Create VPC
        #

        prefix = 'hpsi-'
        cidr = '10.0.0.0/16'

        vpc = _ec2.Vpc(
            self,
            'Vpc',
            nat_gateways=1,
            ip_addresses=_ec2.IpAddresses.cidr(cidr),
            gateway_endpoints={
                "s3": _ec2.GatewayVpcEndpointOptions(
                    service=_ec2.GatewayVpcEndpointAwsService.S3
                )
            },
            vpc_name=prefix+"hpsi"
        )
        # cdk.Tags.of(vpc).add('name', 'stb-cpkc')

        # Set up Flow Log for VPC
        vpc.add_flow_log(prefix+'FlowLog', traffic_type=_ec2.FlowLogTrafficType.REJECT)

        # Create CPKC security group for all CPKC services
        ckpc_sg = _ec2.SecurityGroup(
            self,
            prefix+"HpsiSG",
            vpc=vpc,
            description="Allow HPSi Applications Access to VPC Services",
            allow_all_outbound=True,
            disable_inline_rules=True,
            security_group_name=prefix+"hpsisg"
        )

        # Add Ingress Rules for CPKC SG
        ckpc_sg.add_ingress_rule(
                peer=_ec2.Peer.ipv4(vpc.vpc_cidr_block),
                connection=_ec2.Port.tcp(5432),
                description="Allow Access to RDS"
            )

        ckpc_sg.add_ingress_rule(
                peer=_ec2.Peer.any_ipv4(),
                connection=_ec2.Port.tcp(80),
                description="Allow HTTP access from Internet"
            )

        ckpc_sg.add_ingress_rule(
                peer=_ec2.Peer.any_ipv4(),
                connection=_ec2.Port.tcp(22),
                description="Allow SSH access from Internet"
            )

        ckpc_sg.add_ingress_rule(
                peer=_ec2.Peer.security_group_id(ckpc_sg.security_group_id),
                connection=_ec2.Port.all_tcp(),
                description="Self-referencing inbound rule for Glue Connection"
            )

        # Add interface endpoint for secrets manager, Glue, and RDS
        vpc.add_interface_endpoint(
            prefix+'SecretsManagerEndpoint',
            service=_ec2.InterfaceVpcEndpointAwsService.SECRETS_MANAGER
        )

        # Add interface endpoint for glue jobs
        vpc.add_interface_endpoint(
            prefix+'GlueEndpoint',
            service=_ec2.InterfaceVpcEndpointAwsService.GLUE
        )

        # Add interface endpoint for glue jobs
        # vpc.add_interface_endpoint(prefix+'RdsEndpoint',
        #                                 service = _ec2.InterfaceVpcEndpointAwsService.RDS
        #                             )

        # Display VPC Outputs
        cdk.CfnOutput(self, prefix+'VPC', value=vpc.vpc_id)
        cdk.CfnOutput(self, prefix+'Default SG', value=ckpc_sg.security_group_vpc_id)
        cdk.CfnOutput(self, prefix+'Main SG', value=ckpc_sg.security_group_id)

        #
        # Supress the CDK Nag warnings for VPC
        #

        # NagSuppressions.add_resource_suppressions_by_path(self,
        #         '/RootStack/NetworkStack/CpkcVpc/SecretsManagerEndpoint/SecurityGroup/Resource',[
        #         {"id": 'CdkNagValidationFailure', "reason": 'Security Manager security group needs no explicit port range set', },
        #    ]
        # )

        # NagSuppressions.add_resource_suppressions_by_path(self,
        #         '/RootStack/NetworkStack/security_group_db/Resource',[
        #         {"id": 'CdkNagValidationFailure', "reason": 'Security Manager security group needs no explicit port range set', },
        #    ]
        # )

        #
        # EC2 Bastion for PostgresDB Client
        #
        web_server = _ec2.Instance(
            self,
            prefix+'PostgresClient',
            instance_name=prefix+"CPKC_Bastion",
            machine_image=_ec2.MachineImage.latest_amazon_linux2(),
            instance_type=_ec2.InstanceType.of(
                instance_class=_ec2.InstanceClass.T3,
                instance_size=_ec2.InstanceSize.MICRO
            ),
            vpc=vpc,
            vpc_subnets=_ec2.SubnetSelection(subnet_type=_ec2.SubnetType.PUBLIC),
            user_data_causes_replacement=True,
            security_group=ckpc_sg
        )

        # Attaching an Elastic IP to keep the DNS name on updates
        _ec2.CfnEIP(self, prefix+'ElasticIP', instance_id=web_server.instance_id)

        # Installing packages (nginx & Postgres client) at instance launch
        web_server.add_user_data('sudo yum update -y',
                                 'sudo amazon-linux-extras install postgresql13 -y')

        cdk.CfnOutput(self, prefix+'PostgresClientDnsName', value=web_server.instance_public_dns_name)
        cdk.CfnOutput(self, prefix+'EC2Name', value=web_server.instance_id)

        # EC2 Tagging constructs
        # cdk.Tags.of(web_server).add('category', 'web server')
        # cdk.Tags.of(web_server).add('subcategory', 'primary', include_resource_types=['AWS::EC2::Instance'])
