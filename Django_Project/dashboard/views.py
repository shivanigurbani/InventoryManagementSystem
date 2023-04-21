from django.shortcuts import render,redirect
from .models import Product,Order
from django.contrib.auth.decorators import login_required
from django.http import HttpResponse
from .forms import PrdoductForm,OrderForm
from django.contrib.auth.models import User
from django.contrib import messages
# Create your views here.

@login_required(login_url='user-login')
def index(request):
    order=Order.objects.all()
    products=Product.objects.all()
    product_count=Product.objects.all().count()
    order_count=Order.objects.all().count()
    workers_count=User.objects.all().count()
    if request.method=='POST':
        form=OrderForm(request.POST)
        if form.is_valid():#after the validation method is call we have to assign the staff to the order which have been made 
            instance=form.save(commit=False)#created a new variable instance if commit is = false we haven't saved it yet 
            instance.staff=request.user#whichever logged in  user is making a request is the staff we want to assign that particular item 
            instance.save()
            return redirect('dashboard-index')
    else:
        form=OrderForm()
    context={
        'order':order,
        'form':form,
        'products':products,
        'product_count':product_count,
        'order_count':order_count,
        'workers_count':workers_count,
    }
    return render(request,'dashboard/index.html',context)

@login_required(login_url='user-login')
def staff(request):
    workers=User.objects.all()
    workers_count=workers.count()
    order_count=Order.objects.all().count()
    product_count=Product.objects.all().count()
    context={
        'workers':workers,
        'workers_count':workers_count,
        'order_count':order_count,
        'product_count':product_count,
    }
    return render(request,'dashboard/staff.html',context)

@login_required
def staff_detail(request,pk):
    workers=User.objects.get(id=pk)
    context={
        'workers':workers,
    }
    return render(request,'dashboard/staff_detail.html',context)

@login_required(login_url='user-login')
def product(request):
    items=Product.objects.all()#Using ORM
    #items=Product.objects.raw('SELECT * FROM dashboard_product') #Rawsql command #nameofapplcation_nameofmodels
    workers_count=User.objects.all().count()
    order_count = Order.objects.all().count()
    product_count=items.count()
    
    if request.method=='POST':
        form=PrdoductForm(request.POST)
        if form.is_valid():
            form.save()
            product_name=form.cleaned_data.get('name')
            messages.success(request,f'{product_name} has been added')
            return redirect('dashboard-product')

    else:
        form=PrdoductForm()
    context={
        'items':items,
        'form':form,
        'workers_count':workers_count,
        'order_count':order_count,
        'product_count':product_count,
    }

    return render(request,'dashboard/product.html',context)


@login_required
def product_delete(request,pk): 
    item=Product.objects.get(id=pk)
    if request.method=="POST":
        item.delete()
        return redirect('dashboard-product')
    
    return render(request,'dashboard/product_delete.html')


@login_required
def product_update(request,pk):
    item= Product.objects.get(id=pk)
    if request.method=='POST':
        form=PrdoductForm(request.POST, instance=item)
        if form.is_valid():
            form.save()
            return redirect('dashboard-product')
    else:
        form=PrdoductForm(instance=item)
    context={
        'form':form

    }
    return render(request,'dashboard/product_update.html',context)



@login_required(login_url='user-login')
def order(request):
    order = Order.objects.all()
    order_count=order.count()
    workers_count=User.objects.all().count()
    product_count=Product.objects.all().count()
    context = {
        'order': order,
        'workers_count':workers_count,
        'order_count':order_count,
        'product_count':product_count,
    }
    return render(request,'dashboard/order.html',context)   