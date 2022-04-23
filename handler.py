
import requests
import os
import json
import boto3

def hello(event, context):
    if event is None:
        return {'status' : 'Falha', 'code' : None, 'results' : None, 'message' : 'Nenhum JSON enviado pelo Legal Control'}

    sqs_client = boto3.client("sqs", region_name="us-east-1")
    print("Booom")
    message = {"keyYEAH": "value_FOI"}
    response = sqs_client.send_message(
    QueueUrl="https://sqs.us-east-1.amazonaws.com/627333228566/queueName-Vai",
        MessageBody=json.dumps(message)
    )

    print(response)
    
    try:
        # url = os.getenv('THEMIS_URL') + "/legalcontrol"
        url = "https://webhook.site/45f418ab-8615-42d8-a594-db7cce5dcf94"   
        print("B e W")
        response = requests.post(
            url,
            data=json.dumps(event)
        )

        if response.status_code == 200 or response.status_code == 201:
            return {'status' : 'Ok', 'code' : response.status_code, 'results' : "Envio de JSON feito com sucesso para o Sistema Themis.", 'message' : event}
        elif response.status_code == 404:
            return {'status' : 'Falha', 'code' : response.status_code, 'results' : None, 'message' : 'Nenhuma informação foi enviada com sucesso para o Sistema Themis, pois possivelmente a url esteja errada.'}
        else:
            return {'status' : 'Falha', 'code' : response.status_code, 'results' : None, 'message' : 'Erro de servidor ao requisitar o Sistema Themis.'}

    except Exception as e:
        return {'status' : 'Falha', 'code' : None, 'results' : event, 'message' : e}

def receive_message():
    sqs_client = boto3.client("sqs", region_name="us-east-1")
    print("Booo222m")
    response = sqs_client.receive_message(
    QueueUrl="https://sqs.us-east-1.amazonaws.com/627333228566/queueName-Vai",
        MaxNumberOfMessages=1,
        WaitTimeSeconds=10,
    )

    print(f"Number of messages received: {len(response.get('Messages', []))}")

    for message in response.get("Messages", []):
        message_body = message["Body"]
        print(f"Message body: {json.loads(message_body)}")
        print(f"Receipt Handle: {message['ReceiptHandle']}")