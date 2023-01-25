import json
import boto3

s3Client = boto3.client('s3')
cluster_name = "arn:aws:ecs:us-east-1:266070530669:cluster/cluster-awake-and-shut-down"


def lambda_handler(event, context):
    print(f"Event -> {event}")
    print(f"\nContext -> {context}")

    # print(f"Vou buscar action")
    # cloudwatchvalue = event['action']
    # print(f"Peguei action {cloudwatchvalue}")

    # print(f"Vou buscar cluster")
    # cluster_name = event['cluster']
    # print(f"Peguei cluster {cluster_name}")

    print(f"Vou conectar no client ecs")
    client = boto3.client('ecs')
    print(f"Me conectei com sucesso no ecs")

    try:
        response = client.list_services(
            cluster=cluster_name,
            launchType="FARGATE",
            # maxResults=2,
            # schedulingStrategy="REPLICA"
        )
        print(f"Sucesso no response do list_tasks => {response['serviceArns']}")
    except:
        print(f"Didnt work Cluster = {cluster_name}")

    service_list = response['serviceArns']

    start_task = "rafawainer-s3-lambda-starter"
    print(f"Start Key = {start_task}")
    stop_task = "rafawainer-s3-lambda-stopper"
    print(f"Stop Key = {stop_task}")
    s3_bucket_key = event['Records'][0]['s3']['bucket']['name']
    print(f"S3 Bucket Key = {s3_bucket_key}")

    # start service with desired tasks
    # if 'start' == cloudwatchvalue:
    if start_task == s3_bucket_key:
        spawncontainer(service_list, cluster_name)
        print(f"Start spwncontainer com sucesso")

    # stop service with desired tasks
    # elif 'stop' == cloudwatchvalue:
    elif stop_task == s3_bucket_key:
        stopcontainer(service_list, cluster_name)
        print(f"Stop stopcontainer com sucesso")

    return {
        'statusCode': 200,
        'body': json.dumps('Script finished')

    }


### Sets the desired count of tasks per service to 1
### Container will spawn after a few moments
def spawncontainer(servicearns, clusterName):
    client = boto3.client('ecs')
    for srv in servicearns:
        responseUpdate = client.update_service(
            cluster=clusterName,
            service=srv,
            desiredCount=2,
        )


### Sets the desired count of tasks per service to 0
### Services still runs but without any container
def stopcontainer(servicearns, clusterName):
    client = boto3.client('ecs')
    for srv in servicearns:
        responseUpdate = client.update_service(
            cluster=clusterName,
            service=srv,
            desiredCount=0,
        )