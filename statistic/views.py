# coding: utf8
from django.shortcuts import render
import datetime
from django.contrib.auth.decorators import login_required
from django.http import HttpResponse, JsonResponse
from django.shortcuts import render
from statistic.models import visitors, Statistic


def add(request):
    v = visitors(
        ip=request.META['REMOTE_ADDR'],
        date=datetime.date.today()
    )
    v.save()
    st = Statistic.objects.get(id=1)
    st.edits = True
    st.save()
    return HttpResponse("ok")


@login_required
def opensAjax(request):
    try:
        if request.POST['open']:
            vis = visitors.objects.filter(date=datetime.date.today())
            St = Statistic.objects.get(id=1)
            St.edits = False
            St.save()
            return JsonResponse({
                'visitor':vis.count()
            })
        else:
            return JsonResponse({})
    except:
        if Statistic.objects.get(id=1).edits:
            vis = visitors.objects.filter(date=datetime.date.today())
            St = Statistic.objects.get(id=1)
            St.edits = False
            St.save()
            return JsonResponse({
                'visitor':vis.count(),
            })
        else:
            return JsonResponse({})
