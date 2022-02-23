import aws_cdk as core
import aws_cdk.assertions as assertions

from save_images_twitter_to_s3.save_images_twitter_to_s3_stack import SaveImagesTwitterToS3Stack


def test_snapshot(snapshot):
    app = core.App()
    stack = SaveImagesTwitterToS3Stack(
        app,
        "SaveImagesTwitterToS3Stack",
        stack_name="SaveImagesTwitterToS3Stack"
    )
    # template = assertions.Template.from_stack(stack).to_json()
    # snapshot.assert_match(template)
