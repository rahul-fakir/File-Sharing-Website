# coding: utf-8
import datetime
from django.contrib.auth.decorators import login_required
from django.shortcuts import render, get_object_or_404
from django.http import HttpResponseRedirect, HttpResponse, Http404
from django.contrib.auth import logout
from catalog.models import item, fotos, file, like, Categories, Libraries
from django.http import JsonResponse
import json
from django.db.models import Q
from cab.models import ExtUser


def main(request):
    items = item.objects.all().order_by('-date_published')
    download = False
    if items.count() > 12:
        download=True
    lik = []
    items = items[:12]
    for i in items:
        lik.append([i.id, like.objects.filter(item=i).count()])
    categories = Categories.objects.all()
    return render(request, "catalog.html", {'items': items, 'likes':lik, 'download':download, 'categories': categories})
    
    
def itemHtml(request):
    categories = Categories.objects.all()
    try:
        id = request.path[request.path.find('/')+1:]
        id = id[id.find('/')+1:]
        id = id[:id.find('/')]
        it = item.objects.select_related().get(id=int(id))
        it.views += 1
        it.main_foto.name = it.main_foto.name.replace('media/','static/')
        it.save()
        #i.main_foto.save()
        f = it.foto.replace('media','static').split(';')
        files = file.objects.select_related().filter(item=it)
        for i in files:
            i.f.name = i.f.name.replace('media/', 'static/')
            #i.f.save()
            
        lik = like.objects.filter(item=it).count()
        #tags = it.tags
        return render(request, 'item.html', {
            'item':it,
            'f':f[:len(f)-1],
            'files': files,
            'like': lik,
            'tags':it.tags.split(';'),
            'categories': categories,
        })
    except:
        raise Http404


def libraries(request):
    categories = Categories.objects.all()
    libraries_all = Libraries.objects.all()
    return render(request, 'libraries.html', {"libraries_all": libraries_all, 'categories': categories})


def libraries_detail(request, id):
    categories = Categories.objects.all()
    library = Libraries.objects.get(id=id)
    items = library.item_set.all()
    lik = []
    for i in items:
        lik.append([i.id, like.objects.filter(item=i).count()])
    return render(
        request, 'items.html',
        {'items': items, 'likes': lik, 'categories': categories})


def showFile(request, id):
    _file = get_object_or_404(file, id=id)
    categories = Categories.objects.all()
    if _file.name.endswith('.stl') or _file.name.endswith('.STL'):
        path = _file.name
        return render(request, 'stl_file.html', {'path': path, 'categories': categories})
    if _file.name.endswith('.x3d') or _file.name.endswith('.X3D'):
        path = _file.name
        return render(request, 'x3d_file.html', {'path': path, 'categories': categories})
    return render(request, 'invalid_file.html')



def itemHtmlFile(request, id):
    categories = Categories.objects.all()
    it = item.objects.select_related().get(id=id)
    f = it.foto.replace('media','static').split(';')
    files = file.objects.select_related().filter(item=it)
    for i in files:
        i.f.name = i.f.name.replace('media/', 'static/')
        lik = like.objects.filter(item=it).count()
    if 'file_id' in request.GET:
        file_id = request.GET['file_id']
        _file = get_object_or_404(file, id=file_id)
        if _file.name.endswith('.stl') or _file.name.endswith('.STL'):
            path = _file.name
            return render(request,
                    'item_stl_file.html',
                        {
                            'path': path,
                            'categories': categories,
                            'item':it,
                            'f':f[:len(f)-1],
                            'files': files,
                            'like': lik,
                            'tags':it.tags.split(';'),
                            'file_id': file_id
                        })
        if _file.name.endswith('.x3d') or _file.name.endswith('.X3D'):
            path = _file.name
            return render(request,
                'item_x3d_file.html',
                        {
                            'path': path,
                            'categories': categories,
                            'item':it,
                            'f':f[:len(f)-1],
                            'files': files,
                            'like': lik,
                            'tags':it.tags.split(';'),
                            'file_id': file_id
                        })
    return render(request, 'item.html', {
        'item':it,
        'f':f[:len(f)-1],
        'files': files,
        'like': lik,
        'tags':it.tags.split(';'),
        'categories': categories
    })
