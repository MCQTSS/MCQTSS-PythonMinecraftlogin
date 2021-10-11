import requests
import json


def send_post(url, post):
    return requests.post(url=url, data=post).text


def login(user, passw):
    post = {
        "name": "Minecraft",
        "version": "1"
    }
    post = {
        "agent": post,
        "username": user,
        "password": passw,
        "requestUser": True
    }
    post = json.dumps(post)
    return send_post("https://authserver.mojang.com/authenticate", post)


def loginout(user, passw):
    post = {
        "username": user,
        "password": passw
    }
    post = json.dumps(post)
    return send_post("https://authserver.mojang.com/signout", post)

