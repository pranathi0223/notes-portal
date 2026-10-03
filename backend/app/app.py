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
        "Access-Control-Allow-Methods": "GET,POST,PUT,DELETE,OPTIONS"
    }

    if method == "OPTIONS":
        return {
            "statusCode": 200,
            "headers": cors_headers,
            "body": ""
        }

    # GET - Get all notes
    if method == "GET":
        response = table.scan()

        return {
            "statusCode": 200,
            "headers": cors_headers,
            "body": json.dumps(response.get("Items", []))
        }

    # POST - Add a new note
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

    # PUT - Edit a note
    if method == "PUT":
        note_id = event.get("pathParameters", {}).get("id")

        body = json.loads(event.get("body", "{}"))

        if not note_id:
            return {
                "statusCode": 400,
                "headers": cors_headers,
                "body": json.dumps({"message": "Note ID is required"})
            }

        response = table.update_item(
            Key={"id": note_id},
            UpdateExpression="SET #t = :title, #c = :content",
            ExpressionAttributeNames={
                "#t": "title",
                "#c": "content"
            },
            ExpressionAttributeValues={
                ":title": body.get("title", ""),
                ":content": body.get("content", "")
            },
            ReturnValues="ALL_NEW"
        )

        return {
            "statusCode": 200,
            "headers": cors_headers,
            "body": json.dumps(response.get("Attributes", {}))
        }

    # DELETE - Delete a note
    if method == "DELETE":
        note_id = event.get("pathParameters", {}).get("id")

        if not note_id:
            return {
                "statusCode": 400,
                "headers": cors_headers,
                "body": json.dumps({"message": "Note ID is required"})
            }

        table.delete_item(
            Key={"id": note_id}
        )

        return {
            "statusCode": 200,
            "headers": cors_headers,
            "body": json.dumps({
                "message": "Note deleted successfully"
            })
        }

    return {
        "statusCode": 405,
        "headers": cors_headers,
        "body": json.dumps({
            "message": "Method not allowed"
        })
    }