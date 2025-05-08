from django.urls import path # type: ignore
from .views import *
from django.conf import settings
from django.conf.urls.static import static

urlpatterns = [
    path('', index),
    path('login/',userLogin),
    path('register',userRegister),
    path('details/<petid>',getPetByid),
    path('logout',userlogout),
    path('filter-by-cat/<catName>',filterbycategory),
    path('sort-by-price/<direction>',sortbyprice),
    path('filter-by-range/',filterByRange),
    path('addtocart/<petid>',addToCart),
    path('search/', searchPet),
    path('showMyCart',showMyCart),
    path('removeCart/<cartid>' , removeCart),
    path('apply-coupon/',apply_coupon),
    path('updatequantity/<cartid>/<operation>',updateQuantity),  # taking two thing cart id and opertion can be increment or decremnt 
    path('confirmorder',confirmOrder),
    path('contact/', contact),
    path('make-payment',makePayment),
    path('placeorder/',palceOrder),

]



urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)