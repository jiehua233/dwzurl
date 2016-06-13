#!/usr/bin/env python
# -*- coding: utf-8 -*-


import random
import urllib
import redis
import logging
import torndb
import falcon
import validators
import ujson as json
from repoze.lru import lru_cache
from wsgiref import simple_server
from etc import config


db = torndb.Connection(**config.mysql)
rpool = redis.ConnectionPool(**config.redis)
rds = redis.StrictRedis(connection_pool=rpool)

chars = "0123456789abcdefghijklmnopqrstuvwxyzABCDEFGHIJKLMNOPQRSTUVWXYZ"


@lru_cache(9999)
def tag_key(tag):
    return config.rds_prefix + "tag=%s" % tag


@lru_cache(9999)
def url_key(url):
    return config.rds_prefix + "url=%s" % url


def rds_cache(method):
    def wrapper(self, tag):
        url = rds.get(tag_key(tag))
        if url is None:
            url = method(self, tag)
            if url is not None:
                rds.setex(tag_key(tag), 86400, url)
                # 一定时间内相同的url转换相同的tag
                rds.setex(url_key(url), 86400, tag)

        return url
    return wrapper


class ShortLinkError(Exception):

    def __init__(self, code=0, tag="", msg=""):
        self.code = code
        self.tag = tag
        self.msg = msg

    @staticmethod
    def handle(ex, req, resp, params):
        resp.status = falcon.HTTP_200
        resp.body = json.dumps({
            "c": ex.code,
            "tag": ex.tag,
            "msg": ex.msg,
        })


class ShortLinkResource(object):

    def on_get(self, req, resp, tag):
        url = self.get_tag(tag)
        if url is None:
            # 不存在的链接，跳转到index页面
            url = self.get_tag("index")
            logging.warn("tag: %s is empty", tag)

        url = urllib.unquote_plus(url)
        # raise falcon.HTTPMovedPermanently(url)
        raise falcon.HTTPFound(url)

    def on_post(self, req, resp, tag):
        body = req.stream.read().strip()
        if not body:
            raise ShortLinkError("-1", tag, "Request body should not be empty.")
        if not validators.url(body):
            raise ShortLinkError("-2", tag, "Url is invalid, e.g: http://www.google.com.hk")

        url = urllib.quote_plus(body)
        if tag == "":
            # 未指定 tag，随机生成
            tag = self.transform_url(url)
        else:
            # 指定 tag，判断是否合法可用
            if self.get_tag(tag):
                raise ShortLinkError(-3, tag, "Tag has been used.")
            if len(tag) > 16:
                raise ShortLinkError(-4, tag, "Tag length should less then 16 byte.")
            self.save_tag(tag, url)

        resp.status = falcon.HTTP_200
        resp.body = json.dumps({"c": 0, "tag": tag, "msg": "ok"})

    @rds_cache
    def get_tag(self, tag):
        d = db.get("SELECT `url` FROM `urls` WHERE `tag` = %s", tag)
        return d["url"] if d else None

    def transform_url(self, url):
        tag = rds.get(url_key(url))
        if tag is None:
            tag = self.generate_tag()
            self.save_tag(tag, url)

        return tag

    def generate_tag(self):
        while True:
            tag = self.rand_str()
            if self.get_tag(tag) is None:
                break

        return tag

    def rand_str(self):
        result = ""
        for i in range(8):
            result += chars[random.randint(0, 61)]

        return result

    def save_tag(self, tag, url):
        db.execute("INSERT INTO `urls`(`tag`, `url`)VALUES(%s, %s)", tag, url)
        rds.setex(url_key(url), 86400, tag)


app = falcon.API()
app.add_route("/{tag}", ShortLinkResource())
app.add_error_handler(ShortLinkError)


if __name__ == "__main__":
    host, port = config.bind.split(":")
    httpd = simple_server.make_server(host, int(port), app)
    httpd.serve_forever()
