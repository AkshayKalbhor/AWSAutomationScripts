import json
import logging
import boto3

# ロギングの基本設定(infoレベルを指定)
logging.basicConfig(level=logging.INFO)
logging.info('info')

def check_instance_status(instance_id, expected_status) -> bool:
    client = boto3.client('ec2')
    response = client.describe_instance_status(
        InstanceIds=[instance_id],
    )

    status = response['InstanceStatuses'][0]['InstanceState']['Name']

    ## TODO:
    # Can consider to handle the scenario's when the status is other than stopped
    # possible statuses : 'pending'|'running'|'shutting-down'|'terminated'|'stopping'|'stopped'
    # Can throw an error when the status is shutting down / terminated
    # Can wait when the status is pending

    if status==expected_status:
        return True
    else:
        return False
    return None

##
# returns true if the operation was successful
# returns false if otherwise
# Response codes are as follows 
#0 : pending
#16 : running
#32 : shutting-down
#48 : terminated
#64 : stopping
#80 : stopped
##
def check_operation_status(response, operation):
    code = None
    result = False
    if operation == "start":
        code=response['StartingInstances'][0]['CurrentState']['Code']
        if code == 0:
            result = True
    elif operation == "stop":
        code=response['StoppingInstances'][0]['CurrentState']['Code']
        if code == 64:
            result = True
    return result

def lambda_handler(event, context):

    print("===== START OF FUNCTION ====")
    client = boto3.client('ec2')
    
    # fetch instance ids to be resized.
    # Insert your Instance ID here
    instance_id = event["instance_id"]
    #my_instance = 'i-076377f3799ad513b'

    ## Fetch the operation to be performed
    operation = event["operation"]


    match operation:
        case "start":
            #Check if the instance is stopped
            ## Commented as the response of the start_instances does not provide details 
            # of InstanceStatuses as described in the documentation, probably a bug with Boto3.
            #if check_instance_status(instance_id, "stopped"):
            # Start the instance
            logging.info("Executing code to Start the instance.")
            response = client.start_instances(InstanceIds=[instance_id])
            if check_operation_status(response, "start"):
                return 1
            else :
                raise Exception("The operation terminated unsuccessfully")
            #else :
            #    raise Exception("The operation terminated unsuccessfully")

        case "stop":
            #Check if the instance is running
            if check_instance_status(instance_id, "running"):
                # Stop the instance
                logging.info("Executing code to Stop the instance.")
                response = client.stop_instances(InstanceIds=[instance_id])
                if check_operation_status(response, "stop"):
                    return 1
                else :
                    raise Exception("The operation terminated unsuccessfully")
            else :
                raise Exception("The operation terminated unsuccessfully")
    print("===== END OF FUNCTION ====")
    return {
        'statusCode': 200,
        'body': json.dumps('Lambda function completed successfully')
    }