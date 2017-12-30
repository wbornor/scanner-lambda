import scanner
from config import config
import unittest

__sns__ = {'Records': [{'EventSource': 'aws:sns', 'EventVersion': '1.0',
                        'EventSubscriptionArn': 'arn:aws:sns:EXAMPLE',
                        'Sns': {'Type': 'Notification',
                                'MessageId': '3e7ecc20-bee0-5c76-b2fc-9ee0217918e3',
                                'TopicArn': 'arn:aws:sns:EXAMPLE',
                                'Subject': 'upc-capture',
                                'Message': '{"upc_a": "011110672698"}',
                                'Timestamp': '2017-12-29T19:54:01.294Z',
                                'SignatureVersion': '1',
                                'Signature': 'EXAMPLE',
                                'SigningCertUrl': 'EXAMPLE',
                                'UnsubscribeUrl': 'EXAMPLE',
                                'MessageAttributes': {}}}]}


class TestScanner(unittest.TestCase):
    @unittest.skip
    def testSNSMessageTriggersHandler(self):
        event = __sns__
        scanner.handler(event, None)

    @unittest.skip('external dependencies')
    def testSMS(self):
        response = scanner.sendsms(config['targetPhone'], 'test')
        self.assertEqual(response['ResponseMetadata']['HTTPStatusCode'], 200)

    @unittest.skip('external dependencies')
    def testEnrichUPC(self):
        fields = scanner.enrichupc('011110672698')
        self.assertEqual(fields['brand_nm'], 'Kroger')
        self.assertEqual(fields['gtin_nm'], 'Peanut Butter')

    # @unittest.skip('external dependencies')
    def testEnrichUPCNoMatch(self):
        fields = scanner.enrichupc('012345678901')
        self.assertIsNone(fields)

    @unittest.skip('external dependencies')
    def testTriggerIfttt(self):
        scanner.trigger_ifttt('011110672698', 'Kroger', 'Peanut Butter')

if __name__ == '__main__':
    unittest.main()
