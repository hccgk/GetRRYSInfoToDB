import sqlite3


dbName = 'rrys.db'


def creatTable(tableName):
    conn = sqlite3.connect(dbName)
    cur = conn.cursor()
    sqll = '''CREATE TABLE IF NOT EXISTS {0} (Title TEXT,Url TEXT,DownloadURLs TEXT);'''.format(tableName)
    cur.execute(sqll)
    conn.commit()
    cur.close()
    conn.close()


def executeSql(sql):
    conn = sqlite3.connect(dbName)
    cur = conn.cursor()
    cur.execute(sql)
    conn.commit()
    cur.close()
    conn.close()

def dbOpen():
    conn = sqlite3.connect(dbName)
    cur = conn.cursor()
    return  cur,conn

