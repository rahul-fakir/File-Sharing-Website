from django.shortcuts import render
from cab.models import ExtUser
from catalog.models import item, Categories, Libraries
from django.contrib.auth import authenticate, login
from django.http import HttpResponseRedirect, JsonResponse, HttpResponse
from django.core.urlresolvers import reverse
from django.contrib import messages
from django.contrib.admin.views.decorators import staff_member_required
from django.shortcuts import get_object_or_404
from PIL import Image


# Create your views here.
# @staff_member_required(login_url='/admins/login')
def home(request):
    if request.user.is_authenticated():
        if request.user.is_admin:
            users = ExtUser.objects.all()
            item_all = item.objects.all()
            delete_id = request.GET.get('delete_id')
            if delete_id:
                try:
                    ExtUser.objects.get(id=delete_id).delete()
                    return HttpResponseRedirect(reverse('staff:home'))
                except:
                    return HttpResponseRedirect(reverse('staff:home'))
            make_staff = request.GET.get('make_staff')
            if make_staff:
                extuser = get_object_or_404(ExtUser, id=make_staff)
                extuser.is_admin = True
                extuser.save()
            remove_staff = request.GET.get('remove_staff')
            if remove_staff:
                extuser = get_object_or_404(ExtUser, id=remove_staff)
                extuser.is_admin = False
                extuser.save()
            return render(request, 'home.html', {"users": users, "item_all": item_all})
        else:
            return render(request, 'staff-login.html')    
    else:
        return render(request, 'staff-login.html')
    
def staff_login(request):
    if request.method == 'POST':
        username_email = request.POST['username']
        password = request.POST['password']
        user = authenticate(email=username_email, password=password)
        if user is not None:
            if user.is_active:
                if user.is_admin:
                    login(request, user)
                    return HttpResponseRedirect(reverse('staff:home'))
                else:
                    messages.warning(request, "Sorry you Don't have access to Enter to this page , please contact the website administrator .")
                    return render(request, 'staff-login.html')
            else:
                messages.warning(request, 'Your account locked')
                return render(request, 'staff-login.html')                
        else:
            messages.warning(request, 'Please Enter valid username / password .')
            return render(request, 'staff-login.html')
    return render(request, 'staff-login.html')

@staff_member_required(login_url='/admins/login')
def edit_profile(request, pk):
    if request.method == 'POST':
        user_id = request.POST['user_id']
        ExtUser.objects.get(id=user_id).delete()
        return HttpResponseRedirect(reverse('staff:home'))
    user = ExtUser.objects.get(id=pk)
    items = item.objects.filter(user_id=request.user.id).select_related()
    return render(request, 'edit-profile.html', {"user": user, "items": items})


@staff_member_required(login_url='/admins/login')
def user_info(request):
    if request.method == 'POST':
        user = ExtUser.objects.get(email=request.POST['p_email'])
        user.firstname = request.POST['firstName']
        user.lastname = request.POST['lastname']
        user.email = request.POST['email']
        user.save()
        return HttpResponseRedirect(reverse('staff:edit-profile', args=[user.id]))

@staff_member_required(login_url='/admins/login')
def change_password(request):
    user = ExtUser.objects.get(id=request.POST['user_id'])
    user.set_password(request.POST['password2'])
    user.save()
    return JsonResponse({'result':True})

@staff_member_required(login_url='/admins/login')
def saveAvatar(request, user_id):
    user = ExtUser.objects.get(id=user_id)
    user.avatar = request.POST['name'].replace('media', 'static')
    user.save()
    return HttpResponse("ok")

from catalog.models import item, fotos, file, like

@staff_member_required(login_url='/admins/login')
def item_view(request):
    items = item.objects.all().order_by('-date_published')
    download = False
    if items.count() > 12:
        download = True
    lik = []
    items = items[:12]
    for i in items:
        lik.append([i.id, like.objects.filter(item=i).count()])
    return render(
        request, 'staffitems.html',
        {'items': items, 'likes': lik, 'download': download})


@staff_member_required(login_url='/admins/login')
def item_view_only(request, pk):
    libraries_all = Libraries.objects.all()
    if request.method == 'POST':
        it = item.objects.get(id=pk)
        library = Libraries.objects.get(name=request.POST['library'])
        it.name = request.POST['name']
        it.information = request.POST['information']
        it.tags = request.POST['tags']
        it.library = library
        it.save()
        return HttpResponseRedirect(reverse("staff:item_view_only", args=[pk]))
    id = request.path[request.path.find('/')+1:]
    id = id[id.find('/')+1:]
    id = id[:id.find('/')]
    it = item.objects.select_related().get(id=int(pk))
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
    return render(request, 'staff-item-view.html', {
        'item':it,
        'f':f[:len(f)-1],
        'files': files,
        'like': lik,
        'tags':it.tags.split(';'),
        'libraries_all': libraries_all,
    })

@staff_member_required(login_url='/admins/login')
def item_image_delete(request):
    _item = item.objects.select_related().get(id=int(request.POST['item'])) 
    if request.user.is_staff:
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

@staff_member_required(login_url='/admins/login')
def item_file_delete(request):
    _item = item.objects.get(id=int(request.POST['item']))
    if request.user.is_staff:
        f = file.objects.get(id=int(request.POST['id']))
        if f.item == _item:
            f.delete()
            return HttpResponse('ok')
    raise Http404


@staff_member_required(login_url='/admins/login')
def item_delete(request):
    item_id = request.GET.get('item_id')
    if item_id:
        item.objects.get(id=item_id).delete()
    return HttpResponseRedirect(reverse('staff:home'))
    

@staff_member_required(login_url='/admins/login')    
def categories(request):
    if request.method == 'POST':
        obj = Categories()
        obj.name = request.POST['name']
        obj.url = request.POST['url']
        obj.save()
        return HttpResponseRedirect(reverse('staff:categories'))
    delete_id = request.GET.get('delete_id')
    if delete_id:
        try:
            Categories.objects.get(id=delete_id).delete()
            return HttpResponseRedirect(reverse('staff:categories'))
        except:
            return HttpResponseRedirect(reverse('staff:categories'))
    categories_all = Categories.objects.all()
    return render(request, 'category.html', {"categories_all": categories_all})
    
    
def categories_edit(request, pk):
    if request.method == 'POST':
        obj = Categories.objects.get(id=pk)
        obj.name = request.POST['name']
        obj.url = request.POST['url']
        obj.save()
        return HttpResponseRedirect(reverse('staff:categories'))
    categories = Categories.objects.get(id=pk)
    return render(request, 'categories-edit.html', {"categories": categories})


@staff_member_required(login_url='/admins/login')    
def libraries(request):
    delete_id = request.GET.get('delete_id')
    if delete_id:
        try:
            Libraries.objects.get(id=delete_id).delete()
            return HttpResponseRedirect(reverse('staff:libraries'))
        except:
            return HttpResponseRedirect(reverse('staff:libraries'))
    libraries_all = Libraries.objects.all()
    return render(request, 'library.html', {"libraries_all": libraries_all})


@staff_member_required(login_url='/admins/login')
def libraries_edit(request, pk):
    libraries = Libraries.objects.get(id=pk)
    return render(request, 'libraries-edit.html', {"libraries": libraries})


@staff_member_required(login_url='/admins/login')
def addlibraries(request):
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
    lib = Libraries(
        name = request.POST['name'],
        image = foto[0],
    )
    lib.save()
    return HttpResponse("ok")


@staff_member_required(login_url='/admins/login')
def editlibraries(request, id):
    lib = Libraries.objects.get(id=id)
    if request.POST['fotos'] == "":
        f = lib.image.path
    else:
        f = request.POST['fotos'].split(';')[0]
    foto = fotos.objects.filter(path=f)[:1]
    lib.name = request.POST['name']
    lib.image = foto[0]
    lib.save()
    return HttpResponse("ok")
