import boto3
import os
import json
import logging

# ロギングの基本設定(infoレベルを指定)
logging.basicConfig(level=logging.INFO)
logging.info('info')

def lambda_handler(event, context):
    
    print(event)
    if 'Records' in event:
        records = event['Records'][0]
        filename = records["s3"]["object"]["key"]
        filenameArray = filename.split("-")
        name = filenameArray[len(filenameArray)-1]
        if name.lower()="app.zip":
            print("Continue deployment of App")
        elif name.lower() = "web.zip":
            print("Continue deployment of Web")
        elif name.lower() = "batch.zip":
            print("Continue deployment of batch")
        else
            print("wrong file uploaded")

    """alarm_names = []
    #Fetch parameters from event.
    if "Target_Alarms" in event:
        #Fetch parmaeters from event as it is scheduled execution
        alarm_names = event["Target_Alarms"]
        alarm_operations = event["Alarm_Operation"] 
    else:
        #CASE Manual execution
        #Fetch target alarms from Environment variables
        if os.environ["Target_Alarms"]:
            alarm_names = os.environ["Target_Alarms"].split(',')

        alarm_names = [ i.strip() for i in alarm_names]
        #Fetch alarm operation from Environment variables
        if os.environ["Alarm_Operation"]:
            alarm_operations = os.environ["Alarm_Operation"]
    
    print("Alarm names are {}, operation is {}".format(alarm_names, alarm_operations))
    # Create CloudWatch client
    cloudwatch = boto3.client('cloudwatch')

    if alarm_operations.upper() == 'ON':
        # Disable alarm
        cloudwatch.enable_alarm_actions(
            AlarmNames=alarm_names,
        )
    elif alarm_operations.upper() == 'OFF':
        # Disable alarm
        cloudwatch.disable_alarm_actions(
            AlarmNames=alarm_names,
        )
    else:
        logger.log("[I] Invalid input for alarm operations.")"""
    
    return {
        'statusCode': 200,
        'body': json.dumps('Hello from Lambda!')
    }