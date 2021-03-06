#coding:utf-8
from __future__ import unicode_literals
from django.shortcuts import render
from ywmodels.models import Websniff
from django.contrib.auth.decorators import login_required
from django.core.paginator import Paginator, EmptyPage, PageNotAnInteger
import math

# Create your views here.

@login_required
def web(request, pk):
    stat_code = ['200', '201', '202', '203', '204', '205', '206','301', '302', '303', '304', '305', '307']
    if request.method == "GET":
        sites = Websniff.objects.all().order_by('id')
    if request.method == "POST":
        url_list = []
        name = request.POST.get('site_name')
        slug = request.POST.get('weburl')
        if not pk:  #pk不存在则是创建新条目,反之则是修改已存在条目
            Websniff.objects.get_or_create(name=name, slug=slug)  #新建
        else:
            web = Websniff.objects.get(id=pk)
            web.name = name
            web.slug = slug
            web.save()
        urlobjs = Websniff.objects.all().order_by('id')
        print url_list
        url_list = list(urlobjs)
        paginator = Paginator(urlobjs, 10)
        if pk:
            curobj = Websniff.objects.get(id=pk)
            url_pos = url_list.index(curobj)
            page = (url_pos + 1) / 10.0
            page = int(math.ceil(page))
            websniffs = paginator.page(page)
        else:
            page = urlobjs.count() / 10.0
            page = int(math.ceil(page))
            websniffs = paginator.page(page)
        return render(request, 'ywweb/web.html', {'websniffs': websniffs, 'codelist': stat_code})
        
    paginator = Paginator(sites, 10)
    try:
        page = request.GET.get('page')
        websniffs = paginator.page(page)      
    except PageNotAnInteger:
        # If page is not an integer, deliver first page.
        websniffs = paginator.page(1)
    except EmptyPage:
        # If page is out of range (e.g. 9999), deliver last page of results.
        websniffs = paginator.page(paginator.num_pages)
    return render(request, 'ywweb/web.html', {'websniffs': websniffs, 'codelist': stat_code})

@login_required
def web_edit(request, pk):
    site = Websniff.objects.get(id=pk)
    return render(request, 'ywweb/editweb.html', {'site': site})
