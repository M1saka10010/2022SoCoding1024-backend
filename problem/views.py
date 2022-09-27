import json

from django.shortcuts import HttpResponse
from django.utils import timezone

from config.models import Site
from user.models import User
from . import models


# Create your views here.


def lister(request):
    if request.method == 'POST':
        if request.POST.get('uuid', None):
            uuid = request.POST.get('uuid', None)
            user = User.objects.filter(uuid=uuid)
            if user.exists():
                problems = models.Problem.objects.all()
                res = {'code': 0, 'problems': []}
                for problem in problems:
                    if problem.is_display:
                        is_pass = models.CorrectLog.objects.filter(problem_id=problem.id, user_id=user[0].id).exists()
                        res['problems'].append(
                            {'problem_id': problem.id, 'template': problem.template, 'problem_title': problem.title,
                             'pass_count': problem.pass_count, 'is_pass': is_pass})
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


def detail(request):
    if request.method == 'POST':
        if request.POST.get('uuid', None) and request.POST.get('problem_id', None):
            uuid = request.POST.get('uuid', None)
            problem_id = request.POST.get('problem_id', None)
            user = User.objects.filter(uuid=uuid)
            if user.exists():
                problem = models.Problem.objects.filter(id=problem_id)
                if problem.exists():
                    is_pass = models.CorrectLog.objects.filter(problem_id=problem_id, user_id=user[0].id).exists()
                    res = {'code': 0, 'problem_id': problem[0].id, 'template': problem[0].template,
                           'title': problem[0].title,
                           'description': problem[0].description, 'tips': problem[0].tips,
                           'pass_count': problem[0].pass_count, 'is_pass': is_pass}
                    res = json.dumps(res, ensure_ascii=False)
                    return HttpResponse(res)
                else:
                    res = {'code': 500, 'message': '题目不存在'}
                    res = json.dumps(res, ensure_ascii=False)
                    return HttpResponse(res)
            else:
                res = {'code': 500, 'message': '用户不存在'}
                res = json.dumps(res, ensure_ascii=False)
                return HttpResponse(res)
        else:
            res = {'code': 500, 'message': 'uuid或problem_id不能为空'}
            res = json.dumps(res, ensure_ascii=False)
            return HttpResponse(res)
    else:
        res = {'code': 500, 'message': '请求方式错误'}
        res = json.dumps(res, ensure_ascii=False)
        return HttpResponse(res)


def submit(request):
    if request.method == 'POST':
        # 比赛结束后不再接受提交
        if Site.objects.filter(key='end_time').exists() and int(
                Site.objects.filter(key='end_time')[0].value) < timezone.now().timestamp():
            res = {'code': 500, 'message': '比赛已结束'}
            res = json.dumps(res, ensure_ascii=False)
            return HttpResponse(res)
        if request.POST.get('uuid', None) and request.POST.get('problem_id', None) and request.POST.get('answer', None):
            uuid = request.POST.get('uuid', None)
            problem_id = request.POST.get('problem_id', None)
            answer = request.POST.get('answer', None)
            if len(answer) > 100:
                res = {'code': 500, 'message': '答案过长'}
                res = json.dumps(res, ensure_ascii=False)
                return HttpResponse(res)
            user = User.objects.filter(uuid=uuid)
            if user.exists():
                if user[0].is_updated:
                    problem = models.Problem.objects.filter(id=problem_id)
                    if problem.exists():
                        if timezone.now().timestamp() - user[0].last_submitted.timestamp() < 2:
                            res = {'code': 500, 'message': '提交过于频繁'}
                            res = json.dumps(res, ensure_ascii=False)
                            return HttpResponse(res)
                        if problem[0].solution == answer:
                            models.Solution.objects.create(problem_id=problem_id, user_id=user[0].id, answer=answer,
                                                           is_correct=True)
                            solution = models.Solution.objects.filter(problem_id=problem_id, user_id=user[0].id,
                                                                      answer=answer)
                            if solution.count() <= 1:
                                models.CorrectLog.objects.create(problem_id=problem_id, user_id=user[0].id,
                                                                 solution_id=solution[0].id,
                                                                 attempt_times=models.Solution.objects.filter(
                                                                     problem_id=problem_id, user_id=user[0].id).count())
                            user.update(last_submitted=timezone.now())
                            res = {'code': 0, 'message': '答案正确'}
                            res = json.dumps(res, ensure_ascii=False)
                            return HttpResponse(res)
                        else:
                            models.Solution.objects.create(problem_id=problem_id, user_id=user[0].id, answer=answer,
                                                           is_correct=False)
                            user.update(last_submitted=timezone.now())
                            res = {'code': 0, 'message': '答案错误'}
                            res = json.dumps(res, ensure_ascii=False)
                            return HttpResponse(res)
                    else:
                        res = {'code': 500, 'message': '题目不存在'}
                        res = json.dumps(res, ensure_ascii=False)
                        return HttpResponse(res)
                else:
                    res = {'code': 500, 'message': '用户未完善信息'}
                    res = json.dumps(res, ensure_ascii=False)
                    return HttpResponse(res)
            else:
                res = {'code': 500, 'message': '用户不存在'}
                res = json.dumps(res, ensure_ascii=False)
                return HttpResponse(res)
        else:
            res = {'code': 500, 'message': 'uuid或problem_id或answer不能为空'}
            res = json.dumps(res, ensure_ascii=False)
            return HttpResponse(res)
    else:
        res = {'code': 500, 'message': '请求方式错误'}
        res = json.dumps(res, ensure_ascii=False)
        return HttpResponse(res)
