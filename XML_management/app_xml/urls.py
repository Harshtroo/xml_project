from django.urls import path
from .views import *
from app_xml import views


urlpatterns = [
    path("", views.show_xml_file, name="show_xml"),
    path("edit_employee",views.EmployeeEdit.as_view(),name="edit_employee"),
]
