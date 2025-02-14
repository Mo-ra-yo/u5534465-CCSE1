from django.shortcuts import render,redirect
from cart.cart import Cart
from billing.forms import ShippingForm, PaymentForm
from billing.models import ShippingAddress, Order, OrderItem
from django.contrib import messages
from django.contrib.auth.models import User
from aromatica.models import Product

# Create your views here.
def billing_success(request):
    return render(request, "billing/billing_success.html")

def checkout(request):
    #get the basket
    cart = Cart(request)
    cart_products = cart.get_prods
    quantities = cart.get_quants
    totals = cart.cart_total()

    if request.user.is_authenticated:
        #checkout as logged in
        shipping_user = ShippingAddress.objects.get(user__id=request.user.id)
        shipping_form = ShippingForm(request.POST or None, instance=shipping_user)

        return render(request, "billing/checkout.html", {"cart_products":cart_products, "quantities":quantities, "totals":totals, "shipping_form":shipping_form})

    else:
        #Checkout without login
        shipping_form = ShippingForm(request.POST or None)
        return render(request, "billing/checkout.html", {"cart_products":cart_products, "quantities":quantities, "totals":totals, "shipping_form":shipping_form})


def billing_details(request):
    #only logged in users can access
    if request.POST:
    #get the cart
        cart = Cart(request)
        cart_products = cart.get_prods
        quantities = cart.get_quants
        totals = cart.cart_total()

        #create billing session
        my_delivery = request.POST
        request.session['my_delivery'] = my_delivery

        #Cgeck to se if user is logged in
        if request.user.is_authenticated:
            #get billing form
            billing_form =PaymentForm()
            return render(request, "billing/billing_details.html", {"cart_products":cart_products, "quantities":quantities, "totals":totals, "shipping_details":request.POST, "billing_form":billing_form})

        else:
            #not logged in 
            billing_form =PaymentForm()
            return render(request, "billing/billing_details.html", {"cart_products":cart_products, "quantities":quantities, "totals":totals, "shipping_details":request.POST, "billing_form":billing_form})

        shipping_form = request.POST
        return render(request, "billing/billing_details.html", {"cart_products":cart_products, "quantities":quantities, "totals":totals, "shipping_form":shipping_form})

    else:
        messages.success(request, "Access: Denied!")
        return redirect('home')
    
def process_order(request):
    if request.POST:
        #get billing form details
        cart = Cart(request)
        cart_products = cart.get_prods
        quantities = cart.get_quants
        totals = cart.cart_total()

        payment_form = PaymentForm(request.POST or None)

        #create shipping session data
        my_delivery = request.session.get('my_delivery')

        #get order info
        full_name = my_delivery['bill_full_name']
        email = my_delivery['bill_email']
        #create shipping address
        shipping_address = f"{my_delivery['bill_address1']}\n{my_delivery['bill_address2']}\n{my_delivery['bill_postcode']}\n{my_delivery['bill_country']}"
        amount_paid = totals

        #create orders
        if request.user.is_authenticated:
            user = request.user

            create_order = Order(user=user, full_name=full_name, email=email, shipping_address=shipping_address, amount_paid=amount_paid)
            create_order.save()

            #create orderitems
            #get the order id primary key
            order_id = create_order.pk
            #get product id
            for product in cart_products():
                product_id = product.id
                price = product.price

            #get the quantity
            for key,value in quantities().items():
                if int(key) == product.id:

                    create_order_item =OrderItem(user=user, order_id=order_id, product_id=product_id, price=price, quantity=value)
                    create_order_item.save()

                #empty cart
                for key in list(request.session.keys()):
                    if key == "session_key":
                        #delete the session key
                        del request.session[key]


            messages.success(request, "Successfully Placed Order")
            return redirect('home')
        
        else:
            #user not logged in
            create_order = Order(full_name=full_name, email=email, shipping_address=shipping_address, amount_paid=amount_paid)
            create_order.save()

            #create orderitems
            #get the order id primary key
            order_id = create_order.pk
            #get product id
            for product in cart_products():
                product_id = product.id
                price = product.price

            #get the quantity
            for key,value in quantities().items():
                if int(key) == product.id:

                    create_order_item =OrderItem( order_id=order_id, product_id=product_id, price=price, quantity=value)
                    create_order_item.save()

                     #empty cart
                for key in list(request.session.keys()):
                    if key == "session_key":
                        #delete the session key
                        del request.session[key]



            messages.success(request, "Successfully Placed Order")
            return redirect('home')


    else:
        messages.success(request, "Access: Denied!")
        return redirect('home')



