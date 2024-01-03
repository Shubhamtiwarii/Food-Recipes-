from django.urls import path,include
from . import views

urlpatterns = [
    path('',views.index,name="homepage"),
    path('signup/',views.signup,name="signup"),
    path('login/',views.login,name="login"),
    path('logout/',views.logout,name="logout"),
    path('cart/',views.cart,name="cart"),
    path('check-out/',views.checkout,name="checkout"),
    path('orders/',views.orders,name="orders"),
    path('add-product/',views.addproduct,name="addproduct"),
    path('add-category/',views.addcategory,name="addcategory"),
    path('detail/<int:id>/',views.detail,name='detail'),
    
]