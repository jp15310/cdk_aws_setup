import aws_cdk as core
import aws_cdk.assertions as assertions

from cdk_aws_setup.cdk_aws_setup_stack import CdkAwsSetupStack

# example tests. To run these tests, uncomment this file along with the example
# resource in cdk_aws_setup/cdk_aws_setup_stack.py
def test_sqs_queue_created():
    app = core.App()
    stack = CdkAwsSetupStack(app, "cdk-aws-setup")
    template = assertions.Template.from_stack(stack)

#     template.has_resource_properties("AWS::SQS::Queue", {
#         "VisibilityTimeout": 300
#     })
