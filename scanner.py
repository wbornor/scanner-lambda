import json
import boto3
from config import config
import urllib.request, urllib.parse

# Product Open Data http://www.product-open-data.com/
__gtin_uri__ = "https://pod.opendatasoft.com/api/records/1.0/search/"

# ifttt webhook
__ifttt_uri___ = "https://maker.ifttt.com/trigger/%s/with/key/%s" % (config['iftttEvent'], config['iftttKey'])


def handler(event, context):
    print(str(event))

    for record in event['Records']:
        msg = record['Sns']['Message']
        print('message: ' + msg)
        msg = json.loads(msg)
        upc_a = msg['upc_a']
        fields = enrichupc(upc_a)
        if fields is None:
            displayText = upc_a + ' not found'
            trigger_ifttt(upc_a, None, None)
        else:
            displayText = fields['brand_nm'] + ' ' + fields['gtin_nm'] + ' (' + upc_a + ') scanned'
            trigger_ifttt(upc_a, fields['brand_nm'], fields['gtin_nm'])

        # sendsms(config['targetPhone'], displayText)

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
    with urllib.request.urlopen(uri) as response:
        data = json.loads(response.read())
        for record in data['records']:
            return record['fields']
    return None


def trigger_ifttt(upc_a, brand, name):
    uri = __ifttt_uri___
    body = {'value1': brand, 'value2': name, 'value3': upc_a}
    data = urllib.parse.urlencode(body).encode('ascii')
    with urllib.request.urlopen(uri, data) as response:
        print(response.read())
