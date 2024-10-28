class cart:
    def __init__(self , request):
        self.request = request
        self.session = request.session
        cart = self.session.get("cart")
        if not cart:
            cart = self.session['cart']
        self.cart = cart
        self.session['cart'] = {}


    def add(self , product , num=1):
        product_id = str(product.id)
        if product_id not in self.cart :
            self.cart['product_id'] = {'num':num}
        else:
            self.cart['product_id']['num']+=num
            self.save()

    def save(self):
        self.session.modified = True

    def remove(self , product):
        product_id = str(product.id)
        if product_id in self.cart:
            del self.cart[product_id]
        self.save()


