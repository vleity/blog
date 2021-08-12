### 第一个flask程序
```python
from flask import Flask

# 创建Flask类对象
app = Flask(__name__)

# 定义url与视图函数映射关系
@app.route('/')
def hello_world():
    return 'Hello World!'


# 启动网站
if __name__ == '__main__':
    app.run()
```

### 开启DEBUG模式

方法一：在`app.run()`中传递一个参数
```python
if __name__ == '__main__':
    app.run(debug=True)
```

方法二：设置app对象的debug属性
```python
app.debug = True
```

方法三：通过配置参数
```python
app.config.update(DEBUG=True)
```

方法四：使用config.py文件

config.py
```python
DEBUG = True
```
app.py
```python
import config
app.config.from_object(config)
```

### 配置文件的两种方式
1、使用`app.config.from_object(config)`加载配置文件

2、使用`app.config.from_pyfile('config.py',silent=False)`加载配置文件，silent默认False，如果文件路径错误，则会报错，设置`silent=True`，如果文件路径错误，则跳过加载，不会报错

### url两种传参方式
1、传递参数的语法是：`/<参数名>/`。然后在视图中定义同名的参数
```python
@app.route('/<id>/')
def hello_world(id):
    return id
```

限制参数的类型，参数的类型有：
- string：默认的参数类型，接受没有斜杠的文本
- int：整形
```python
# http://127.0.0.1:5000/111
@app.route('/<int:id>/')
def hello_world(id):
    return str(id)
```

- float：浮点类型
```python
# http://127.0.0.1:5000/1.0/
@app.route('/<float:id>/')
def hello_world(id):
    return str(id)
```

- path：和string类型类似，但是接受斜杠
```python
# http://127.0.0.1:5000/1.0/sss/dsasd/
@app.route('/<path:id>/')
def hello_world(id):
    return str(id)
```

- uuid：uuid字符串

```python
# http://127.0.0.1:5000/ea5a0b09-62cb-4d14-afd6-4e6ea7bf702f/
@app.route('/<uuid:id>/')
def hello_world(id):
    return str(id)
```

- any：可以指定多种路径

```python
# http://127.0.0.1:5000/user/123/
# http://127.0.0.1:5000/blog/123/
@app.route('/<any(user,blog):url_path>/<id>/')
def hello_world(url_path,id):
    return str(url_path+'/'+id)
```

2、通过问号(?)的形式传参
```python
from flask import Flask,request

# http://127.0.0.1:5000/?wd=python
@app.route('/')
def hello_world():
    wd = request.args.get('wd')
    return wd
```

3、如果页面想做seo的话，推荐使用第一种

### url_for使用

```python
from flask import Flask, url_for

@app.route('/')
def hello_world():
    return url_for('my_list')   # /list/

@app.route('/list/')
def my_list():
    return "my_list!"
```

```python
@app.route('/')
def hello_world():
    return url_for('my_list')   # /list/2/

@app.route('/list/<page>/')
def my_list(page):
    return "my_list!"
```

### 自定义参数类型
1、使用正则表达式
```python
from werkzeug.routing import BaseConverter

# 定义一个手机号码的参数类型
class TelephoneConveter(BaseConverter):
    regex = r'1[345678]\d{9}'

app.url_map.converters['tel'] = TelephoneConveter

@app.route('/<tel:id>/')
def hello_world(id):
    return id
```

2、使用`to_python`函数,函数返回值将会传递到view函数中作为参数
```python
from werkzeug.routing import BaseConverter

# 定义一个可转化为列表的参数类型  A+B  -->  ['A','B']
class ListConveter(BaseConverter):

    # 返回值将直接传给视图函数作为参数值
    def to_python(self, value):
        print(type(value))
        return value.split('+')

app.url_map.converters['list'] = ListConveter

@app.route('/list/<list:id>/')
def list(id):
    return "列表是  %s" %id
```

3、使用`to_url`函数，函数返回值将会在调用`url_for`函数的时候生成符合要求的url形式
```python
from werkzeug.routing import BaseConverter

# 定义一个可转化为列表的参数类型  A+B  -->  ['A','B']
class ListConveter(BaseConverter):

    # 返回值将直接传给视图函数作为参数值
    def to_python(self, value):
        print(type(value))
        return value.split('+')
    
        def to_url(self, value):
        return '+'.join(value)

    
app.url_map.converters['list'] = ListConveter

@app.route('/')
def hello_world():
    return url_for('list',id=['A', 'B'])  # /list/A+B/

@app.route('/list/<list:id>/')
def list(id):
    return "列表是  %s" %id
```

### 让其他电脑访问我的flask项目
```python
if __name__ == '__main__':
    app.run(host='0.0.0.0')
```

### 指定端口号
flask默认使用5000端口
```python
if __name__ == '__main__':
    app.run(port=8000)
```

### GET和POST请求
请求方式有：POST, GET, DELETE, PUT等

1、`GET`请求，只会在服务器上获取资源，不会改变服务器的状态，推荐使用

2、`POST`请求，会给服务器提交一些数据或文件时推荐使用

```python 
@app.route('/m/',methods=['POST','GET'])
def method():
    return "hello world"
```

### 重定向 redirect
```python
from flask import Flask, url_for, redirect, request

app = Flask(__name__)
app.config.from_pyfile('config.py', silent=True)


@app.route('/login/', endpoint='login')
def login():
    return "login page"


@app.route('/profile/', endpoint='profile')
def profile():
    if request.args.get('name'):
        return '个人中心页面'
    else:
        # 重定向到登录页面
        return redirect(url_for('login'), code=302)


if __name__ == '__main__':
    app.run()
```

### 视图函数Response返回值
视图函数的返回值会被自动转化为一个相应对象，Flask转换逻辑如下：

- 如果返回的是一个合法的响应对象，则直接返回。
- 如果返回的是一个字符串，那么Flask会重新创建一个`werkzeug.wrappers.Response`对象，`Response`将该字符串作为主体，状态码为200，`MIME`为`text/html`，然后返回该`Response`对象。

```python
@app.route('/')
def hello_world():
    # return 'hello world'
    return Response(response='hello world',status=200,mimetype='text/html')
```

- 如果返回的是一个元组，元组中的数据类型是(response，status，headers)，status值会覆盖默认的200状态码，headers可以是一个列表或字典，作为额外的消息头。
- 如果以上条件都不满足，flask会假设返回的是一个合法的`WISG`应用程序，并通过`Response.fore_type(rv,request,environ)`转换为一个请求对象。

```python
from flask import Flask, Response, jsonify

app = Flask(__name__)
app.config.from_pyfile('config.py', silent=True)


# 将视图函数中返回的字典，转换成json对象，然会返回
class JSONResponse(Response):

    @classmethod
    def force_type(cls,response,environ=None):
        """
        这个方法只有视图函数返回非字符，非元组，非Response对象才会调用
        """
        if isinstance(response,dict):
            response = jsonify(response)
            return super(JSONResponse,cls).force_type(response,environ)


app.response_class = JSONResponse


@app.route('/')
def hello_world():
    return {'name':'Tom','age':20}


if __name__ == '__main__':
    app.run()

```



### 模板渲染
index.html
```html
<!DOCTYPE html>
<html lang="en">
<head>
    <meta charset="UTF-8">
    <title>首页</title>
</head>
<body>
    <h1>首页</h1>
</body>
</html>
```

渲染模板
```python
from flask import Flask, render_template


app = Flask(__name__)
app.config.from_pyfile('config.py', silent=True)


@app.route('/')
def index():
    return render_template('index.html')


if __name__ == '__main__':
    app.run()

```

### 模板传参
1、直接传参
```python
@app.route('/')
def index():
    return render_template('index.html',username='Tom',age=20)
```
```html
<!DOCTYPE html>
<html lang="en">
<head>
    <meta charset="UTF-8">
    <title>首页</title>
</head>
<body>
    <h1>这是从模板中渲染的数据</h1>
    <p>{{ username }}</p>
    <p>{{ age }}</p>
</body>
</html>
```


2、使用字典
```python
@app.route('/')
def index():
    context = {
        "username":"Tom",
        "age":20,
    }
    return render_template('index.html',context=context)
```
```html
<!DOCTYPE html>
<html lang="en">
<head>
    <meta charset="UTF-8">
    <title>首页</title>
</head>
<body>
    <h1>这是从模板中渲染的数据</h1>
    <p>{{ context.username }}</p>
    <p>{{ context.age }}</p>
</body>
</html>
```

3、使用关键字参数
```python
@app.route('/')
def index():
    context = {
        "username":"Tom",
        "age":20,
    }
    return render_template('index.html',**context)
```
```html
<!DOCTYPE html>
<html lang="en">
<head>
    <meta charset="UTF-8">
    <title>首页</title>
</head>
<body>
    <h1>这是从模板中渲染的数据</h1>
    <p>{{ username }}</p>
    <p>{{ age }}</p>
</body>
</html>
```

### 模板中使用url_for

```python
from flask import Flask, render_template

app = Flask(__name__)

@app.route('/',endpoint='index')
def index():
    return render_template('index.html')


@app.route('/login/',endpoint='login')
def login():
    return render_template('login.html')

if __name__ == '__main__':
    app.run(debug=True)
```
index.html,可以传递参数
```html
<a href="{{ url_for('login',ref='/') }}">登录</a>
```


### Jinja2模板过滤器

`abs`绝对值过滤器
```python
@app.route('/',endpoint='index')
def index():
    return render_template('index.html',position=-10)
```
```html
<p>绝对值是：{{ position|abs }}</p>
```

`default`默认值过滤器

没有传参数的默认值
```html
<p>值是：{{ position|default(0) }}</p>
```

传递的参数值为 position=None 或 空字符串，空列表，空字典。等价于 `position or 0`
```html
<p>值是：{{ position|default(0,boolean=True) }}</p>  {# 值是：0 #}
<p>值是：{{ position|default(0,boolean=False) }}</p>  {# 值是：None #}
```

### 自定义时间处理过滤器

```python
from flask import Flask, render_template
from datetime import datetime


app = Flask(__name__)


@app.template_filter('handle_time')
def handle_time(time):
    """
    time 距离现在的时间
    1、如果时间间隔小于1分钟，则显示“刚刚”
    2、如果时间间隔大于1分钟小于1小时，则显示“xx分钟前”
    3、如果时间间隔大于1小时小于24小时，则显示“xx小时前”
    4、如果时间间隔大于24小时小于30天，则显示“xx天前”
    5、否则显示具体时间
    """
    if isinstance(time, datetime):
        now = datetime.now()
        timestamp = (now - time).total_seconds()    # 获取秒数
        if timestamp < 60:
            return "刚刚"
        elif 60 <= timestamp < 60*60:
            minutes = timestamp / 60
            return "%s分钟前" % int(minutes)
        elif 60*60 <= timestamp < 60*60*24:
            hours = timestamp / (60*60)
            return "%s小时前" % int(hours)
        elif 60*60*24 <= timestamp < 60*60*24*30:
            days = timestamp / (60*60*24)
            return "%s天前" % int(days)
        else:
            return time.strftime('%Y-%m-%d %H:%M:%S')
    else:
        return time


@app.route('/', endpoint='index')
def index():
    context = {
        "create_time" : datetime(2020,2,13,16,0,0)
    }
    return render_template('index.html', **context)


@app.route('/login/',endpoint='login')
def login():
    return render_template('login.html')

if __name__ == '__main__':
    app.run(debug=True)
```
```html
<p>发表时间：{{ create_time|handle_time}}</p>
```


### 模板中使用if语句
```html
{% if 1==2 %}
    <h1>if</h1>
{% elif 1==1 %}
    <h1>elseif</h1>
{% else %}
    <h1>else</h1>
{% endif %}
```

### 模板中使用for循环
```python
@app.route('/', endpoint='index')
def index():
    context = {
        "create_time" : datetime(2020,2,13,16,0,0),
        "books":[
            {
                "name":"三国演义",
                "author":"罗贯中",
                "price":109.00
            },
            {
                "name": "水浒传",
                "author": "施耐庵",
                "price": 119.00
            },
            {
                "name": "西游记",
                "author": "吴承恩",
                "price": 129.00
            },
            {
                "name": "红楼梦",
                "author": "曹雪芹",
                "price": 139.00
            },
        ]
    }
    return render_template('index.html', **context)
```

```html
<table border="1px">
    <tr>
        <th>序号</th>
        <th>书名</th>
        <th>作者</th>
        <th>价格</th>
    </tr>
    {% for book in books %}
    <tr>
        <td>{{loop.index}}</td>
        <td>{{book.name}}</td>
        <td>{{book.author}}</td>
        <td>{{book.price}}</td>
    </tr>
    {% endfor %}
</table>
```

### 打印九九乘法表
```html
<table border="1px">
    {% for i in range(1,10) %}
    <tr>
        {% for j in range(1,i + 1) %}
        <td>{{ j }} x {{ i }} = {{ i*j }}</td>
        {% endfor %}
    </tr>
    {% endfor %}
</table>
```


















