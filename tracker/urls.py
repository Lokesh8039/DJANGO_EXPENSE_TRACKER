from .views import index,delete
from django.urls import path

urlpatterns = [
    path("",index , name="home"),
    path("/<int:id>",delete,name = "delete_transaction")
]
