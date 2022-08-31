from unicodedata import name
from xml.dom.minidom import Document
from django.conf import settings
from django.contrib import admin
from django.urls import path
from . import views


urlpatterns = [
    path("",views.cards,name="cards"),
    path("product/",views.product,name="product"),
    path("about/",views.about,name='about'),
    path("contact/",views.contact,name="contact"),
    path("checklist/<int:id>",views.checklist,name="department"),
    path("order/",views.orders,name="order"),
    path("search/",views.search,name="search"),
    path("signup/",views.signup,name="signup"),
    path("login/",views.userlogin,name="login"),
    path("logout/",views.userlogout,name="logout"),
    path("review/",views.reviews,name="reviews"),
    path("orderdetails/",views.orderdetails,name="orderdetails"),
    path("confirm/",views.confirm,name="confirm"),
    path("track/",views.trackorder,name="track"),
    path("profile/",views.userprofile,name="userprofile"),
    path("feedback/",views.userfeedback,name="userfeedback"),
]