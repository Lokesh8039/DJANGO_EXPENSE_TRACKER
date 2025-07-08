from .views import index,delete, login_view,register_view,logout_view
from django.urls import path

urlpatterns = [
    path("",index , name="home"),
    path("login/",login_view , name = "login_view"),
    path("logout/",logout_view , name = "logout_view"),
    path("register/",register_view , name = "register_view"),
    path("/<int:id>",delete,name = "delete_transaction")
]
