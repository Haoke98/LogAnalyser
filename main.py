# _*_ codign:utf8 _*_
"""====================================
@Author:Sadam·Sadik
@Email：1903249375@qq.com
@Date：2023/8/17
@Software: PyCharm
@disc:
======================================="""
import logging
import re
import sys
from urllib.parse import urlparse

import click
import elasticsearch
from elasticsearch import Elasticsearch
from elasticsearch.helpers import bulk

from lib import logger

PATTERN = r'''(\d{1,3}\.\d{1,3}\.\d{1,3}\.\d{1,3}) - (.*?) \[(\d{2}/\w{3}/\d{4}:\d{2}:\d{2}:\d{2} \+\d{4})\] "(\w*)\s?(.*?)\s?(HTTP/1\.0|HTTP/1\.1|HTTP/2\.0)?" (\d{3}) (\d+) "(.*?)" "(.*?)"'''
ip_count = {}
status_count = {}
top_urls = {}


def send_bulk_request(client, actions):
    try:
        resp = bulk(client, actions=actions)
        return resp
    except elasticsearch.helpers.BulkIndexError as e:
        logging.error(e)
        for err in e.errors:
            logging.error(err)
        sys.exit(1)


@click.command()
@click.option("-fp", "--file-path", prompt="请输入日志文件路径", type=str)
@click.option("-d", "--domain", prompt="请输入日志所属于的站点域名", type=str)
@click.option("--es-host", prompt="请输入ElasticSearch弹性检索引擎的访问地址（ip:port)", type=str)
@click.option("--es-username", prompt="请输入ElasticSearch弹性检索引擎的用户名", type=str)
@click.option("--es-password", prompt="请输入ElasticSearch弹性检索引擎的密码", type=str)
@click.option("--es-ca", prompt="请输入ElasticSearch弹性检索引擎的通信加密证书（路径）", type=str)
@click.option("-bs", "--batch-size", type=int, default=10000)
def main(file_path, domain, es_host, es_username, es_password, es_ca, batch_size):
    index = f"nginx-log-{domain}"
    logging.info(f"file path:[{file_path}], index:{index}")
    esClient = Elasticsearch(es_host, basic_auth=(es_username, es_password), ca_certs=es_ca, request_timeout=3600)
    isExists = esClient.indices.exists(index=index)
    max_line_num = 0
    if isExists:
        resp = esClient.search(index=index, size=0, aggs={
            "max_line_num": {
                "max": {
                    "field": "lineNum"
                }
            }
        })
        max_line_num = int(resp.body["aggregations"]["max_line_num"]["value"])
    else:
        resp = esClient.indices.create(index=index)
        logging.info(f"创建索引[{index}]成功！:{resp}")
    start_line_num = max_line_num
    with open(file_path) as f:
        f.seek(0)
        for i, line in enumerate(f):
            if i >= start_line_num - 1:
                break

        actions = []
        line_num = start_line_num
        while True:
            line_num += 1
            line = f.readline()
            if not line:
                break
            match = re.search(PATTERN, line)
            if match is None:
                print(f"异常记录：{line_num}:[{line}]")
                sys.exit(1)
            else:
                ip, RemoteUser, time, method, url, HTTP_Version, status, ResponseSize, Referer, ua = match.groups()
                result = urlparse(url)
                print(line_num, time, ip, method, HTTP_Version, result.path, result.query, status, ResponseSize,
                      RemoteUser, Referer, ua)
                if result.params != '':
                    pass
                action = {
                    "_index": index,
                    "_id": line_num,
                    "_source": {
                        "lineNum": line_num,
                        "ip": ip,
                        "time": time,
                        "method": method,
                        "HTTP_Version": HTTP_Version,
                        "path": result.path,
                        "query": result.query,
                        "status": status,
                        "ResponseSize": ResponseSize,
                        "RemoteUser": RemoteUser,
                        "UserAgent": ua,
                        "Referer": Referer
                    }
                }
                actions.append(action)
                ip_count[ip] = ip_count.get(ip, 0) + 1
                status_count[status] = status_count.get(status, 0) + 1
                top_urls[url] = top_urls.get(url, 0) + 1
            if line_num % batch_size == 0:
                # 按周期进行一次批量上传
                resp = send_bulk_request(esClient, actions)
                actions = []
        # 最后一次进行批量上传
        resp = send_bulk_request(esClient, actions)
        print('Unique IPs:', len(ip_count))
        print('Status codes:', status_count)
        print('Top URLs:', dict(sorted(top_urls.items(), key=lambda x: x[1], reverse=True)[:5]))


if __name__ == '__main__':
    logger.init("LogAnalyser")
    main()
