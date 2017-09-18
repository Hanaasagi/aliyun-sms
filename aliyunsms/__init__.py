import uuid
import hmac
import json
import pytz
import base64
import requests
import datetime
from collections import OrderedDict
from urllib.parse import quote


def _generate_sign(secret, tosign):
    mac = hmac.new(secret.encode("utf-8"), tosign.encode("utf-8"), "sha1")
    return base64.b64encode(mac.digest())


def urlencode(url):
    return quote(url).replace("+", "%20").replace("*", "%2A").\
        replace("%7E", "~").replace('/', '%2F')


def _get_utc():
    utc_now = datetime.datetime.now(pytz.timezone('utc'))
    return utc_now.strftime('%Y-%m-%dT%H:%M:%SZ')


class AliyunSMS:

    VERSION = '2017-05-25'
    SIGNATUREMETHOD = 'HMAC-SHA1'
    SIGNATUREVERSION = '1.0'
    FORMAT = 'JSON'
    ACTION = 'SendSms'
    URL_PREFIX = 'http://dysmsapi.aliyuncs.com/?Signature='

    def __init__(self, access_key_id, access_secret, regionid='cn-hangzhou'):
        self._access_key_id = access_key_id
        self._access_secret = access_secret
        self._regionid = regionid
        self._params = {}
        self._params['SignatureMethod'] = self.SIGNATUREMETHOD
        self._params['AccessKeyId'] = self._access_key_id
        self._params['RegionId'] = 'cn-hangzhou'

    @property
    def version(self):
        return self.VERSION

    def request(self, phone_numbers, sign, template_code, template_param):
        self._params['SignatureNonce'] = uuid.uuid4().hex
        self._params['SignatureVersion'] = self.SIGNATUREVERSION
        self._params['Timestamp'] = _get_utc()
        self._params['Format'] = self.FORMAT
        self._params['Action'] = self.ACTION
        self._params['Version'] = self.VERSION
        self._params['PhoneNumbers'] = phone_numbers
        self._params['SignName'] = sign
        self._params['TemplateCode'] = template_code
        self._params['TemplateParam'] = json.dumps(template_param)

        sorted_params = OrderedDict(sorted(self._params.items()))

        buf = []

        for key, value in sorted_params.items():
            buf.append('&{}={}'.format(*map(urlencode, (key, value))))

        params_str = ''.join(buf)[1:]

        tosign = 'GET&%2F&{}'.format(urlencode(params_str))
        sign = _generate_sign(self._access_secret + '&', tosign)
        signature = urlencode(sign)

        request_url = '{}{}&{}'.format(self.URL_PREFIX, signature, params_str)
        resp = requests.get(request_url)
        result = resp.json()
        result['status_code'] = resp.status_code
        return result


if __name__ == '__main__':
    cli = AliyunSMS(access_key_id='testId', access_secret='testSecret')
    resp = cli.request(phone_numbers='15300000001',
                       sign='阿里云短信测试专用',
                       template_code='SMS_71390007',
                       template_param={'customer': 'test'})
    print(resp)
