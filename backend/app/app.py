import json

notes = []


def lambda_handler(event, context):
    method = event.get("httpMethod", "GET")

    # Get all notes
    if method == "GET":
        return {
            "statusCode": 200,
            "headers": {"Content-Type": "application/json"},
            "body": json.dumps(notes)
        }

    # Create a note
    if method == "POST":
        body = json.loads(event.get("body", "{}"))

        note = {
            "id": len(notes) + 1,
            "title": body.get("title", ""),
            "content": body.get("content", "")
        }

        notes.append(note)

        return {
            "statusCode": 201,
            "headers": {"Content-Type": "application/json"},
            "body": json.dumps(note)
        }

    return {
        "statusCode": 405,
        "body": "Method not allowed"
    }