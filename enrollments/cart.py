class cart:
    def __init__(self , request):
        self.request = request             # ریکوئست کاربر
        self.session = request.session     # (دیتای موقت کابر) سشن ریکوئست کاربر
        cart = self.session.get("cart")    # گرفتن اطلاعات  سبد خرید  از سشن کاربر
        if not cart:
            cart = self.session['cart']    #  اگر در سشن مقدار  سبد خرید وجود نداشت یعنی برای اولین بار خرید میکند و  یکی ایجاد میکند
        self.cart = cart
        self.session['cart'] = {} # مقدار سبد در سشن را برابر با یک دیکشنری خالی قرار میدهد 


    def add(self , product , num=1): # متدی برای اضافه کردن دوره ها (محصولات) به  سبد خرید 
        product_id = str(product.id) 
        if product_id not in self.cart :  
            self.cart['product_id'] = {'num':num}   # اگر آیدی در سبد خرید وجود نداشت ، به سبد خرید اضافه میکند
        # else: 
        #     self.cart['product_id']['num']+=num 

            self.save()  # تعییرات اعمال شده در سبد خرید را ذخیره میکند

    def save(self): # متدی برای ذخیره تعییرات
        self.session.modified = True # 

    def remove(self , product):       # متدی برای حذف محصول 
        product_id = str(product.id)
        if product_id in self.cart:   #  اگر محصول در سبد خرید وجود داشت آن را حذف میکند
            del self.cart[product_id]
        self.save() # تعییرات را ذخیره می کند



 




