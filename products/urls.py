from django.urls import path
from . import views

urlpatterns = [
       
        path("show/<str:id>",views.show,name="show")
]

