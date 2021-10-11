# CodeBy MCQTSS(2138939969)
# 注释没怎么写(懒)
# 参考:https://wiki.vg/Microsoft_Authentication_Scheme
import requests
import json
from selenium import webdriver
import time


class Minecraft_login:
    def __init__(self):
        self.headers = {
            'accept-language': 'zh-CN',
            'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/84.0.4147.105 Safari/537.36',
            'Content-Type': 'application/x-www-form-urlencoded'
        }
        self.headers_json = {
            'Accept': 'application/json',
            'accept-language': 'zh-CN',
            'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/84.0.4147.105 Safari/537.36',
            'Content-Type': 'application/json'
        }
        # 2个请求时使用的请求头

    def getuuid_headers_json(self, token):  # 获取UUID时需要提交的请求头
        return {
            'Accept': 'application/json',
            'accept-language': 'zh-CN',
            'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/84.0.4147.105 Safari/537.36',
            'Content-Type': 'application/json',
            'Authorization': "Bearer " + token
        }

    def qzjwb(self, text, start_str, end):  # 取出文本中间文本
        start = text.find(start_str)
        if start >= 0:
            start += len(start_str)
            end = text.find(end, start)
            if end >= 0:
                return text[start:end].strip()

    def microsoft_login(self, mail, password):  # Microsoft全自动登录,使用selenium,实际客户端不推荐使用
        driver = webdriver.Chrome(
            executable_path="")  # executable_path可以去掉,我电脑有Bug
        driver.get(
            "https://login.live.com/oauth20_authorize.srf?client_id=00000000402b5328&response_type=code&scope=service%3A%3Auser.auth.xboxlive.com%3A%3AMBI_SSL&redirect_uri=https%3A%2F%2Flogin.live.com%2Foauth20_desktop.srf")
        driver.find_element_by_xpath('//*[@id="i0116"]').send_keys(mail)
        driver.find_element_by_xpath('//*[@id="idSIButton9"]').click()
        time.sleep(2)
        driver.find_element_by_xpath('//*[@id="i0118"]').send_keys(password)
        driver.find_element_by_xpath('//*[@id="idSIButton9"]').click()
        while True:
            url = driver.current_url
            if str(url).find("https://login.live.com/oauth20_desktop.srf") != -1:
                driver.close()
                return url

    def get_token(self, code):
        post_data = "client_id=00000000402b5328&code={}&grant_type=authorization_code&redirect_uri=https://login.live.com/oauth20_desktop.srf&scope=service::user.auth.xboxlive.com::MBI_SSL".format(
            code)
        ret = requests.post(url="https://login.live.com/oauth20_token.srf", data=post_data, headers=self.headers).text
        return json.loads(ret)

    def XboxLive_XBL(self, token):
        post_data = {
            "Properties": {
                "AuthMethod": "RPS",
                "SiteName": "user.auth.xboxlive.com",
                "RpsTicket": token
            },
            "RelyingParty": "http://auth.xboxlive.com",
            "TokenType": "JWT"
        }
        ret = requests.post(url="https://user.auth.xboxlive.com/user/authenticate", data=json.dumps(post_data),
                            headers=self.headers_json).text
        return json.loads(ret)

    def XboxLive_XSTS(self, token):
        post_data = {
            "Properties": {
                "SandboxId": "RETAIL",
                "UserTokens": [
                    token
                ]
            },
            "RelyingParty": "rp://api.minecraftservices.com/",
            "TokenType": "JWT"
        }
        ret = requests.post(url="https://xsts.auth.xboxlive.com/xsts/authorize", data=json.dumps(post_data),
                            headers=self.headers_json).text
        return json.loads(ret)

    def Minecraft_verify(self, token, uhs):
        post_data = {
            "identityToken": "XBL3.0 x={};{}".format(uhs, token)
        }
        ret = requests.post(url="https://api.minecraftservices.com/authentication/login_with_xbox",
                            data=json.dumps(post_data),
                            headers=self.headers_json).text
        return json.loads(ret)

    def Minecraft_uuid(self, token):
        ret = requests.get(url='https://api.minecraftservices.com/minecraft/profile',
                           headers=self.getuuid_headers_json(token)).text
        ret = json.loads(ret)
        try:
            if ret['error'] == "NOT_FOUND":
                return ret['The server has not found anything matching the request URI']
        except:
            return ret