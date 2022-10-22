import json

from django.core.cache import cache
from django.shortcuts import HttpResponse

from config.models import Site
from problem.models import CorrectLog
from user.models import User


# Create your views here.


def get_rank_list():
    users = User.objects.all()
    # correct_logs = CorrectLog.objects.all()
    # 罚时
    if Site.objects.filter(key='penalty').exists():
        penalty = int(Site.objects.get(key='penalty').value)
    else:
        penalty = 0
    # 开始时间
    if Site.objects.filter(key='start_time').exists():
        start_time = float(Site.objects.get(key='start_time').value)
    else:
        start_time = 0
    rank_list = []
    for user in users:
        logs = CorrectLog.objects.filter(user_id=user.id)
        pass_count = 0
        pass_list = []
        consume_time = 0
        for log in logs:
            pass_count += 1
            pass_list.append(log.problem_id)
            consume_time += (log.submit_time.timestamp() - start_time) + penalty * (log.attempt_times - 1)
        if pass_count != 0:
            rank_list.append(
                {'id': user.id, 'pass_count': pass_count, 'consume_time': consume_time, 'username': user.username,
                 'pass_list': pass_list})
    rank_list.sort(key=lambda x: (x['pass_count'], x['consume_time']))
    return rank_list


def my_rank(request):
    if request.method == 'POST':
        if request.POST.get('uuid', None):
            uuid = request.POST.get('uuid', None)
            # 如果在缓存内，直接输出
            if cache.get(uuid):
                return HttpResponse(cache.get(uuid))
            user = User.objects.filter(uuid=uuid)
            if user.exists():
                rank_list = get_rank_list()
                rank = 0
                for i in range(len(rank_list)):
                    if user.id == rank_list[i]['id']:
                        rank = i + 1
                        break
                res = {'status': 0, 'rank': rank}
                res = json.dumps(res, ensure_ascii=False)
                cache.set(uuid, res, 30)
                return HttpResponse(res)
            else:
                res = {'status': 500, 'message': '用户不存在'}
                res = json.dumps(res, ensure_ascii=False)
                return HttpResponse(res)
        else:
            res = {'status': 500, 'message': '参数错误'}
            res = json.dumps(res, ensure_ascii=False)
            return HttpResponse(res)
    else:
        res = {'status': 500, 'message': '请求方式错误'}
        res = json.dumps(res, ensure_ascii=False)
        return HttpResponse(res)


def ranking(request):
    # 如果在缓存内，直接输出
    if cache.get('rank'):
        return HttpResponse(cache.get('rank'))
    rank_list = get_rank_list()
    rank = []
    for i in range(len(rank_list)):
        rank.append(
            {'rank': i + 1, 'username': rank_list[i]['username'], 'pass_count': rank_list[i]['pass_count'],
             'pass_list': rank_list[i]['pass_list'], 'consume_time': rank_list[i]['consume_time']})
    res = {'status': 0, 'data': rank}
    res = json.dumps(res, ensure_ascii=False)
    # 写入缓存
    cache.set('rank', res, 30)
    return HttpResponse(res)
