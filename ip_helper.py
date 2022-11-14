# _*_ codign:utf8 _*_
"""====================================
@Author:Sadam·Sadik
@Email：1903249375@qq.com
@Date：2022/11/14
@Software: PyCharm
@disc:
======================================="""
import requests
from lxml import etree


def getGeoLocation(ip):
    """
    查询IP地址对应的物理地址
    :param ip:IP地址
    :return:返回物理定位地址的汉子字符串
    """
    url = f"https://ip.tool.chinaz.com/{ip}"
    response = requests.get(url)
    response.encoding=response.apparent_encoding
    # 解码响应对象，得到页面源码
    # content = response.read().decode('utf-8')
    content = response.text
    parsed_html = etree.HTML(content)
    em = parsed_html.xpath('//span[@class="Whwtdhalf w45-0 lh45"]//em')[0]
    return em.text
    # #print(len("四川省成都市 电信"))  python 汉字算一个字节
    # #print(type(content))
    # str = content[content.find("WhwtdWrap bor-b1s col-gray03"):content.find("clearfix plr10")-87] # 大致筛选出归属地所在的字符串
    # a = str[::-1]
    # b = a[0:a.find(">")]
    # return b[::-1]


if __name__ == '__main__':
    ipAdd = input("请输入IP地址：")
    print("IP的归属地为：：" + getGeoLocation(ipAdd))