from aromatica.models import Product

class Cart():
    def __init__(self, request):
        self.session = request.session

        #get current session 
        cart = self.session.get('session_key')
        
        if not cart:
            cart = self.session['session_key'] = {}

        #if 'session_key' not in request.session:
            #cart = self.session['session_key'] = {}

            #ensure basket is acessible for every page

        self.cart = cart

    def add(self, product, quantity):
        product_id = str(product.id)
        product_qty = str(quantity)

        if product_id not in self.cart:
            self.cart[product_id] = int(product_qty)
            #self.cart[product_id] = {'price': str(product.price)}

        self.session.modified = True

    def __len__(self):
        return len(self.cart)
    
    def get_prods(self):
        #get product is from the cart
        product_ids = self.cart.keys()
        #use id to display the products
        products = Product.objects.filter(id__in=product_ids)

        return products
    
    def get_quants(self):
        quantities = self.cart
        return quantities
    
    def update(self, product, quantity):
        product_id = str(product)
        product_qty = int(quantity)

        #get basket
        basket = self.cart
        #update basket

        basket[product_id] = product_qty

        self.session.modified = True

        thing = self.cart
        return thing
    
    def delete(self, product):
        product_id = str(product)

        #delete form basket
        if product_id in self.cart:
            del self.cart[product_id]

        self.session.modified = True

    def cart_total(self):
        #get product id 
        product_ids = self.cart.keys()

        products = Product.objects.filter(id__in=product_ids)
        quantities = self.cart
        #start from 0
        total = 0

        for key, value in quantities.items():
            key = int(key)
            for product in products:
                if product.id == key:
                    total = total+ (product.price * value)
        return total


