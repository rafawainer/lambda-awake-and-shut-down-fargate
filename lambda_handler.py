import json
import boto3

def lambda_handler(event, context):
    print(f"Event -> {event}")
    print(f"\nContext -> {context}")

    print(f"Vou buscar action")
    cloudwatchvalue = event['action']
    print(f"Peguei action {cloudwatchvalue}")

    print(f"Vou buscar cluster")
    cluster_name = event['cluster']
    print(f"Peguei cluster {cluster_name}")

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
        print(f"Didnt work Cluster = {cluster_name} / Event {cloudwatchvalue}")

    service_list = response['serviceArns']

    if 'start' == cloudwatchvalue:
        spawncontainer(service_list, cluster_name)
        print(f"Start spwncontainer com sucesso")

    elif 'stop' == cloudwatchvalue:
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