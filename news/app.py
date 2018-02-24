#-*- coding=UTF-8 -*-
from flask import render_template
from flask import abort
from flask import Flask
# tiaozhan 2

from datetime import datetime
from flask import Flask,render_template 
from flask_sqlalchemy import SQLAlchemy 


app=Flask(__name__)

app.config.update(dict(
    SQLALCHEMY_DATABASE_URI='mysql://root@localhost/zpz'
    ))
db=SQLAlchemy(app)

## 文章 表 包含的数据 
class File(db.Model):
    __tablename__='files'

    id=db.Column(db.Integer,primary_key=True)    # key=true ?? 
    title=db.Column(db.String(80),unique=True)
    created_time=db.Column(db.DateTime)
    category_id=db.Column(db.Integer,db.Foreignkey('categories.id'))
    category = db.relationship('Category',uselist=False)
    content=db.Column(db.Text)

    def __init__(self,title,created_time,category,content):
        self.title=title
        self.created_time=created_time
        self.category=category
        self.content=content 


##  类别 表包含的数据
class Category(db.Model):
    __tablename__='categories'

    id=db.Column(db.Integer,primary_key=True)
    name=db.Column(db.String(80))
    files=db.relationship('File')

    def __init__(self,name):
        self.name=name

#添加测试数据 
def insert_datas():
    java=Category('Java')
    python=Category('Python')
    file1=File('Hello java',datetime.utcnow(),java,'File Content - Java is cool')
    file2=File('Hello python', datetime.utcnow(),python,'File Content - pyhton is cool !')
    db.session.add(java)
    db.session.add(python)
    db.session.add(file1)
    db.session.add(file2)
    db.session.commit()


#路由实现

@app.route('/')
def index():
    #show title name's table 
    return render_template('index.html',files=File.query.all())

@app.route('/files/<int:file_id>')
def file(file_id):
    # read and show 'filename.json'  内容
    file_item=File.query.get_or_404(file_id)
    return render_tempalte('file.html',file_item=file_item)

@app.errorhandler(404)
def not_found(error):
    return render_template('404.html'),404

if __name__=='__main__':
    app.debug=True
    app.run(port=3000)







