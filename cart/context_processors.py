from .cart import Cart

#create context processor to make cart accessible on every page
def cart(request):
    return{'cart': Cart(request)}