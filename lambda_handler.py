import json
import boto3

cluster_name = "arn:aws:ecs:us-east-1:266070530669:cluster/cluster-awake-and-shut-down"


def session_boto3():

    with open("credentials/credentials.json", encoding='utf-8') as arquivo_json:
        dados = json.load(arquivo_json)

        # Para consultar credentials + session token, utilizar codigo abaixo com o aws cli instalado
        # aws sts get-session-token --duration-seconds 129600
        aws_region = dados['aws_region']
        aws_access_id = dados['aws_access_key_id']
        aws_secret_key = dados['aws_secret_access_key']
        aws_access_token = dados['aws_access_token']

        return boto3.Session(
            aws_access_key_id=aws_access_id,
            aws_secret_access_key=aws_secret_key,
            aws_session_token=aws_access_token,
            region_name=aws_region
        )


# Sets the desired count of tasks per service to 1
# Container will spawn after a few moments
def spawncontainer(servicearns, cluster_name):
    client = boto3.client('ecs')
    for srv in servicearns:
        client.update_service(
            cluster=cluster_name,
            service=srv,
            desiredCount=2,
        )


# Sets the desired count of tasks per service to 0
# Services still runs but without any container
def stopcontainer(servicearns, cluster_name):
    client = boto3.client('ecs')
    for srv in servicearns:
        client.update_service(
            cluster=cluster_name,
            service=srv,
            desiredCount=0,
        )


def lambda_handler(event, context):
    print(f"\nEvent -> {event}")
    print(f"\nContext -> {context}")

    session = session_boto3()
    session.client('s3')

    # print(f"Vou buscar action")
    # cloudwatchvalue = event['action']
    # print(f"Peguei action {cloudwatchvalue}")

    # print(f"Vou buscar cluster")
    # cluster_name = event['cluster']
    # print(f"Peguei cluster {cluster_name}")

    print(f"\nVou conectar no client ecs")
    client = boto3.client('ecs')
    print(f"\nMe conectei com sucesso no ecs")

    try:
        response = client.list_services(
            cluster=cluster_name,
            launchType="FARGATE"
            # maxResults=2,
            # schedulingStrategy="REPLICA"
        )
        print(f"\nSucesso no response do list_tasks => {response['serviceArns']}")
    except:
        print(f"\nDidnt work Cluster = {cluster_name}")

    service_list = response['serviceArns']

    start_task = "rafawainer-s3-lambda-starter"
    print(f"\nStart Key = {start_task}")
    stop_task = "rafawainer-s3-lambda-stopper"
    print(f"Stop Key = {stop_task}")

    print(f"\nEvent Records -> {event['Records']}")
    print(f"Event Records[s3] -> {event['Records'][0]['s3']}")
    print(f"Event Records[s3][bucket] -> {event['Records'][0]['s3']['bucket']}")
    print(f"Event Records[s3][bucket][name\ -> {event['Records'][0]['s3']['bucket']['name']}")

    s3_bucket_key = event['Records'][0]['s3']['bucket']['name']
    print(f"S3 Bucket Key = {s3_bucket_key}")

    # start service with desired tasks
    # if 'start' == cloudwatchvalue:
    if start_task == s3_bucket_key:
        spawncontainer(service_list, cluster_name)
        print(f"\nStart spwncontainer com sucesso")

    # stop service with desired tasks
    # elif 'stop' == cloudwatchvalue:
    elif stop_task == s3_bucket_key:
        stopcontainer(service_list, cluster_name)
        print(f"\nStop stopcontainer com sucesso")

    return {
        'statusCode': 200,
        'body': json.dumps('Script finished')

    }
