# aliyun-sms
![](https://img.shields.io/badge/Python-3-3AA066.svg)  
阿里云短信 SDK

由于 aliyun 默认的 Python SDK 是 Python 2.x 版本的，所以自己实现了一个 3.x 版本的

实现参考 [API 文档](https://help.aliyun.com/document_detail/56189.html?spm=5176.doc55317.6.568.HnirA8)

**Usage**

```
cli = AliyunSMS(access_key_id='testId', access_secret='testSecret')
resp = cli.request(phone_numbers='15300000001',
                   sign='阿里云短信测试专用',
                   template_code='SMS_71390007',
                   template_param={'customer': 'test'})

```


**Response**
```
{'Message': 'Specified access key is not found.', 'RequestId': '91AC1C92-ECC4-4C07-AE6E-4D53DD15D872', 'HostId': 'dysmsapi.aliyuncs.com', 'Code': 'InvalidAccessKeyId.NotFound', 'status_code': 404}
```
