from django.shortcuts import render, redirect
from django.http import HttpResponse
from django.contrib.auth.hashers import make_password, check_password
from store.models.product import Product
from store.models.customer import Customer
from store.models.category import Category
from store.models.our_user import Our_user
from django.views import View
from django.contrib.auth.models import User
from django.contrib.auth import authenticate, login, logout
from store.forms.product_form import Product_form
from store.forms.category_form import Category_form
from django.core.mail import send_mail
import math, random
from django.http import JsonResponse


# Create your views here.
def index_page(request):
    if request.method == 'GET':
        product = None
        category = Category.get_all_category()
        categoryID = request.GET.get('category')
        if categoryID:
            product = Product.get_all_products_by_categoryid(categoryID)
        else:
            product = Product.objects.all()
        data = {}
        data['products'] = product
        data['categorys'] = category
        return render(request, 'index.html', data)
    else:
        # product_id=request.POST.get('product_id')
        
        return redirect('index')


# register form validation
def validateCustomer(customer, conform_password):
    error_msg = None
    if (not customer.name) and len(customer.name) < 4:
        error_msg = "name required or should be min 4char's long !"
        
    elif (not customer.phone) and len(customer.phone) < 4:
        error_msg = "phone number required or should be 10 digit !"
    elif len(customer.email) < 6:
        error_msg = "Email should be min 8char's long !"
    elif (not customer.password) and len(customer.password) < 6:
        error_msg = "password missing or should be 6char's long.!"
    elif not customer.password == conform_password:
        error_msg = "passwords are not same...!"
    return error_msg


def registerUser(request):
    PostData = request.POST
    name = PostData.get('name')
    phone = PostData.get('phone')
    email = PostData.get('email')
    password = PostData.get('password')
    conform_password = PostData.get('conform_password')

    value = {
        'name': name, 'phone': phone, 'email': email
    }

    customer = Customer(name=name, phone=phone, email=email, password=password)

    # save
    error_msg = validateCustomer(customer, conform_password)
    if not error_msg:
        customer.password = make_password(customer.password)
        customer.save()
        request.session['customer_id'] = customer.id
        return redirect('otp_page')
    else:
        data = {
            'error': error_msg,
            'values': value
        }

        return render(request, 'register.html', data)


def register_page(request):
    if request.method == 'GET':
        return render(request, 'register.html')
    else:
        return registerUser(request)


def generateOTP():
    digits = "0123456789"
    OTP = ""
    for i in range(4):
        OTP += digits[math.floor(random.random() * 10)]
    return OTP


global o
o = 0


def send_otp(request):
    global o
    email = request.POST.get("email")
    print(email)
    o = generateOTP()
    print(o)
    subject = 'OTP for authentication'
    message = 'Your OTP for authentication is {o}'
    from_email = 'ajeeshachu2019@gmail.com'
    recipient_list = [email]

    send_mail(subject, message, from_email, recipient_list, fail_silently=False)


def otp_page(request):
    global o
    error_msg = None
    if request.method == 'POST':
        user_otp = request.POST.get('user_otp')
        print('server otp', o)
        print('user otp', user_otp)
        if o == user_otp:
            return redirect('index')
        else:
            error_msg = 'invalid otp !'
    return render(request, 'otp_page.html', {'error': error_msg})


class Login(View):
    def get(self, request):
        return render(request, 'user_signin.html')

    def post(self, request):
        if 'customer_password' in request.session:
            return redirect('index')
        else:
            email = request.POST.get('email')
            password = request.POST.get('password')
            customer = Customer.get_customer_by_email(email)
            error_msg = None
            if customer:
                flag = check_password(password, customer.password)
                if flag:
                    if customer.active:
                        print(customer.active)
                        request.session['customer_id'] = customer.id
                        # request.session['customer_email'] = customer.email
                        return redirect("index")
                    else:
                        error_msg = 'user is bloked by admin!'
                else:
                    error_msg = 'invalid Email or password..!'
            else:
                error_msg = 'invalid Email or password..!'
        return render(request, 'user_signin.html', {'error': error_msg})


def forgot_password(request):
    return render(request, 'forgot_password.html')


def logout_page(request):
    try:
        # del request.session['customer_id']
        # del request.session['customer_email']
        request.session.clear()
    except KeyError:
        return redirect("index")
    return redirect("user_signin")


def admin_login(request):
    error_msg = None
    if request.method == 'GET':
        return render(request, 'adminlogin.html')
    elif request.user.is_authenticated:
        return redirect('admindashboard')
    else:
        if request.method == 'POST':
            name = request.POST.get('name')
            password = request.POST.get('password')

            user = authenticate(request, username=name, password=password)

            if user is not None:
                login(request, user)
                return redirect('admindashboard')
            else:
                error_msg = 'invalid Name or password..!'

    return render(request, 'adminlogin.html', {'error': error_msg})


def admin_dashboard(request):
    return render(request, 'admindashboard.html')


def admin_logout(request):
    if request.user.is_authenticated:
        logout(request)
    return redirect("adminlogin")


def admin_users(request):
    if request.method == "GET":
        customer = Customer.get_all_customers()
        return render(request, 'admin_users.html', {'customer': customer})


def userblock(request):
    cust_id = request.GET['cust_id']
    check = Customer.objects.filter(id=cust_id)
    for x in check:
        if x.active:
            Customer.objects.filter(id=cust_id).update(active=False)
        else:
            Customer.objects.filter(id=cust_id).update(active=True)
    return redirect(admin_users)


def admin_orders(request):
    return render(request, 'admin_orders.html')


def admin_products(request):
    if request.method == "GET":
        product = Product.objects.all()
        return render(request, 'admin_products.html', {'product': product})


def admin_category(request):
    if request.method == "GET":
        category = Category.get_all_category()
        return render(request, 'admin_categorys.html', {'category': category})


def add_new_product(request):
    if request.method == 'POST':
        name = request.POST.get('name')
        price = request.POST.get('price')
        stoke = request.POST.get('stoke')
        brand = request.POST.get('brand')
        description = request.POST.get('description')
        image = request.FILES.get('image')
        category = request.POST.get('category')
        category = Category.objects.filter(name=category).first()
        Product.objects.create(name=name, price=price, description=description, stoke=stoke, image=image,brand=brand,
                               category=category)
        return redirect('admin_products')
    return render(request, 'add_new_product.html')


def edit_product(request, id):
    prod = Product.objects.get(id=id)
    if request.method == 'POST':
        fm = Product_form(request.POST, request.FILES, instance=prod)
        if fm.is_valid():
            fm.save()
            return redirect('admin_products')
    else:
        fm = Product_form(instance=prod)
        return render(request, 'edit_product.html', {'fm': fm})


def delete_product(request, id):
    prod = Product.objects.get(id=id)
    prod.delete()
    return redirect('admin_products')


def add_new_category(request):
    if request.method == 'POST':
        fm = Category_form(request.POST)
        if fm.is_valid():
            fm.save()
            return redirect('admin_category')
    else:
        fm = Category_form()
        return render(request, 'add_new_category.html', {'fm': fm})


def edit_category(request, id):
    cat = Category.objects.get(id=id)
    if request.method == 'POST':
        fm = Category_form(request.POST, instance=cat)
        if fm.is_valid():
            fm.save()
            return redirect('admin_category')
    else:
        fm = Category_form(instance=cat)
        return render(request, 'edit_category.html', {'fm': fm})


def delete_category(request, id):
    cat = Category.objects.get(id=id)
    cat.delete()
    return redirect('admin_category')


def about_product(request):
    if request.method == 'GET':
        prod_id = request.GET['prod_id']
        prod = Product.objects.filter(id=prod_id)
        return render(request, 'about_product.html', {'prod': prod})
    else:
        name = request.POST.get('name')
        email = request.POST.get('email')
        address = request.POST.get('address')
        pincode = request.POST.get('pincode')
        city = request.POST.get('city')
        phone = request.POST.get('phone')
        landmark = request.POST.get('landmark')
        state = request.POST.get('state')
        
        Our_user.objects.create(name=name, email=email,address=address,pincode=pincode, city=city,phone=phone,landmark=landmark,
                               state=state)
        return redirect('index')
    
def add_to_cart(request):
    item_id = request.POST.get('item_id')
    item = Product.objects.get(id=item_id)
    cart = request.session.get('cart', [])
    cart.append({
        'item_id': item.id,
        'name': item.name,
        'price': item.price,
        'brand': item.brand,
    })
    request.session['cart'] = cart
    print(cart)
    return JsonResponse({'status': 'success'})

def cart_view(request):
    cart = request.session.get('cart', [])
    context = {
        'cart': cart,
    }
    return render(request, 'cart.html', context)