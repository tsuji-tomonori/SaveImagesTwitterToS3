import aws_cdk as cdk

from save_images_twitter_to_s3.save_images_twitter_to_s3_stack import SaveImagesTwitterToS3Stack


app = cdk.App()
SaveImagesTwitterToS3Stack(
    app, 
    "SaveImagesTwitterToS3Stack",
    stack_name="SaveImagesTwitterToS3Stack"
)

app.synth()
