# coding: utf-8
import datetime
from django.contrib.auth.decorators import login_required
from django.shortcuts import render
from django.http import HttpResponseRedirect, HttpResponse, Http404
from django.contrib.auth import logout
from catalog.models import item, fotos, file, like, Categories, Libraries
from django.http import JsonResponse
import json
from .models import ExtUser
from .models import UserManager
from zipfile import *
from django.db.models import Q
from django.contrib.auth import get_user_model
from cab.forms import *
from PIL import Image
import random
import string
from django.core.mail import send_mail
from os.path import abspath, join, dirname


# logout cab
@login_required
def cab_logout(request):
    # logout
    logout(request)

    # redirect
    return HttpResponseRedirect("/login")


# /cab/
@login_required
def main(request):
    items = item.objects.filter(user_id=request.user.id).select_related()
    categories = Categories.objects.all()
    libraries_all = Libraries.objects.all()
    for i in items:
        i.main_foto.name = ("%s" % i.main_foto.path).replace("media/", 'static/')
        i.foto = i.foto.replace("media/", 'static/')
        i.save()
        i.main_foto.save()
    return render(request, 'profile.html', {'items': items, 'categories': categories, 'libraries_all': libraries_all})
    


@login_required
def addAjax(request):
    foto = request.POST['fotos'].split(";")
    f = fotos(
        path='static/fotos/no_image_dummy.png',
        name='no_image_dummy.png'
    )
    if foto[0] != "":
        f = fotos( path=foto[0].replace('media','static'),name=foto[0].replace('media','static') )
    f.save()
    c = item(
        name=request.POST['name'],
        information=request.POST['inform'],
        date_published=datetime.datetime.now(),
        views=0,
        tags="",
        main_foto=f,
        fotos=request.POST['fotos']
    )
    c.save()
    return HttpResponse("ok")
        
        
@login_required
def downloadAvatar(request):
    fot = fotos(
        path=request.FILES['file'],
        name="%s" % request.FILES['file']
    )
    fot.save()
    return JsonResponse({
        'foto': "%s" % fot.path
    })
    

@login_required
def saveAvatar(request):
    user = ExtUser.objects.get(email=request.user.email)
    user.avatar = request.POST['name'].replace('media', 'static')
    user.save()
    return HttpResponse("ok")
    
    
@login_required
def editProfile(request):
    user = ExtUser.objects.get(email=request.user.email)
    user.firstname = request.POST['firstName']
    user.lastname = request.POST['lastname']
    user.email = request.POST['email']
    user.save()
    return HttpResponseRedirect("/profile/")
    

@login_required
def downloadFilesNewItem(request):
    fot = file(
        name="%s" % request.FILES['file'],
        dowloads=0,
        size=len(request.FILES['file']),
        date_published=datetime.datetime.now(),
        f=request.FILES['file'],
        item=item.objects.all()[0]
    )
    fot.save()
    return JsonResponse({
        'file': fot.id
    })
    

@login_required
def addItem(request):
    if request.POST['fotos'] == "":
        fot = fotos(
            path="media/fotos/def.jpg",
            name="media/fotos/def.jpg"
        )
        fot.save()
        f = "media/fotos/def.jpg"
    else:
        f = request.POST['fotos'].split(';')[0]
    img = Image.open(f)#otos.objects.get(path=f).path)
    if (img.width / 4.0) * 3 != img.height:
        if img.width > img.height:
            one = img.height / 3.0
            img = img.crop(
                (
                    (img.width - one*4)/2.0,
                    0,
                    (img.width - one*4)/2.0 + one*4.0,
                    one*3.0
                )
            )
        else:
            one = img.width / 4.0
            img = img.crop(
                (
                    0,
                    (img.height - one*3)/2.0,
                    one*4,
                    (img.height - one*3)/2.0 + one*3.0
                )
            )
        img.save(f)
    foto = fotos.objects.filter(path=f)[:1]
    library = Libraries.objects.get(name=request.POST['library'])
    it = item(
        name = request.POST['name'],
        date_published = datetime.datetime.now(),
        main_foto = foto[0],
        foto = request.POST['fotos'],
        information = request.POST['inform'],
        views = 0,
        tags = request.POST['tags'].replace(',',';'),
        user = ExtUser.objects.get(id=request.user.id),
        library = library
    )
    it.save()
    for i in request.POST['files'].split(';'):
        i = i.replace(";","")
        if i != "":
            fil = file.objects.get(id=int(i))
            fil.item=it
            fil.save()
    return HttpResponse("ok")



def register(request):
    return render(request, 'register.html', {'form':UserCreationForm()})
    


def registerPost(request):
    if request.method == "POST":
        user_form = UserCreationForm(request.POST)
        
        if user_form.is_valid():
            new_user = user_form.save(commit=False)
            new_user.set_password(user_form.cleaned_data['password1'])
            new_user.avatar = "media/fotos/family-guy-peter-310_k1wDME5.jpg.jpg"
            new_user.save()
            return HttpResponseRedirect("/login")
    else:
        user_form = UserCreationForm()
    return render(request, 'register.html', {'form':user_form})
    
    

@login_required
def deleteItem(request):
    it = item.objects.get(id=int(request.POST['id']))
    for i in like.objects.filter(item=it):
        i.delete()
    for i in file.objects.filter(item=it):
        i.delete()
    it.delete()
    return HttpResponse("ok")
    

@login_required
def addDownloadFile(request):
    try:
        f = file.objects.get(id=int(request.POST['id']))
        f.dowloads += 1
        f.save()
        return HttpResponse("ok")
    except:
        raise Http404
        
        
@login_required
def addDownloadFileAll(request):
    name = 'media/files/' + str(datetime.datetime.now()) + '.zip'
    url = name.replace('../','').replace('media/', 'static/')
    # Создание архива
    z = ZipFile(name, 'w')
    # Добавление файла в архив
    for i in file.objects.filter(item=item.objects.get(id=int(request.POST['id']))):
        z.write("%s" % i.f, i.name)
    z.close()
    
    return JsonResponse({
        'zip': url
    })
    
    
def search(request):
    items = item.objects.filter(
        Q(name__icontains=request.GET['s']) | 
        Q(date_published__icontains=request.GET['s']) | 
        Q(information__icontains=request.GET['s']) | 
        Q(tags__icontains=request.GET['s'])
    )
    lik = []
    for i in items:
        lik.append([i.id, like.objects.filter(item=i).count()])
    return render(request, "catalog.html", {'items': items, 'likes':lik})
    

@login_required
def _like(request):
    for i in like.objects.filter(
        Q(user=ExtUser.objects.get(id=int(request.user.id))),
        Q(item=item.objects.get(id=int(request.POST['id'])))
    ):
        i.delete()
        return JsonResponse({
            "result":True
        })
    
    lik = like(
        user=ExtUser.objects.get(id=int(request.user.id)),
        item=item.objects.get(id=int(request.POST['id']))
    )
    lik.save()
    return JsonResponse({
        "result":False
    })
    
    
def ajaxOpens(request):
    items = item.objects.all().order_by('-date_published')
    kol = opa = 0
    for i in items:
        if i.id == int(request.POST['id']):
            kol = opa
            break
        opa += 1
    items  = items[opa+1:opa+13]
    lik = []
    for i in items:
        lik.append([i.id, like.objects.filter(item=i).count()])
    spisok = []
    for i in items:
        el = {}
        el.update({'name': i.name})
        el.update({'author': i.user.lastname + " " + i.user.firstname})
        el.update({'avatar': i.user.avatar})
        el.update({'main_foto': i.main_foto.name})
        el.update({'date': i.date_published})
        el.update({'views': i.views})
        el.update({'id': i.id})
        for q in lik:
            if q[0] == i.id:
                el.update({'likes': q[1]})
        
        #spisok.update({i.id: el})
        spisok.append(el)
    return JsonResponse({
        "items":spisok
    })
    


# FORGOT PASSWORD
def forgotPassword(request):
    if request.method == 'POST':
        #if request.POST['user'] != "":
        try:
            user = ExtUser.objects.get(email=request.POST['user'])
            if user.forgotKey == request.POST['Key']:
                return render(request, 'forgotPassword.html', {'password':user})
            else:
                return render(request, 'forgotPassword.html', {'key':user, 'errorKey':True})
        except Exception:
            try:
                if request.POST['password'] != "":
                    try:
                        user = ExtUser.objects.get(email=request.POST['userforgotKey'])
                        if request.POST['password'] == request.POST['password2']:
                            #user = ExtUser.objects.get(forgotKey=request.POST['userforgotKey'])
                            user.set_password(request.POST['password'])
                            user.forgotKey = ""
                            user.save()
                            return HttpResponseRedirect('/login')
                        else:
                            return render(request, 'forgotPassword.html', {'passwordError':user, 'password':user})
                    except Exception:
                        raise Http404
            except Exception:
                try:
                    user = ExtUser.objects.get(email=request.POST['username'])
                    if user.forgotKey == "":
                        a = string.ascii_letters + string.digits
                        key = ''.join([random.choice(a) for i in range(10)])
                        user.forgotKey = key 
                        user.save()
                        send_mail('Password reset', 'Please enter the following code on the server in the field for restoration :' + key,
                        'info@biobots.com', [user.email], fail_silently=False)
                        return render(request, 'forgotPassword.html', {'key':user})
                    else:
                        return render(request, 'forgotPassword.html', {'key':user})
                except Exception:
                    return render(request, 'forgotPassword.html', {'error':True})
    elif request.method == 'GET':
        return render(request, 'forgotPassword.html')
    raise Http404
    
    
    
@login_required
def changePassword(request):
    try:
        user = ExtUser.objects.get(id=int(request.user.id))
        if user.check_password(request.POST['passwordOld']):
            if request.POST['password1'] == request.POST['password2']:
                if request.POST['password2'] != "":
                    user.set_password(request.POST['password2'])
                    user.save()
                    return JsonResponse({'result':True})
                else:
                    return JsonResponse({'result':False, 'error':'Password length zero'})
            else:
                return JsonResponse({'result':False, 'error':'New passwords do not match'})
        else:
            return JsonResponse({'result':False, 'error':'Old password does not match'})
    except Exception:
        return JsonResponse({'result':False, 'error':'The error on the server . Please try again later'})
        
        
        

@login_required
def changeItem(request):
    libraries_all = Libraries.objects.all()
    categories = Categories.objects.all()
    _item = item.objects.select_related().get(id=int(request.GET['item']))
    if _item.user.id == request.user.id:
        _item.main_foto.name = _item.main_foto.name.replace('media/','static/')
        _item.save()
        f = _item.foto.replace('media','static').split(';')
        files = file.objects.select_related().filter(item=_item)
        for i in files:
            i.f.name = i.f.name.replace('media/', 'static/')

        return render(request, 'editItem.html', {
            'item':_item,
            'f':f[:len(f)-1],
            'files': files,
            'tags':_item.tags.split(';'),
            'libraries_all': libraries_all,
            'categories': categories
        })
        #return render(request, 'editItem.html', {'item':item.objects.get(id=int(request.GET['item']))})
    else:
        raise Http404
        
        
@login_required
def changeDelFoto(request):
    _item = item.objects.select_related().get(id=int(request.POST['item'])) 
    if _item.user.id == request.user.id:
        if int(request.POST['number']) != 1:
            q = _item.foto.split(';')[int(request.POST['number'])-1]
            _item.foto = _item.foto.replace(q+';', '')
            _item.save()
            return HttpResponse('ok')
        else:
            _item.foto = _item.foto[_item.foto.find(':')+1:]
            f = _item.foto.split(';')[0].replace('static/','media/')
            img = Image.open(f)
            if (img.width / 4.0) * 3 != img.height:
                if img.width > img.height:
                    one = img.height / 3.0
                    img = img.crop(
                        (
                            (img.width - one*4)/2.0,
                            0,
                            (img.width - one*4)/2.0 + one*4.0,
                            one*3.0
                        )
                    )
                else:
                    one = img.width / 4.0
                    img = img.crop(
                        (
                            0,
                            (img.height - one*3)/2.0,
                            one*4,
                            (img.height - one*3)/2.0 + one*3.0
                        )
                    )
                img.save(f)
            fot = fotos(path=f, name=f.replace('media/','static/'))
            fot.save()
            _item.main_foto = fot
            
            _item.save()
            
            return HttpResponse('ok')
    else:
        raise Http404
        
        

@login_required
def changeAddFoto(request):
    try:
        _item = item.objects.get(id=int(request.POST['item']))
        if _item.user.id == request.user.id:
            _item.foto += request.POST['fotos']
            _item.save()
            return HttpResponse("ok")
        raise Http404
    except Exception:
        raise Http404
    
    
@login_required
def changeTags(request):
    try:
        _item = item.objects.get(id=int(request.POST['item']))
        if _item.user.id == request.user.id:
            if request.POST['tags'] != "":
                _item.tags = request.POST['tags'].replace(',',';')
                _item.save()
                return HttpResponse('ok')
            raise Http404
        raise Http404
    except Exception:
        raise Http404

@login_required
def changeLibrary(request):
    try:
        _item = item.objects.get(id=int(request.POST['item']))
        if _item.user.id == request.user.id:
            if request.POST['library'] != "":
                library = Libraries.objects.get(name=request.POST['library'])
                _item.library = library
                _item.save()
                return HttpResponse('ok')
            raise Http404
        raise Http404
    except Exception:
        raise Http404
    
@login_required
def changeInform(request):
    try:
        _item = item.objects.get(id=int(request.POST['item']))
        if _item.user.id == request.user.id:
            if request.POST['inform'] != "":
                _item.information = request.POST['inform']
                _item.save()
                return HttpResponse('ok')
            raise Http404
        raise Http404
    except Exception:
        raise Http404
    
    
@login_required
def changeDelFile(request):
    _item = item.objects.get(id=int(request.POST['item']))
    if _item.user.id == request.user.id:
        f = file.objects.get(id=int(request.POST['id']))
        if f.item == _item:
            f.delete()
            return HttpResponse('ok')
    raise Http404
    
    
    
@login_required
def changeAddFileSave(request):
    try:
        _item = item.objects.get(id=int(request.POST['item']))
        if _item.user.id == request.user.id:
            for i in request.POST['files'].split(';'):
                try:
                    f = file.objects.get(id=int(i))
                    f.item = _item
                    f.save()
                except Exception:
                    pass
            return HttpResponse('ok')
        raise Http404
    except Exception:
        raise Http404