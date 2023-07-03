from django.shortcuts import render, redirect
from django.views.generic.edit import UpdateView
import xmltodict
from django.urls import reverse

def show_xml_file(request):
    with open("/home/ashishv/XML_project/XML_management/app_xml/user_data.xml","r", encoding="utf-8") as file:
        user_xml = file.read()
    user_dict = xmltodict.parse(user_xml)
    user_data = user_dict["employees"]
    for value in user_data["employee"]:
        value["id"] = value["@id"]
        del value["@id"]
    return render(request,"user_list.html", {"user_data" : user_data["employee"]})


class EmployeeEdit(UpdateView):
    # success_url = reverse("show_xml")

    def get(self, request, *args, **kwargs):
        print("hello")
        return redirect("show_xml/")
