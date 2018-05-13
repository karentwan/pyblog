from flask import Flask
from flask import request
from flask import render_template, session, redirect,url_for
from flask import send_file
import functools
import json
import db,util
import time
'''
网站的入口，所有的url都将转到这里面
如果要使用模板，那么这个python文件和templates目录需要
存在同一级目录下面
'''
app = Flask(__name__)
#使用session需要这个秘钥
app.secret_key = '123456'

'''
验证用户是否登录
'''
def verify(func):
    @functools.wraps(func)
    def wrapper(*args, **kw):
        user = session.get('user')
        if not user:
            return redirect('/loginview')
        print(args, kw)
        return func(*args, **kw)
    return wrapper

'''
api格式的验证，返回的是json数据，而不是
跳转到登陆页面
'''
def apiVerify(func):
    @functools.wraps(func)
    def wrapper(*args, **kw):
        user = session.get('user')
        if not user:
            return json.dumps({'code': 201, 'content':'用户未登陆'})
        return func(*args, **kw)
    return wrapper


# 首页
@app.route('/index', methods=['GET'])
def getIndex():
    sql = 'select a.title, a.time, u.username, c.catename, a.id ' \
          'from article as a left join user as u on a.autorid = u.id left join ' \
          'category as c on a.categoryid = c.id;'
    values = db.findByCondition(sql)
    user = session.get('user')
    username = None
    if user:
        username=user['username']
        print('username:%s'%(username))
    # print(values)
    return render_template("index.html", articles=values)


'''
获取文章列表
'''
@app.route('/list', methods=['GET'])
def listArticle():
    sql = 'select a.id, a.title, a.time, u.username, c.catename, a.great, a.brief, a.subcategory ' \
          'from article as a left join user as u ' \
          'on a.autorid = u.id left join category as c on a.categoryid = c.id';
    values = db.findByCondition(sql)
    # print(values)
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
    if util.cmp_password(password, value['password']):
        # 存cookie
        obj = {'userid':value['id'], 'username':value['username']}
        session['user'] = obj
        print('username:%s'%(value['username']))
        return redirect('/index')
    return send_file('static/fail.html')

@app.route('/logout')
def logout():
    session.clear()
    return redirect('/index')

@app.route('/comment', methods=["POST"])
@verify
def comment():
    user = session.get('user')
    content = request.form.get("comment")
    articleId = request.form.get("articleId")
    pid = request.form.get('pid')
    if not pid:
        pid = 0
    uid = user['userid']
    print("uid, articleId, content", (uid, int(articleId), content, int(pid)))
    # python的数据库操作全用%s占位，用其他的会报错
    sql = "insert into comment values(null, %s, %s, %s, %s, %s)"
    # 生成时间戳
    t = time.time()
    count = db.insert(sql, content, pid, articleId, uid, t)
    print("cout:%s"%(count))
    if count > 0:
        return redirect('/detail?id=' + articleId)
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
        return redirect('/index')
    return send_file('static/fail.html')

# 点赞
@app.route('/great', methods=['GET'])
@apiVerify
def great():
    user = session.get('user')
    uid = user['userid']
    #get方法使用这个函数获取参数，post函数使用request.form.get()获取参数
    articleId = request.args.get('id')
    print("点赞函数开始执行-----：%s"%(articleId))
    sql = "update article set great = great + 1 where id = %s"
    count = db.insert(sql, articleId)
    print("点赞", count)
    if count > 0:
        return json.dumps({'code': 200})
    return json.dumps({'code': 202})

@app.route('/getUserComment', methods=['POST'])
def getUserComment():
    # 获取文章id
    articleId = request.form.get('articleId')
    # 查评论
    sql = "select c.id, c.pid, u.username, c.content " \
          "from comment as c left join user as u on c.authorid=u.id where articleid=%s order by c.time desc"
    comments = db.findByCondition(sql, articleId)
    print(comments)
    ret = dataTreeForComment(comments)
    print("ret:%s" % (ret))
    return json.dumps(ret)

# 内容详情
@app.route('/detail', methods=['GET'])
def detail():
    id = request.args.get('id')
    # python字符串格式化输出
    # sql = 'select a.title, a.content from article as a where id={id}'.format(id=id)
    sql = "select a.title, a.content, c.catename " \
          "from article as a left join category as c on a.categoryid = c.id where a.id = {id}".format(id=id)
    print('sql:%s'%(sql))
    values = db.findOneByCondition(sql)
    print(values)

    return render_template('content.html', id=id, content=values)

'''
为评论创建评论树
'''
def dataTreeForComment(comments):
    # 待返回的结果
    ret = []
    temp = dict()
    for comment in comments:
        comment['children'] = []
        # print(t)
        temp[comment['id']] = comment
    for comment in comments:
        # 返回父元素的所在的行
        item = temp.get(comment['pid'])
        if not item:
            ret.append(comment)
        else:
            print(item)
            item['children'].append(comment)
    return ret

if __name__ == '__main__':
    app.run()