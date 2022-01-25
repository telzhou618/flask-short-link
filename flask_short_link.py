import random
import re
from datetime import datetime

from flask import Flask
from flask import request, abort, redirect
from flask_sqlalchemy import SQLAlchemy


# 配置
class AppConfig:
    SQLALCHEMY_DATABASE_URI = "mysql+pymysql://root:root@localhost/test"
    SQLALCHEMY_TRACK_MODIFICATIONS = False
    SQLALCHEMY_ECHO = True


app = Flask(__name__)
app.config.from_object(AppConfig())
db = SQLAlchemy(app)


# model
class ShortLink(db.Model):
    __tablename__ = 'tb_short_link'

    id = db.Column(db.Integer, primary_key=True)
    short_key = db.Column(db.String(30), unique=True, nullable=False)
    source_url = db.Column(db.String(300), nullable=False)
    created_time = db.Column(db.DateTime, nullable=False)


@app.route("/short-link/create", methods=['POST', 'GET'])
def create_short_link():
    """创建短连接"""
    SOURCE_KEYS = ['a', 'b', 'c', 'd', 'e', 'f', 'g', 'h', 'i', 'j', 'k', 'l', 'm', 'n', 'o', 'p',
                   'q', 'r', 's', 't', 'u', 'v', 'w', 'x', 'y', 'z', '0', '1', '2', '3', '4', '5',
                   '6', '7', '8', '9']
    url = request.args.get('url')
    if not url or not re.match(r'^https?:/{2}\w.+$', url):
        return {'success': False, 'message': '参数url不合法'}

    short_key = ''.join(random.sample(SOURCE_KEYS, 8))  # 数据库建了唯一索引，若重复提醒用户重试
    sl = ShortLink(short_key=short_key, source_url=url, created_time=datetime.now())
    db.session.add(sl)
    db.session.commit()
    short_full_url = 'http://localhost:9091/' + short_key  # 更换成短连接域名
    return {"id": sl.id, "short_full_url": short_full_url,
            'created_time': sl.created_time.strftime('%Y-%m-%d %H:%M:%S')}


@app.route("/<string:short_key>", methods=['GET'])
def redirect_source_url(short_key):
    """传入短连后重定向到到原链接"""
    sl = ShortLink.query.filter_by(short_key=short_key).first()
    return redirect(sl.source_url) if sl else abort(404)


if __name__ == '__main__':
    app.run(port=9091, debug=True)
