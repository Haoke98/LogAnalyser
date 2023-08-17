# _*_ codign:utf8 _*_
"""====================================
@Author:Sadam·Sadik
@Email：1903249375@qq.com
@Date：2023/8/17
@Software: PyCharm
@disc:
======================================="""
import re
import sys

log_file = '/Users/shadikesadamu/Downloads/www.1.ink.log'

pattern = r'''(\d{1,3}\.\d{1,3}\.\d{1,3}\.\d{1,3}) - (.*?) \[(\d{2}/\w{3}/\d{4}:\d{2}:\d{2}:\d{2} \+\d{4})\] "(\w*)\s?(.*?)" (\d{3}) (\d+) "(.*?)" "(.*?)"'''
ip_count = {}
status_count = {}
top_urls = {}
if __name__ == '__main__':
    with open(log_file) as f:
        for i, line in enumerate(f):
            match = re.search(pattern, line)
            if match is None:
                print(f"异常记录：[{line}]")
                sys.exit(1)
            else:
                ip, tel, time, method, url, status, bytes, unknown, ua = match.groups()
                print(i, time, ip, method, url, status, bytes, tel, unknown, ua)
                ip_count[ip] = ip_count.get(ip, 0) + 1
                status_count[status] = status_count.get(status, 0) + 1
                top_urls[url] = top_urls.get(url, 0) + 1

    print('Unique IPs:', len(ip_count))
    print('Status codes:', status_count)
    print('Top URLs:', dict(sorted(top_urls.items(), key=lambda x: x[1], reverse=True)[:5]))
