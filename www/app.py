from flask import Flask
from flask import request
from flask import render_template, session
from flask import send_file
import db,util
'''
网站的入口，所有的url都将转到这里面
如果要使用模板，那么这个python文件和templates目录需要
存在同一级目录下面
'''
app = Flask(__name__)

# 首页
@app.route('/index', methods=['GET'])
def getIndex():
    sql = 'select a.title, a.time, u.username, c.catename, a.id ' \
          'from article as a left join user as u on a.autorid = u.id left join ' \
          'category as c on a.categoryid = c.id;'
    values = db.select(sql)
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
        session['user'] = {'userid':id}
        return render_template('index.html', username=value[1])
    return send_file('static/fail.html')

@app.route('/register', methods=['POST'])
def register():
    username = request.form.get('username')
    password = request.form.get('password')
    ecode = util.MD5(password)
    sql = "insert into user values(null, %s, %s)"
    count = db.insert(sql, username, password)
    if count > 0:
        return send_file('static/success.html')
    return send_file('static/fail.html')


# 内容详情
@app.route('/detail', methods=['GET'])
def detail():
    id = request.args.get('id')
    # python字符串格式化输出
    sql = 'select a.title, a.content from article as a where id={id}'.format(id=id)
    print('sql:%s'%(sql))
    values = db.findone(sql)
    print(values)
    return render_template('content.html', content=values)


if __name__ == '__main__':
    app.run()