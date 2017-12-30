import json
import boto3
from config import config
import urllib.request

# Open Product Data http://www.product-open-data.com/
__gtin_uri__ = "https://pod.opendatasoft.com/api/records/1.0/search/"


def handler(event, context):
    print(str(event))

    for record in event['Records']:
        msg = record['Sns']['Message']
        print('message: ' + msg)
        msg = json.loads(msg)
        upc_a = msg['upc_a']
        fields = enrichupc(upc_a)
        displayText = fields['brand_nm'] + ' ' + fields['gtin_nm'] + ' added to shopping list (' + upc_a + ')'
        sendsms(config['targetPhone'], displayText)


def sendsms(phone, msg):
    print('publish phone: ' + phone + ' msg:' + msg)
    client = boto3.Session(profile_name=config['awsProfile']).client('sns')
    response = client.publish(
        PhoneNumber=phone,
        Message=msg,
        MessageAttributes={'AWS.SNS.SMS.SMSType': {'DataType': 'String', 'StringValue': 'Transactional'}}
    )
    print('publish response: ' + str(response))
    return response


def enrichupc(upc_a):
    gtin = upc_a.rjust(13, '0')  # zero pad to get to GTIN format (13)
    uri = __gtin_uri__ + ("?dataset=pod_gtin&q=%s" % gtin)
    f = urllib.request.urlopen(uri)
    data = f.read()
    data = json.loads(data)
    for record in data['records']:
        return record['fields']
    return None
