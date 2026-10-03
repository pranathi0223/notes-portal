import json
import os
import uuid
import boto3

dynamodb = boto3.resource("dynamodb")
table = dynamodb.Table(os.environ["TABLE_NAME"])


def lambda_handler(event, context):
    method = event.get("httpMethod", "GET")

    # Get all notes
    if method == "GET":
        response = table.scan()

        return {
            "statusCode": 200,
            "headers": {"Content-Type": "application/json"},
            "body": json.dumps(response.get("Items", []))
        }

    # Create a note
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
            "headers": {"Content-Type": "application/json"},
            "body": json.dumps(note)
        }

    return {
        "statusCode": 405,
        "body": "Method not allowed"
    }