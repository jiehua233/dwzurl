#!/usr/bin/env python
# -*- coding: utf-8 -*-

mysql = {
    "host": "127.0.0.1:3306",
    "user": "root",
    "password": "root",
    "database": "shortlink",
}

redis = {
    "host": "127.0.0.1",
    "port": 6379,
    "db": 3,
}

rds_prefix = "link:"


"""Gunicorn setting"""
bind = "127.0.0.1:28004"
workers = 1
worker_class = "gevent"
accesslog = "-"     # log to stderr
errorlog = "-"      # log to stderr
loglevel = "info"
