# This is a sample Python script.

# Press ⌃R to execute it or replace it with your code.
# Press Double ⇧ to search everywhere for classes, files, tool windows, actions, and settings.

import requests
from bs4 import BeautifulSoup
import sqlhelper
import sqlite3

from lxml import etree
import urllib3
from xml.dom.minidom import parse
import xml.dom.minidom
import xml.etree.cElementTree as ET

dbName = 'rrys.db'
tableName = 'movielist'
header = {
    'User-Agent': 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/92.0.4515.159 Safari/537.36',
    'Content-Type': 'text/html;charset=utf-8',
    'Accept-Language': 'zh-CN;q=0.9',
    'Content-Encoding': 'gzip',
    'Cookie': "37cs_user=37cs81473663543; 37cs_pidx=2; UM_distinctid=17bb8f7eda17f9-070c097d6d63da-35667c03-13c680-17bb8f7eda2e01; CNZZDATA1260535040=1459794415-1630890673-https%3A%2F%2Fwww.google.com.hk%2F|1630890673; 37cs_show=253,75; cscpvrich5041_fidx=2"}
firstHost = 'https://www.dydytt.net/html/gndy/dyzz/index.html'
beforeTitle = 'https://www.dydytt.net'


def findNamePages() -> None:
    r = requests.get(firstHost, headers=header)
    r.encoding = r.apparent_encoding
    html = r.text
    soup = BeautifulSoup(html, 'lxml')

    cur, conn = sqlhelper.dbOpen()
    for i, child in enumerate(soup.find_all('a', {'class': 'ulink'})):
        ul = beforeTitle + child['href']
        title = child.text
        inserts = '''INSERT INTO {0} VALUES('{1}','{2}','');'''.format(tableName,title, ul)
        cur.execute(inserts)

    conn.commit()
    cur.close()
    conn.close()

def findDownLoadPath():
    print("begain")
    cur, conn = sqlhelper.dbOpen()
    sql = '''SELECT Url from {0}'''.format(tableName)
    cur.execute(sql)
    values = cur.fetchall()
    for host in values:
        print(host[0])
        r = requests.get(host[0], headers=header)
        r.encoding = r.apparent_encoding
        html = r.text
        soup = BeautifulSoup(html, 'lxml')
        for i, child in enumerate(soup.find_all('a', {'target': '_blank'})):
            if 'magnet' in child['href']:
                magnet = '''UPDATE {0} set DownloadURLs = '{1}' where Url= '{2}' '''.format(tableName,child['href'],host[0])
                cur.execute(magnet)
                break

    conn.commit()
    cur.close()
    conn.close()

if __name__ == '__main__':
    # sqlhelper.creatTable(tableName)
    # findNamePages()
    findDownLoadPath()
