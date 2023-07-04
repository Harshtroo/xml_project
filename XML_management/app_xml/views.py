import xml.etree.ElementTree as ET
from django.shortcuts import render, redirect
from django.views.generic import UpdateView,TemplateView,FormView
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


class EmployeeEdit(FormView):
    template_name = "employee_update.html"
    # success_url = reverse("show_xml")

    def get(self, request, *args, **kwargs):
        with open("/home/ashishv/XML_project/XML_management/app_xml/user_data.xml", "r", encoding="utf-8") as file:
            user_xml = file.read()
        user_dict = xmltodict.parse(user_xml)
        user_data = user_dict["employees"]
        for value in user_data["employee"]:
            employee_id = value["@id"]
            if employee_id == self.kwargs["id"] :
                select_employee_data = {"id":value.get("@id"),
                                        "firstname": value.get("firstname"),
                                        "lastname": value.get("lastname"),
                                        "title": value.get("title"),
                                        "division": value.get("division"),
                                        "building": value.get("building"),
                                        "room": value.get("room"),}
        return render(request,self.template_name,{"select_employee_data": select_employee_data})

    def post(self, request, *args, **kwargs):
        print("post_data=============",request.POST)

        employees = ET.Element("employees")
        employee = ET.SubElement(employees,"employee",id=request.POST["id"])

        firstname = ET.SubElement(employee,'firstname')
        lastname = ET.SubElement(employee,"lastname")
        title = ET.SubElement(employee,"title")
        division = ET.SubElement(employee,"division")
        building = ET.SubElement(employee,"building")
        room = ET.SubElement(employee,"room")

        firstname.text = request.POST["firstname"]
        lastname.text = request.POST["lastname"]
        title.text = request.POST["title"]
        division.text = request.POST["division"]
        building.text = request.POST["building"]
        room.text = request.POST["room"]

        tree = ET.ElementTree(employees)

        tree.write(f"user_data.xml")

        return redirect("/")