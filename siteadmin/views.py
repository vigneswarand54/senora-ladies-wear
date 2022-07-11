from multiprocessing import context
from django.shortcuts import redirect, render
from order.models import Order
from product.models import product,Variation, subcategory,category
from django.contrib import messages
from django.contrib import auth
from django.contrib.auth.decorators import login_required
from django.db.models import Q
from accounts.models import accounts
from siteadmin.form import addproductform,addvariationform,addcategoryform,addsubcategoryform
from accounts.forms import registrationform

# Create your views here.


def admin_register(request):
    if request.method == 'POST':
        form = registrationform(request.POST)
        if form.is_valid():
            first_name = form.cleaned_data['first_name']
            last_name = form.cleaned_data['last_name']
            email = form.cleaned_data['email']
            phone = form.cleaned_data['phone']
            password = form.cleaned_data['password']
            username = email.split("@")[0]
            user = accounts.objects.create_superuser(
                first_name = first_name,
                last_name = last_name,
                email = email,
                phone = phone,
                username = username,
                password = password,
                )
            user.save()
            messages.success(request, 'Registration successful.')
            return redirect('adminregister')
    else:
        form = registrationform()
    context={
        'form':form,
    }
    return render(request,'admin/admin_register.html',context)

def admin_login(request):
    if request.method == 'POST':
        email = request.POST['email']
        password = request.POST['password']
        user = auth.authenticate(email = email , password = password)
        if user is not None:
            if user.is_superadmin:
                auth.login(request,user)
                messages.success(request, "You are logged in")
                return redirect('dashboard')
            else:
                messages.error(request, 'you are not an admin')
                return redirect('login')
        else:
            messages.error(request, 'invalid login credentials')
            return redirect('adminlogin')
    return render(request, 'admin/admin_login.html')

@login_required(login_url = 'adminlogin')
def admin_logout(request):
    auth.logout(request)
    messages.success(request, 'You are logged out.')
    return redirect('adminlogin')

@login_required(login_url = 'adminlogin')
def dashboard(request):
    return render(request,'admin/dashboard.html')

@login_required(login_url = 'adminlogin')
def usermanagement(request):
    if 'q' in request.GET:
        q = request.GET['q']
        user = accounts.objects.filter(Q(username__icontains=q)|Q(first_name__icontains=q)|Q(id__icontains=q))
    else:
        user = accounts.objects.all()
    context = {'users':user}
    return render(request,'admin/usermanagement.html',context)

@login_required(login_url = 'adminlogin')
def blockuser(request,id):
    user = accounts.objects.get(id=id)
    if user != request.user:
        user.is_active = False
        user.save()
        return redirect('usermanagement')
    
@login_required(login_url = 'adminlogin')
def unblockuser(request,id):
    user = accounts.objects.get(id=id)
    if user.is_active == False:
        user.is_active = True
        user.save()
        return redirect('usermanagement')
    
@login_required(login_url = 'adminlogin')
def productmanagement(request):
    if 'q' in request.GET:
        q = request.GET['q']
        Product = product.objects.filter(Q(product_name__icontains=q)|Q(id__icontains=q)).order_by('id')
    else:
        Product = product.objects.all().order_by('id')
    context = {'products':Product,}
    return render(request,'admin/productmanagement.html',context)

@login_required(login_url = 'adminlogin')
def editproduct(request,id):
    Product=product.objects.get(id=id)
    form=addproductform(instance=Product)
    if request.method == 'POST':
        form=addproductform(request.POST,instance=Product)
        if form.is_valid():
            form.save()
            return redirect('productmanagement')
    context={
        'form':form
    }
    return render(request,'admin/editproduct.html',context)

@login_required(login_url = 'adminlogin')
def deleteproduct(request,id):
    Product = product.objects.filter(id = id)
    Product.delete()
    return redirect('productmanagement')

@login_required(login_url = 'adminlogin')
def addproduct(request):
    form=addproductform()
    if request.method == 'POST':
        form=addproductform(request.POST)
        if form.is_valid():
            item = form.save()
            return redirect('addvariation')
        else:
            messages.warning(request, 'Enter the requied values')
    context={
        'form':form
    }
    return render(request,'admin/addproduct.html',context)

@login_required(login_url = 'adminlogin')
def filtermanagement(request):
    Category=category.objects.all().order_by('id')
    Subcategory=subcategory.objects.all().order_by('id')
    
    context={
        'categorys':Category,
        'subcategorys':Subcategory
    }
    return render(request,'admin/filtermanagement.html',context)

@login_required(login_url = 'adminlogin')
def addfilters(request):
    categoryform=addcategoryform()
    subcategoryform=addsubcategoryform()              
    
    context={
        'categoryform':categoryform,
        'subcategoryform':subcategoryform
    }
    return render(request,'admin/addfilters.html',context)

@login_required(login_url = 'adminlogin')
def addcategory(request):
    if request.method == 'POST':
        categoryform=addcategoryform(request.POST)
        if categoryform.is_valid():
            categoryform.save()
            return redirect('addfilters')
        else:
            print('hello1')
            messages.warning(request, 'Enter the requied values')
    return redirect('addfilters')

@login_required(login_url = 'adminlogin')
def deletecategory(request,id):
    Category = category.objects.filter(id = id)
    Category.delete()
    return redirect('filtermanagement')

@login_required(login_url = 'adminlogin') 
def addsubcategory(request):
    if request.method == 'POST':
        subcategoryform=addsubcategoryform(request.POST)
        if subcategoryform.is_valid():
            subcategoryform.save()
            return redirect('addfilters')
        else:
            messages.warning(request, 'Enter the requied values')
    return redirect('addfilters')

@login_required(login_url = 'adminlogin')
def deletesubcategory(request,id):
    Subcategory = subcategory.objects.filter(id = id)
    Subcategory.delete()
    return redirect('filtermanagement')

@login_required(login_url = 'adminlogin')
def load_subcategories(request):
    category = request.GET.get('category')
    Subcategory = subcategory.objects.filter(category_id=category).order_by('id')
    return render(request, 'admin/city_dropdown_list_options.html', {'Subcategory': Subcategory})

@login_required(login_url = 'adminlogin')
def variationmanagement(request):
    if 'q' in request.GET:
        q = request.GET['q']
        variation = Variation.objects.filter(Q(product_name__icontains=q)|Q(variation_category__icontains=q)|Q(variation_value__icontains=q)).order_by('id')
    else:
        variation = Variation.objects.all().order_by('id')
    context = {'variations':variation,}
    return render(request,'admin/variationmanagement.html',context)

@login_required(login_url = 'adminlogin')
def deletevariation(request,id):
    variation = Variation.objects.filter(id = id)
    variation.delete()
    return redirect('variationmanagement')

@login_required(login_url = 'adminlogin')
def addvariation(request):
    form = addvariationform()
    if request.method == 'POST':
        form=addvariationform(request.POST)
        if form.is_valid():
            form.save()
            return redirect('addvariation')
        else:
            messages.warning(request, 'Enter the requied values')
    context={
        'form':form
    }
    return render(request,'admin/addvariation.html',context)

@login_required(login_url = 'adminlogin')
def ordermanagement(request):
    if 'q' in request.GET:
        q = request.GET['q']
        order = Order.objects.filter(Q(order_number__icontains=q)|Q(id__icontains=q)|Q(status__icontains=q),is_ordered=True).order_by('-created_at')
    else:
        order = Order.objects.all().filter(is_ordered=True).order_by('-created_at')
    context = {'orders':order,}
    return render(request,'admin/ordermanagement.html',context)

@login_required(login_url = 'adminlogin')
def orderstatus(request,id):
    if request.method == 'POST':
        status = request.POST['status']
        order = Order.objects.get(id=id)
        order.status = status
        order.save()
    return redirect('ordermanagement')
