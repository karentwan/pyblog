from flask import Flask
from flask import request
from flask import render_template, session, redirect,url_for
from flask import send_file
import json
import db,util
'''
网站的入口，所有的url都将转到这里面
如果要使用模板，那么这个python文件和templates目录需要
存在同一级目录下面
'''
app = Flask(__name__)
#使用session需要这个秘钥
app.secret_key = '123456'
# 首页
@app.route('/index', methods=['GET'])
def getIndex():
    sql = 'select a.title, a.time, u.username, c.catename, a.id ' \
          'from article as a left join user as u on a.autorid = u.id left join ' \
          'category as c on a.categoryid = c.id;'
    values = db.select(sql)
    user = session.get('user')
    username = None
    if user:
        username=user['username']
        print('username:%s'%(username))
    print(values)

    return render_template("index.html", articles=values)

'''
获取文章列表
'''
@app.route('/list', methods=['GET'])
def list():
    sql = 'select a.id, a.title, a.time, u.username, c.catename, a.great, a.brief, a.subcategory ' \
          'from article as a left join user as u ' \
          'on a.autorid = u.id left join category as c on a.categoryid = c.id';
    values = db.select(sql)
    print(values)
    return render_template("list.html", list=values)

# 登录注册界面
@app.route('/loginview', methods=['GET'])
def loginview():
    return render_template('login.html')


@app.route('/registerview', methods=['GET'])
def registerview():
    return render_template('register.html')

@app.route('/hasUser', methods=['POST'])
def hasUser():
    # post请求需要使用下面这种方式取值
    username = request.form.get('username')
    sql = "select id from user where username=%s"
    value = db.findOneByCondition(sql, username)
    print(value)
    print(username)
    if value:
        return json.dumps({'code': 200})
    return json.dumps({'code': 201})


@app.route('/login', methods=['POST'])
def login():
    username = request.form.get('username')
    password = request.form.get('password')
    # 查数据库
    sql = 'select id, username, password from user where username=%s'
    print(sql)
    value = db.findOneByCondition(sql, username)
    # 如果查不到
    if not value:
        # 不能使用/static/fail.html,要使用下面的形式
        return send_file('static/fail.html')
    if util.cmp_password(password, value[2]):
        # 存cookie
        obj = {'userid':value[0], 'username':value[1]}
        session['user'] = obj
        print('username:%s'%(value[1]))
        return redirect('/index')
    return send_file('static/fail.html')

@app.route('/logout')
def logout():
    session.clear()
    return redirect('/index')

@app.route('/comment', methods=["POST"])
def comment():
    user = session.get('user')
    if not user:
        return redirect("/loginview")
    content = request.form.get("comment")
    articleId = request.form.get("articleId")
    pid = request.form.get('pid')
    if not pid:
        pid = 0
    uid = user['userid']
    print("uid, articleId, content", (uid, articleId, content, pid))
    sql = "insert into comment values(null, %s, %s, %s, %s)"
    count = db.insert(sql, content, pid, articleId, uid)
    print("cout:%s"%(count))
    if count > 0:
        return send_file('static/success.html')
    return send_file('static/fail.html')

@app.route('/register', methods=['POST'])
def register():
    username = request.form.get('username')
    password = request.form.get('password')
    if not username or not password:
        return send_file('static/fail.html')
    encode = util.MD5(password)
    sql = "insert into user values(null, %s, %s)"
    count = db.insert(sql, username, encode)
    if count > 0:
        return send_file('static/success.html')
    return send_file('static/fail.html')


# 内容详情
@app.route('/detail', methods=['GET'])
def detail():
    id = request.args.get('id')
    # python字符串格式化输出
    # sql = 'select a.title, a.content from article as a where id={id}'.format(id=id)
    sql = "select a.title, a.content, c.catename " \
          "from article as a left join category as c on a.categoryid = c.id where a.id = {id}".format(id=id)
    print('sql:%s'%(sql))
    values = db.findone(sql)
    print(values)
    # 查评论
    sql = "select c.pid, c.articleid, u.username, c.content " \
          "from comment as c left join user as u on c.authorid=u.id where articleid=%s"

    comments = db.findByCondition(sql, id)
    return render_template('content.html', id=id, content=values, comments=comments)


if __name__ == '__main__':
    app.run()