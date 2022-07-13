from django.http import HttpResponse
from django.contrib import messages
from django.core.mail import EmailMessage
from django.contrib.auth.decorators import login_required
from django.template.loader import render_to_string
from django.shortcuts import render, redirect
from customer.models import Cartitem, Delivery_address
from product.models import Variation, product
from order.models import OrderProduct
from .models import Order, Payment
import datetime
import razorpay
from senora.settings import RAZORPAY_API_KEY, RAZORPAY_API_SECRETKEY

# Create your views here.

@login_required(login_url='login')
def place_order(request):
    current_user = request.user
    payment_status = None
    grand_total = 0
    quantity = 0
    total = 0
    tax = 0
    cart_items = Cartitem.objects.filter(user=current_user)
    cart_count = cart_items.count()
    if cart_count > 0:
        for cart_item in cart_items:
            total += (cart_item.product.price * cart_item.quantity)
            quantity += cart_item.quantity
        tax = (3 * total)/100
        grand_total = int(total + tax)*100
    
        if request.method == 'POST':
            print('dddddddddddd')
            id = request.POST.get('address')
            print(id)
            address = Delivery_address.objects.get(user=current_user,id=id)
            data = Order()
            print("address",address)
            data.delivery_address = address
            data.order_note = request.POST.get('ordernote', False)
            data.order_total = grand_total/100
            data.tax = tax
            data.ip = request.META.get('REMOTE_ADDR')

            data.save()

            print(data.delivery_address)
            # Generate order number

            yr = int(datetime.date.today().strftime('%Y'))
            mt = int(datetime.date.today().strftime('%m'))
            dt = int(datetime.date.today().strftime('%d'))
            d = datetime.date(yr, mt, dt)
            current_date = d.strftime("%Y%m%d")
            order_number = current_date + str(data.id)
            request.session['order_number'] = order_number
            data.order_number = order_number
            data.user = request.user
            data.save()
            print(data.delivery_address)
            # create razorpay client
            client = razorpay.Client(auth=(RAZORPAY_API_KEY, RAZORPAY_API_SECRETKEY))

            # generate order
            DATA = {
                "amount": grand_total,
                "currency": "INR",
                "receipt": order_number,
                "payment_capture": 1
            }
            response_payment = client.order.create(data=DATA) 
            print(response_payment)
            payment_status = response_payment['status']
            print(payment_status)
            if payment_status == 'created':
                payment = Payment(
                    user=request.user,
                    order_id=order_number,
                    payment_method= 'razorpay',
                    amount_paid=grand_total/100,

                )
                payment.save()
                print(grand_total)
                response_payment['name'] = request.user
                context = {
                    'payment':   response_payment,
                    'grand_total':   grand_total,
                }
                return render(request, 'order/payments.html', context)
        else:
            return redirect('checkout')
    else:
        messages.error(request, 'add some items to cart...!!')
        return redirect('checkout')

@login_required(login_url='login')
def payment_status(request):
    payment_id = request.POST['razorpay_payment_id']
    order_number = request.session['order_number']
    print(payment_id)
    try:
        payment = Payment.objects.get(order_id = order_number)
        payment.payment_id = payment_id
        payment.paid       = True
        payment.save()
        print(payment,'..........................................')
        print(order_number)
        order = Order.objects.get(user=request.user,is_ordered=False,order_number=order_number)
        order.is_ordered = True
        order.status = 'Accepted'
        print(order.status)
        order.save()
        user = request.user
        cart_items = Cartitem.objects.filter(user=user)
        print(cart_items)
        for cart_item in cart_items:
            pro_data = OrderProduct()
            pro_data.order = order
            pro_data.payment = payment
            pro_data.user = user
            pro_data.product = cart_item.product
            pro_data.quantity = cart_item.quantity
            pro_data.product_price = cart_item.product.price
            pro_data.Ordered = True 
            pro_data.save()
            
            pr = cart_item.product
            Product = product.objects.get(id=pr.id)
            Product.stock -= cart_item.quantity
            Product.save()
            
        cart_items.delete()
        # print('fwffvw')
        mail_subject = 'Thank You for Shopping with us!'
        message = render_to_string('order/order_placed_email.html',{'user':request.user,'order':order,})
        to_email = request.user.email
        send_email = EmailMessage(mail_subject,message,to=[to_email])
        send_email.send()
        print(send_email,'lastlastlastlast;ast')
        return render(request,'order/payment_status.html',{'status':True})
    except:
        return render(request,'order/payment_status.html',{'status':False})
    
    
