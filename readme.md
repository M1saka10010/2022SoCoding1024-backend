# 部署方法

建议使用Linux进行部署

## 1. 安装依赖

```
git clone https://github.com/M1saka10010/socoding1024.git
cd socoding1024
pip install -r requirements.txt
```

## 2. 配置

### 2.1 配置数据库

找到`socoding1024/settings.py`，修改数据库配置并修改`SECRET_KEY`的值以及`DEBUG`为`False`
，然后执行`python manage.py migrate`进行数据库迁移。

### 2.2 配置静态文件

修改`socoding1024/settings.py`中的`STATIC_ROOT`为静态文件的存放路径，然后执行`python manage.py collectstatic`进行静态文件收集。

### 2.3 配置管理员

执行`python manage.py createsuperuser`创建管理员账号。

### 2.4 配置网站配置

执行`python manage.py runserver`启动服务器，然后访问 `/admin/` 进行网站配置。
在后台的`网站配置`中配置网站的相关信息。
其中penalty为每次提交错误的惩罚时间，单位为秒，
start_time为比赛开始时间，格式为unix时间戳，
end_time为比赛结束时间，格式为unix时间戳，

## 3. 部署

### 3.1 部署uwsgi

修改`uwsgi.ini`中的`chdir`为项目路径，然后执行`uwsgi uwsgi.ini`启动uwsgi。

### 3.2 部署nginx

```nginx
    location ^~ /static/ {
        alias /www/wwwroot/socoding1024/socoding1024/static/;
    }

    location / {
        include     uwsgi_params;
        uwsgi_pass  127.0.0.1:52800;
        uwsgi_param UWSGI_SCRIPT /www/wwwroot/socoding1024/.wsgi;  #wsgi.py所在的目录名+.wsgi
        uwsgi_param UWSGI_CHDIR /www/wwwroot/socoding1024/; #项目路径
    }
```

把`/www/wwwroot/socoding1024/`替换为项目路径，然后重启nginx。

# API接口

方便进行二次开发

## 用户模块

### 用户注册

`/user/register`

请求方法:`post`

请求参数:`username`

返回格式:`json`

返回示例:

`{"code": 0, "uuid": "1145141919810"}`

### 用户信息

`/user/info`

请求方法:`post`

请求参数:`uuid`

返回示例:

`{"code": 0, "status": true, "username": "123", "email": "admin@baidu.com", "phone": "", "student_code": "1145141919810"}`

### 修改用户信息

`/user/update`

请求方法:`post`

请求参数:`uuid, email, phone, student_code`

返回示例:

`{"code": 0, "message": "更改成功"}`

`{"code": 500, "message": "无法多次更改"}`

## 题目模块

### 题目列表

`/problem/list`

请求方法:`post`

请求参数:`uuid`

返回示例:

`{"code": 0, "problems": [{"problem_id": 1, "template": 0, "problem_title": "111", "pass_count": 0, "is_pass": true}]}`

`{"code": 500, "message": "uuid不能为空"}`

### 题目详情

`/problem/detail`

请求方法:`post`

请求参数:`uuid, problem_id`

返回示例:

`{"code": 0, "problem_id": 1, "template": 0, "title": "111", "description": "111", "tips": "111", "pass_count": 0, "is_pass": true}`

`{"code": 500, "message": "uuid或problem_id不能为空"}`

### 答案提交

`/problem/submit`

请求方法:`post`

请求参数:`uuid, problem_id, answer`

返回示例:

`{"code": 0, "message": "答案错误"}`

`{"code": 0, "message": "答案正确"}`

`{"code": 500, "message": "uuid或problem_id或answer不能为空"}`

## 排行模块

### 榜单排名

`/rank/list`

请求方法:`get`

请求参数:无

返回示例:

`{"status": 0, "data": [{"rank": 1, "username": "123", "pass_count": 1, "pass_list": [1], "consume_time": 1663726855.738126}, {"rank": 2, "username": "1234", "pass_count": 1, "pass_list": [1], "consume_time": 1663761321.988158}]}`

### 我的排名

`/rank/my`

请求方法:`post`

请求参数:`uuid`

返回示例:

`{"status": 0, "rank": 2}`

`{"status": 500, "message": "用户不存在"}`