import pymysql

# 连接MYSQL数据库
db = pymysql.connect(host="localhost", user="root",
                     passwd="wstc9093", db="comment")
cursor = db.cursor()


def create_table():
    '''在数据库建表，加字段'''
    sql = '''CREATE TABLE IF NOT EXISTS `comments`(
        comment_content text(5000),
        emotion int
    );'''
    cursor.execute(sql)
    return


def save_data(data_dict):
    '''存储爬取到的数据'''
    sql = '''INSERT INTO comments(comment_content) VALUES(%s)'''
    value_tup = (data_dict['comment_content'])

    try:
        cursor.execute(sql, value_tup)
        db.commit()
    except:
        print('数据库写入失败')
    return


def close_sql():
    '''关闭数据库'''
    db.close()
