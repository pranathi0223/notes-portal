import json
import os
import uuid
import boto3


def lambda_handler(event, context):

    dynamodb = boto3.resource(
        "dynamodb",
        endpoint_url=os.environ["DYNAMODB_ENDPOINT"],
        region_name="ap-south-1",
        aws_access_key_id="dummy",
        aws_secret_access_key="dummy"
    )

    table = dynamodb.Table(os.environ["TABLE_NAME"])

    method = event.get("httpMethod", "GET")

    cors_headers = {
        "Content-Type": "application/json",
        "Access-Control-Allow-Origin": "*",
        "Access-Control-Allow-Headers": "Content-Type",
        "Access-Control-Allow-Methods": "GET,POST,OPTIONS"
    }

    if method == "OPTIONS":
        return {
            "statusCode": 200,
            "headers": cors_headers,
            "body": ""
        }

    if method == "GET":
        response = table.scan()

        return {
            "statusCode": 200,
            "headers": cors_headers,
            "body": json.dumps(response.get("Items", []))
        }

    if method == "POST":
        body = json.loads(event.get("body", "{}"))

        note = {
            "id": str(uuid.uuid4()),
            "title": body.get("title", ""),
            "content": body.get("content", "")
        }

        table.put_item(Item=note)

        return {
            "statusCode": 201,
            "headers": cors_headers,
            "body": json.dumps(note)
        }

    return {
        "statusCode": 405,
        "headers": cors_headers,
        "body": json.dumps({
            "message": "Method not allowed"
        })
    }