from courses.models import Courses


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



    def __iter__(self): # متدی برای حلقه زدن روی سبد خرید کاربر
        product_ids = self.cart.keys() # دریافت تمام کلید های دیکشنری سبد خرید 
        product = Courses.objects.filter(id__in = product_ids)  # دریافت اطلاعات دوره های داخل سبد خرید از مدل دوره ها
        cart = self.cart.copy() # کپی گرفتن از سبد خرید تا اطلاعاتی که از دیتابیس به دست میآوریم را در کنار سبد خرید کپی شده 
                                # نشان دهیم نه در سبد خرید اصلی تا در هر بار فراخوانی شی ، اطلاعات محصولات قبلی دیگر در سشن قرار نگیرند
        for p in product:
            cart[str(p.id)]['object'] = p # روی محصولات سبد خرید حلقه میزنیم و درون آیدی محصول اطلاعات محصول (که از دیتابیس به دست آوردیم ) را نیز ذخیره میکنیم

        for prod in cart.values(): 
            yield prod # ساخت یک جنریتور که هربار روی سبد خرید حلقه زدیم  ، تنها یک محصول را برگرداند ، بار دیگر محصول دیگر تا آخرین محصول



    def __len__(self): # متدی برای دریافت تعداد محصولات سبد خرید
        return len(self.cart.keys()) 




