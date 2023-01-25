import json

import lambda_handler

event_json = '{"Records": [{"eventVersion": "2.1", "eventSource": "aws:s3", "awsRegion": "us-east-1", "eventTime": "2023-01-25T20:46:40.545Z", "eventName": "ObjectCreated:Put", "userIdentity": {"principalId": "A2U77GNYX3CCOL"}, "requestParameters": {"sourceIPAddress": "177.9.118.145"}, "responseElements": {"x-amz-request-id": "QPXK7C5VZKD8ANW7", "x-amz-id-2": "TNhFbSUVG5IaFLZEy7r9CEX/iI8Uindn6/wRhdTyxtOgXVRpqEPx4zW2kqWTFCeT9Ux7l2z+BtNky6ODYqy0qKhutRAKulerz9AjAAhf6/k="}, "s3": {"s3SchemaVersion": "1.0", "configurationId": "8ade7ce4-4403-4a02-b61b-9213a232b9b3", "bucket": {"name": "rafawainer-s3-lambda-starter", "ownerIdentity": {"principalId": "A2U77GNYX3CCOL"}, "arn": "arn:aws:s3:::rafawainer-s3-lambda-stopper"}, "object": {"key": "59b1887f-3b7f-41d6-ba91-14d5f26481ed.csv", "size": 175, "eTag": "bd1782de779a41e6fe53727b4a12f5e6", "sequencer": "0063D195307A5385AB"}}}]}'
context = 'LambdaContext([aws_request_id=cb8142e6-3c6e-43bb-8ae6-2ae409a13593,log_group_name=/aws/lambda/start-stop-ecs-fargate-nginx,log_stream_name=2023/01/25/[$LATEST]3d747da48db441d4b1c37a4da69db08e,function_name=start-stop-ecs-fargate-nginx,memory_limit_in_mb=128,function_version=$LATEST,invoked_function_arn=arn:aws:lambda:us-east-1:266070530669:function:start-stop-ecs-fargate-nginx,client_context=None,identity=CognitoIdentity([cognito_identity_id=None,cognito_identity_pool_id=None])])'
event = json.loads(event_json)

lambda_handler.lambda_handler(event, context)