import random
import json
import requests

class Yunpian(object):

    def __init__(self, api_key):
        self.api_key = api_key
        self.single_send_url = "https://sms.yunpian.com/v2/sms/single_send.json"

    def send_sms(self, code, mobile):
        params = {
            "apikey":self.api_key,
            "mobile":mobile,
            #"text":"【蚂蚁行者】欢迎使用{name}，您的手机验证码是{code}。本条信息无需回复".format(name = "蚂蚁行者", code = code)
            "text": "【慕学生鲜】您的验证码是{code}。如非本人操作，请忽略本短信".format(code=code)
        }
        response = requests.post(self.single_send_url,data=params)
        re_dict = json.loads(response.text)
        return re_dict

if __name__ == "__main__":
    yun_pian = Yunpian("d6c4ddbf50ab36611d2f52041a0b949e")
    yun_pian.send_sms("0503","18792554545")