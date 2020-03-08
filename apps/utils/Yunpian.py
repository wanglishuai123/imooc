import requests
import json
from edu.settings import YP_API_KEY

def send_single_sms(code,mobile):
    url = "https://sms.yunpian.com/v2/sms/single_send.json"

    res = requests.post(url,data={
        "apikey":YP_API_KEY,
        "text": "【白面书生网络工作室】亲爱的，您的验证码是{},请尽快验证。".format(code),
        "mobile":mobile
    })

    return json.loads(res.text)



if __name__ == '__main__':
    res = send_single_sms("3123","15235894102")