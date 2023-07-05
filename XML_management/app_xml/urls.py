from django.urls import path
from app_xml import views


urlpatterns = [
    path("", views.show_xml_file, name="show_xml"),
    path("edit_employee/<str:id>/",views.EmployeeEdit.as_view(),name="edit_employee"),
    path("delete_employee/<str:id>/", views.EmployeeDelete.as_view(), name="delete_employee"),
    path("add_employee/",views.EmployeeAdd.as_view(),name="add_employee"),
]
