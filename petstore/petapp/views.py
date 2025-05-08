from django.shortcuts import render, redirect # type: ignore 
from .models import Pet, Cart,Order
from django.contrib.auth.models import User
from django.contrib.auth import authenticate,login,logout
from django.db.models import Q
import razorpay
import uuid
from django.core.mail import send_mail
from django.contrib.messages import add_message,Message
from django.contrib import messages


# Create your views here.

def index(request):
    user=request.user
    request.session.pop('usessionid', None)
    #None is the default value to return if the key doesn't exist. agr usersession nhi raha tho none dedo 
    print("user loggen in ",user.is_authenticated)
    
    data=Pet.objects.all()

    # type = Pet.objects.all(type=type)
    # print(type)
    return render (request,'index.html',{'data':data})




def userLogin(request):
    if request.method=='GET':
        return render(request,'login.html')
    else:
        u=request.POST['name']
        p=request.POST['password']
        user= authenticate(username=u,password=p)
        # print("login user after authentication ", user)   if present it will give me name and not present it will give me none
        '''
        authencicate will chck the credtials is correct 
        and
        login wil do login with the authecicate is done 
        '''
      
        if user is not None:
            login(request,user)
            return redirect('/')
        else:
            context={}
            context['error']="plz enter the valid credentials"
            return render(request,'login.html',context)
        


def userlogout(request):
    logout(request)
    return redirect('/')

def userRegister(request):
    if request.method=='GET':
        return render(request,'register.html')
    else:
        """
        1. fetch the form data
        2. save the data in user table
        3. if succesfull ... login page , else register page

        """
        u= request.POST['Name'].strip()
        e= request.POST['Email'].strip()
        p= request.POST['Password'].strip()
        cp= request.POST['Confirmpassword'].strip()

        context={}

        if u =="" or p=="" or  cp=="" or e=="" :
            context['error']= "all the fields are compulsary "
            return render(request, 'register.html', context)
        elif p != cp:
            context['error']='password and confirm passmust be same'
            return render(request, 'register.html', context)
        elif  User.objects.filter(username=u).exists():
            context['error']='user already exist'
            return render(request, 'register.html', context)
        elif  User.objects.filter(email=e).exists():
            context['error']='email alrady exist '
            return render(request, 'register.html', context)

        else:
            user= User.objects.create(username=u,email=e)
            user.set_password(p)
            user.save()
            return redirect('/login')


def getPetByid(request,petid):
    context={}
    petOBj=Pet.objects.get(id=petid)
    context['pet']=petOBj
    return render(request,'details.html',context)

def filterbycategory(request, catName):
    data = Pet.objects.filter(type=catName)
    request.session['catsession'] = catName  #  store name, not list
    request.session['usessionid'] = []  #Clear the old list

    return render(request, 'index.html', {'data': data})



def sortbyprice(request, direction):
    usessionid = request.session.get('usessionid', [])  # second arguments is empty list if usession is not present
    catsession = request.session.get('catsession', None) # second arguments is none if categiry is not selected 

    # Set sort column
    column = 'price' if direction == 'asc' else '-price'

    # Priority: usessionid > catsession > all
    if usessionid:
        data = Pet.objects.filter(id__in=usessionid).order_by(column)
        '''
        agr usesseion h tho chck karega ki id__in ke andar jo id h aur user ka jo id h usko filter
        matlb sirf vo hi id rehge jo user ne search karke store kiya h 
        '''

    elif catsession:
        data = Pet.objects.filter(type=catsession).order_by(column)
        '''
        catsesion ke andar dog ya cat hoga aur vo mera type se filter karega
        type ke andar jo presently selected category store hogi 
        '''

    else:
        data = Pet.objects.order_by(column)

    return render(request, 'index.html', {'data': data})

    # usessionid = request.session.get('usessionid',[])
    # catsession= request.session.get('catsession',[])
    # if usessionid:
    #     if direction=='asc':
    #         column='price'
    #     else:
    #         column='-price'
    #     data=Pet.objects.filter(Q(id__in=usessionid)).order_by(column)
    #     return render (request,'index.html',{'data':data})
    # elif catsession:
    #         if direction=='asc':
    #             column='price'
    #         else:
    #             column='-price'
    #         data=Pet.objects.filter(type=catsession).order_by(column)
    #         return render (request,'index.html',{'data':data})
    # else:
    #     if direction=='asc':
    #         column='price'
    #     else:
    #         column='-price'
    #     data=Pet.objects.order_by(column)
    #     return render (request,'index.html',{'data':data})


def filterByRange(request):
    min= request.GET['min']
    max= request.GET['max']
    '''
    min=100 and max=600
    select * from __ where price >= min and price<= max and ;
    select * from 

    '''


    c1= Q(price__gte=min) # Q is used  for filter using keyword (AND < OR <  )
    c2= Q(price__lte=max)
    usessionid = request.session.get('usessionid',[])
    q = Q(id__in=usessionid)  # check if pet's id is in the stored list
    '''
    SELECT * FROM pet WHERE id IN (2, 4, 6); for example 
    gte is greater than equal
    lte is less than equal
    '''

    if usessionid:

        # Filter within previously searched results
        q = Q(id__in=usessionid)
        data = Pet.objects.filter(q & c1 & c2)
        if not data.exists():
         notfound = f"No pets found in your search between ₹{min} and ₹{max}"
         return render(request, 'index.html', {'notfound': notfound})
        
    else:
        # If no search was done, filter all pets by price range
        data = Pet.objects.filter(c1 & c2)
        if not data.exists():
         notfound = f"No pets found in your search between ₹{min} and ₹{max}"
         return render(request, 'index.html', {'notfound': notfound})
    return render (request,'index.html',{'data':data})

def addToCart(request,petid):
    selectedPetObject=Pet.objects.get(id=petid)
    # cartall= .objects.get(id=petid)
    # if petid in selectedPetObject:
    #     error= 'already is cart'
    #     return render (request,'index.html',{'error':error} )
    userid= request.user.id
    if userid is not None:
        loggedInUserObject = User.objects.get(id=userid)
        cart = Cart.objects.create(
            uid=loggedInUserObject,
            pid=selectedPetObject

        )

        cart.save()
        return redirect('/')
    

        

    else:
        # error="please login"
        return redirect('/login')
    
   
        # return render(request,'login.html',{'error':error})

def searchPet(request):
    query= request.GET['query'].strip()
    data=Pet.objects.filter(Q(breed__icontains=query))

    if query=='':
        error=f'{query} is not found not valid input'
        return render(request,'index.html',{'error':error})
    
    elif data.exists():
        request.session['usessionid'] = list(data.values_list('id', flat=True))   
        '''
        values_list():
        This is a Django QuerySet method that returns a list of specific field values from your model, instead of full model instances.

        'id':
        This is the field name you're extracting. In this case, it's the id field of the Pet model (usually the primary key).

        Pet.objects.values_list('id')
        This returns: 
        [(1,), (2,), (3,), (4,)]

        Pet.objects.values_list('id', flat=True)
        This returns:
        [1, 2, 3, 4]



        '''
        return render (request,'index.html',{'data':data})
    else:
        error=f'{query} is not found '
        return render(request,'index.html',{'error':error})



def showMyCart(request):
    userid=request.user.id
    # user=User.objects.get(id=userid)
    mycart=Cart.objects.filter(uid=userid)
    count=len(mycart)
    totalBill=0
    for cart in mycart:
        totalBill += cart.pid.price  *  cart.quantity

    request.session['totalBill']=totalBill

    return render(request,'mycart.html',{'mycart':mycart , 'count':count ,'totalBill':totalBill})
    

def removeCart(request,cartid):
    mycart = Cart.objects.filter(id=cartid)
    mycart.delete()
    return redirect('/showMyCart')
     

coupon_code_list={'save100':100,'save500':500}
def apply_coupon(request):
    action = request.POST.get('action')  # 'apply' or 'remove'
    coupon_code = request.POST.get('coupon_code', '').strip()
    userid = request.user.id
    mycart = Cart.objects.filter(uid=userid)
    count = len(mycart)
    discount=0

    # Base total before any discount
    totalBill = sum(cart.pid.price * cart.quantity for cart in mycart)

    applied_coupon = False
    coupon_attempted = False
    error = ''

 
    if action == 'apply':
        coupon_attempted = True

        if count >= 1:
            if coupon_code in coupon_code_list:
                applied_coupon = True
                discount = coupon_code_list[coupon_code]
                totalBill = max(totalBill - discount,0)
                # request.session['applied_coupon'] = True
                request.session['totalBill'] = totalBill
            else:
                error = "Invalid coupon code"
        else:
            error = "Please add items to cart before applying a coupon"
            coupon_attempted = False

    elif action == 'remove':
        applied_coupon = False
        request.session['applied_coupon'] = False
        request.session['totalBill'] = totalBill  # reset full price
        coupon_attempted = False
        

    # Always update session to current total
    request.session['totalBill'] = totalBill
    print(totalBill)

    return render(request, 'mycart.html', {
        'totalBill': totalBill,
        'applied_coupon': applied_coupon,
        'mycart': mycart,
        'count': count,
        'coupon_attempted': coupon_attempted,
        'error': error,
        'discount':discount,
        'coupon_code':coupon_code
    })





def updateQuantity(request,cartid,operation):
    cart= Cart.objects.filter(id=cartid)
    print(cart)

    for i in cart:
        print(i)
    if operation == 'incr':
        q = cart[0].quantity
        cart.update(quantity=q+1)
        return redirect('/showMyCart')
    # if operation == 'decr':
    else:
        q = cart[0].quantity

        cart.update(quantity=q-1)
        return redirect('/showMyCart')


def confirmOrder(request):
    
    userid=request.user.id
    # user=User.objects.get(id=userid)
    mycart=Cart.objects.filter(uid=userid)
    count=len(mycart)
    totalBill= request.session.get('totalBill',None)
    print(totalBill)

    return render(request,'confirm.html',{'mycart':mycart , 'count':count ,'totalBill':totalBill})


def contact(request):
    return render(request,'contact.html')


def makePayment(request):
    '''we need ti add the detail in the order table 
    1. get the cureent  loged in user id 
    2.basesd on the get the cart detail of that user 
    3.find out the total billl amout for this user 
    4. define model order 
    '''
    userid = request.user.id
    data = Cart.objects.filter(uid=userid)

    totalBill= request.session.get('totalBill',None)
    # totalBill = sum(cart.pid.price * cart.quantity for cart in data)
    client = razorpay.Client(auth=("rzp_test_uWbBTFmHqIi9dN","6EV65YVkhZTGRmAlqLhpsWl2"))
    
    data = {
        'amount': int(totalBill) * 100,
        'currency': "INR" ,
        'receipt': ''
    }


    payement =  client.order.create(data=data)
    print(payement)
    context ={}

    context['data'] = payement

    return render(request,'pay.html', context)


def palceOrder(request):
    userid = request.user.id
    orderid=uuid.uuid4()
    cart_list = Cart.objects.filter(uid=userid)
    totallBill= request.session.get('totalBill',None)
    for cart in cart_list:
        order=Order.objects.create(orderid=orderid,userid=cart.uid, petid=cart.pid,quantity=cart.quantity,totallBill=totallBill)
        order.save()

    cart_list.delete()


    subject = 'Order Confirmation – Thank You for Your Purchase!'
    order_id_str = str(orderid)
    message = (
        f"Hi {request.user.username},\n\n"
        f"Thank you for placing your order with us!\n"
        f"Your order ID is: {order_id_str}\n\n"
        "We will notify you once your order is shipped.\n\n"
        "Best regards,\n"
        "petStore"
    )

    send_mail(
        subject,
        message,
        'adityask080@gmail.com',
        [request.user.email, ],
        fail_silently=False,
    )
    messages.info(request, 'order has been placed succesfully ')  # ✅ Correct way
    return  redirect('/')


