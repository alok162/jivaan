from django.urls import path, include, re_path
from employee import views

urlpatterns = [re_path(r"^/$", views.EmployeeChunk.as_view())]

