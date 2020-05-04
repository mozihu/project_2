from flask import Flask, jsonify, request
from flask_cors import CORS
import pymysql

# configuration
DEBUG = True

# instantiate the app
app = Flask(__name__)
app.config.from_object(__name__)

# enable CORS
CORS(app)


# sanity check route
@app.route('/', methods=['GET'])
def search_comments():
    keyword = request.args.get('keyword')
    print(keyword)

    # 连接MYSQL数据库
    db = pymysql.connect(host="localhost", user="root",
                         passwd="wstc9093", db="comment")
    cursor = db.cursor()
    sql = '''SELECT * FROM comments'''
    cursor.execute(sql)
    result = cursor.fetchall()

    sum_num = 0
    positive_num = 0
    negative_num = 0
    comments = []

    for r in result:
        if keyword in r[4]:
            sum_num += 1
            comments.append({
                'key': sum_num,
                'date': r[1],
                'comment_content': r[4],
                'emotion': r[5]
            })

            if r[5] == '正面':
                positive_num += 1
            else:
                negative_num += 1
    # print(comments)
    return jsonify({
        'sum_num': sum_num,
        'positive_num': positive_num,
        'negative_num': negative_num,
        'comments': comments
    })


if __name__ == '__main__':
    app.run()
