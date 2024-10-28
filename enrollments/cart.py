class cart:
    def __init__(self , request):
        self.request = request
        self.session = request.session
        cart = self.session.get("cart")
        if not cart:
            cart = self.session['cart']
        self.cart = cart
        self.session['cart'] = {}

    

