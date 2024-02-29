from django.urls import path
from . import views

urlpatterns = [
    path('', views.home, name="home"),
    path('store/', views.store, name="store"),
    path('cart/', views.cart, name="cart"),
    path('checkout/', views.checkout, name="checkout"),
    path('register/', views.registerPage, name="register"),
    path('login/', views.loginPage, name="login"),
    path('logout/', views.logoutUser, name="logout"),
    path('message/', views.message, name="message"),
    path('owner/', views.owner, name="owner"),

    path('forum/', views.forum, name="forum"),
    path('profile/<int:pk>', views.profile, name="profile"),


    path('update_item/', views.updateItem, name="update_item"),
    path('process_order/', views.processOrder, name="update_item"),
]