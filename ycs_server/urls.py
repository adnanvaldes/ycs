from django.urls import path
from ycs_server import views

urlpatterns = [
	path("", views.index, name="index")
]