import json
# import sagemaker
import base64
# from sagemaker.serializers import IdentitySerializer
import boto3
runtime = boto3.client('runtime.sagemaker')

# Fill this in with the name of your deployed model
ENDPOINT = "image-classification-2023-10-28-13-22-57-716"

def lambda_handler(event, context):
    print(event['body']['image_data'])
    # Decode the image data
    image = base64.b64decode(event['body']['image_data'])

    # # Instantiate a Predictor
    # predictor = sagemaker.predictor.Predictor(ENDPOINT)

    # # For this model the IdentitySerializer needs to be "image/png"
    # predictor.serializer = IdentitySerializer("image/png")
    
    # # Make a prediction:
    # inferences = predictor.predict(image)
    
    # Note: Fix the import sagemaker issue
    response = runtime.invoke_endpoint(
        EndpointName=ENDPOINT,
        ContentType='image/png',
        Body=image    
    ) 
    inferences = response['Body'].read()
    
    # We return the data back to the Step Function    
    event["inferences"] = inferences.decode('utf-8')
    
    return {
        "statusCode": 200,
        "body": {
            "image_data": event['body']['image_data'],
            "s3_bucket": event['body']['s3_bucket'],
            "s3_key": event['body']['s3_key'],
            "inferences": event['inferences'],
        }
    }