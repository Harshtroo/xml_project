import xml.etree.ElementTree as ET
from django.shortcuts import render, redirect
from django.views.generic import UpdateView,TemplateView,FormView,View
import xmltodict
from django.conf import settings
from django.urls import reverse
from datetime import datetime




def show_xml_file(request):
    with open(settings.XML_FILE_PATH,"r", encoding="utf-8") as file:
        user_xml = file.read()
    user_dict = xmltodict.parse(user_xml)
    user_data = user_dict["employees"]
    for value in user_data["employee"]:
        value["id"] = value["@id"]
        del value["@id"]
    return render(request,"user_list.html", {"user_data" : user_data["employee"]})


class EmployeeEdit(View):
    template_name = "employee_update.html"

    def get(self, request, *args, **kwargs):
        with open(settings.XML_FILE_PATH, "r", encoding="utf-8") as file:
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
        tree = ET.parse('app_xml/static/xml/user_data.xml')
        root = tree.getroot()
        user_id = request.POST["id"]
        employee = root.find(f"./employee[@id='{user_id}']")

        if employee is not None:
            # Update the desired data
            employee.find('firstname').text = request.POST["firstname"]
            employee.find('lastname').text = request.POST["lastname"]
            employee.find('title').text = request.POST["title"]
            employee.find('division').text = request.POST["division"]
            employee.find('building').text = request.POST["building"]
            employee.find('room').text =  request.POST["room"]

            # Save the updated XML back to the file
            current_time = datetime.now().strftime("%Y_%m_%d-%I-%M-%p")
            file_path = f'app_xml/static/xml/user_data-{current_time}.xml'
            tree.write(file_path)
            settings.XML_FILE_PATH = file_path

        return redirect("/")