#import boto3
import os
import json
import logging

logger = logging.getLogger()
logger.setLevel(logging.INFO)

def lambda_handler(event, context):
    logger.info("Received event is {}".format(event))

    #Variables declaration section.
    DATA = []

    if 'Events' in event:
        events = event['Events']
        #print(json.dumps(events, indent=4, sort_keys=True))
        #Iterate on each received event
        # process the event and send it to Hinemos.
        for event in events:

            #print(json.dumps(event, indent=4, sort_keys=True))

            #populate the object in the format that is expected by hinemos.
            data_details = {}
            data_details['DATE'] = event["Date"]
            data_details['TYPE'] = "STRING"
            #TODO Confirm if the datadetails key will always be Aurora Status. RDS ?
            data_details['KEY'] = "Aurora_Status"
            data_details['MSG'] = event["Message"]
            DATA.append(data_details)

        #Call function to send data to Hinemos.
        try:
            send_messages_to_hinemos(DATA)
        except Exception as ex:
            logger.error("Error occured while sending data to Hinemos. Error is {}".format(ex))
    else:
        logger.log("Wrong event received to the lambda function. event is :{}".format(event))

def send_messages_to_hinemos(DATA):

    print(json.dumps(DATA, indent=4, sort_keys=True))

    #Fetch Hinemos endpoint from environment variables.
    #Fetch hinemos port from environment variables.
    #Send data to hinemos.
    #Throw error if the connection to hinemos fails.
    if "HINEMOS_SERVER_ENDPOINT" in os.environ and \
        "HINEMOS_SERVER_PORT" in os.environ:
        hine_svr = os.environ("HINEMOS_SERVER_ENDPOINT")
        hine_svr_port = os.environ("HINEMOS_SERVER_PORT")

        try:
            #TODO Code to connect to Hinemos server goes here
            print("")
            response = ""
            return response
        except Exception as ex:
            raise ex
    else:
        raise Exception("Necessary environment variables not found.")

if __name__ == "__main__":

    context = ""
    with open('RDSEventsToLambdaToHinemos\sample_instance_backup_event.json', 'r') as f:
        event = json.load(f)
    # Verify the imported json.
    #print(json.dumps(event, indent=4, sort_keys=True))
    
    #Calling the lambda function.
    lambda_handler(event, context)