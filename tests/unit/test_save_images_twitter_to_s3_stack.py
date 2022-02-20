import aws_cdk as core
import aws_cdk.assertions as assertions

from save_images_twitter_to_s3.save_images_twitter_to_s3_stack import SaveImagesTwitterToS3Stack

# example tests. To run these tests, uncomment this file along with the example
# resource in save_images_twitter_to_s3/save_images_twitter_to_s3_stack.py
def test_sqs_queue_created():
    app = core.App()
    stack = SaveImagesTwitterToS3Stack(app, "save-images-twitter-to-s3")
    template = assertions.Template.from_stack(stack)

#     template.has_resource_properties("AWS::SQS::Queue", {
#         "VisibilityTimeout": 300
#     })
