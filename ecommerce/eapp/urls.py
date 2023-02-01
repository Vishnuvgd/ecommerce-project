from django.urls import path
from .views import *

urlpatterns = [
 path('',index),
 path('userlogin/',userlog),
 path('register/',register),
 path('shoplog/',shoplog),
 path('shopreg/',shopreg),
 path('shopregdisplay/',spregdiplay),
 path('editshopreg/<int:id>',editshopreg),
 path('editregister/<int:id>',editregister),
 path('upload/',itemupload),
 path('uploaddisplay/',uploaddiplay),
 path('userview/',userview),
 path('productdel/<int:id>',productdel),
 path('productedit/<int:id>',productedit),
 path('addtocart/<int:id>',addcart),
 path('cartdisplay/',cartdisplay),
 path('itemremove/<int:id>',itemremove),
 path('itembuy/<int:id>',itembuy),
 path('profilepage/',profile),
 path('userprofile/',userprofile)
]