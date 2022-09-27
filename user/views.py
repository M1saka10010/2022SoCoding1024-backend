import json
import re
from uuid import uuid4

from django.shortcuts import HttpResponse
from django.utils import timezone

from . import models


# Create your views here.

def register(request):
    if request.method == 'POST':
        if request.POST.get('username', None):
            uuid = str(uuid4())
            username = request.POST.get('username', None)
            if len(username) > 20:
                res = {'code': 500, 'message': '用户名过长'}
                res = json.dumps(res, ensure_ascii=False)
                return HttpResponse(res)
            user = models.User.objects.filter(username=username)
            if user.exists():
                res = {'code': 500, 'message': '用户名已存在'}
                res = json.dumps(res, ensure_ascii=False)
                return HttpResponse(res)
            user.create(username=username, uuid=uuid, last_submitted=timezone.now())
            res = {'code': 0, 'uuid': uuid}
            res = json.dumps(res, ensure_ascii=False)
            return HttpResponse(res)
        else:
            res = {'code': 500, 'message': '用户名不能为空'}
            res = json.dumps(res, ensure_ascii=False)
            return HttpResponse(res)
    else:
        res = {'code': 500, 'message': '请求方式错误'}
        res = json.dumps(res, ensure_ascii=False)
        return HttpResponse(res)


def info(request):
    if request.method == 'POST':
        if request.POST.get('uuid', None):
            uuid = request.POST.get('uuid', None)
            user = models.User.objects.filter(uuid=uuid)
            if user.exists():
                res = {'code': 0, 'status': user[0].is_updated, 'username': user[0].username, 'email': user[0].email,
                       'phone': user[0].phone,
                       'student_code': user[0].student_code}
                res = json.dumps(res, ensure_ascii=False)
                return HttpResponse(res)
            else:
                res = {'code': 500, 'message': '用户不存在'}
                res = json.dumps(res, ensure_ascii=False)
                return HttpResponse(res)
        else:
            res = {'code': 500, 'message': 'uuid不能为空'}
            res = json.dumps(res, ensure_ascii=False)
            return HttpResponse(res)
    else:
        res = {'code': 500, 'message': '请求方式错误'}
        res = json.dumps(res, ensure_ascii=False)
        return HttpResponse(res)


def update(request):
    if request.method == 'POST':
        uuid = request.POST.get('uuid', None)
        # username = request.POST.get('username', None)
        email = request.POST.get('email', None)
        phone = request.POST.get('phone', None)
        student_code = request.POST.get('student_code', None)
        if uuid:
            user = models.User.objects.filter(uuid=uuid)
            if user.exists():
                if not user.get().is_updated:
                    if not email and not phone and not student_code:
                        res = {'code': 500, 'message': '至少填写一项'}
                        res = json.dumps(res, ensure_ascii=False)
                        return HttpResponse(res)
                    if email is not None:
                        if not re.match(r'^[a-zA-Z0-9_-]+@[a-zA-Z0-9_-]+(\.[a-zA-Z0-9_-]+)+$', email):
                            res = {'code': 500, 'message': '邮箱格式错误'}
                            res = json.dumps(res, ensure_ascii=False)
                            return HttpResponse(res)
                        if models.User.objects.get(email=email):
                            res = {'code': 500, 'message': '邮箱已存在'}
                            res = json.dumps(res, ensure_ascii=False)
                            return HttpResponse(res)
                    if phone is not None:
                        if len(phone) != 11:
                            res = {'code': 500, 'message': '手机号格式错误'}
                            res = json.dumps(res, ensure_ascii=False)
                            return HttpResponse(res)
                        if models.User.objects.get(phone=phone):
                            res = {'code': 500, 'message': '手机号已存在'}
                            res = json.dumps(res, ensure_ascii=False)
                            return HttpResponse(res)
                    if student_code is not None:
                        if len(student_code) > 20:
                            res = {'code': 500, 'message': '学号太长'}
                            res = json.dumps(res, ensure_ascii=False)
                            return HttpResponse(res)
                        if models.User.objects.get(student_code=student_code):
                            res = {'code': 500, 'message': '学号已存在'}
                            res = json.dumps(res, ensure_ascii=False)
                            return HttpResponse(res)
                    # user.update(username=username, email=email, phone=phone, student_code=student_code)
                    user.update(email=email, phone=phone, student_code=student_code)
                    user.update(is_updated=True)
                    res = {'code': 0, 'message': '更改成功'}
                    res = json.dumps(res, ensure_ascii=False)
                    return HttpResponse(res)
                else:
                    res = {'code': 500, 'message': '无法多次更改'}
                    res = json.dumps(res, ensure_ascii=False)
                    return HttpResponse(res)
            else:
                res = {'code': 500, 'message': '用户不存在'}
                res = json.dumps(res, ensure_ascii=False)
                return HttpResponse(res)
        else:
            res = {'code': 500, 'message': 'uuid不能为空'}
            res = json.dumps(res, ensure_ascii=False)
            return HttpResponse(res)
    else:
        res = {'code': 500, 'message': '请求方式错误'}
        res = json.dumps(res, ensure_ascii=False)
        return HttpResponse(res)
