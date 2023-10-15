import xml.etree.ElementTree as ET
from django.shortcuts import render, redirect
from django.views.generic import View
import xmltodict
from django.conf import settings
from django.urls import reverse
from datetime import datetime
import glob
import os
from django.http import JsonResponse
from django.core.paginator import Paginator
import xmltodict


def get_latest_file():
    files = glob.glob(settings.XML_FILE_PATH)
    return max(files, key=os.path.getctime)


def read_file_data(request, file_name):
    with open(file_name, "r", encoding="utf-8") as file:
        try:
            user_xml = file.read()

            user_dict = xmltodict.parse(user_xml)
            user_data = user_dict["employees"]

            for value in user_data["employee"]:
                value["id"] = value["@id"]
                del value["@id"]
            return user_data["employee"]

        except Exception as e:
            return JsonResponse({"error_message": str(e)}, status=400)


def show_xml_file(request):
    latest_file_path = get_latest_file()
    file_data = read_file_data(request, latest_file_path)
    return render(request, "user_list.html", {"user_data": file_data})


class EmployeeEdit(View):
    template_name = "employee_update.html"

    def get(self, request, *args, **kwargs):
        latest_file_path = get_latest_file()
        with open(latest_file_path, "r", encoding="utf-8") as file:
            try:
                user_xml = file.read()
                user_dict = xmltodict.parse(user_xml)
                user_data = user_dict["employees"]
                for value in user_data["employee"]:
                    employee_id = value["@id"]
                    if employee_id == self.kwargs["id"]:
                        select_employee_data = {"id": value.get("@id"),
                                                "firstname": value.get("firstname"),
                                                "lastname": value.get("lastname"),
                                                "title": value.get("title"),
                                                "division": value.get("division"),
                                                "building": value.get("building"),
                                                "room": value.get("room"), }
                return render(request, self.template_name, {"select_employee_data": select_employee_data})
            except Exception as e:
                return JsonResponse({"error_message": str(e)}, status=400)

    def post(self, request, *args, **kwargs):
        latest_file_path = get_latest_file()
        tree = ET.parse(latest_file_path)
        root = tree.getroot()
        user_id = request.POST["id"]
        employee = root.find(f"./employee[@id='{user_id}']")
        try:
            if employee is not None:
                # Update the desired data
                employee.find('firstname').text = request.POST["firstname"]
                employee.find('lastname').text = request.POST["lastname"]
                employee.find('title').text = request.POST["title"]
                employee.find('division').text = request.POST["division"]
                employee.find('building').text = request.POST["building"]
                employee.find('room').text = request.POST["room"]

                # Save the updated XML back to the file
                current_time = datetime.now().strftime("%Y_%m_%d-%I-%M-%S")
                file_path = f'app_xml/static/xml/user_data-{current_time}.xml'
                tree.write(file_path)
                settings.XML_FILE_PATH = file_path

            return redirect("/")

        except Exception as e:
            return JsonResponse({"error_message": str(e)}, status=500)


class EmployeeDelete(View):

    def get(self, request, *args, **kwargs):
        latest_file_path = get_latest_file()
        try:
            tree = ET.parse(latest_file_path)
            root = tree.getroot()
            user_id = self.kwargs["id"]
            for country in root.findall('employee'):
                val_to_delete = country.attrib['id']
                if val_to_delete == user_id:
                    root.remove(country)
            current_time = datetime.now().strftime("%Y_%m_%d-%I-%M-%S")
            file_path = f'app_xml/static/xml/user_data-{current_time}.xml'
            tree.write(file_path)
            settings.XML_FILE_PATH = file_path
            return redirect("/")
        # return JsonResponse({"messages": "success"})
        except Exception as e:
            return JsonResponse({"error_message": str(e)}, status=400)


class EmployeeAdd(View):
    template_name = "user_list.html"

    def get(self, request, *args, **kwargs):
        return render(request, self.template_name)

    def post(self, request, *args, **kwargs):
        try:
            latest_file_path = get_latest_file()
            tree = ET.parse(latest_file_path)
            root = tree.getroot()

            user_id = request.POST["id"]
            existing_employee_ids = [employee.attrib.get("id") for employee in root.findall("employee")]
            if user_id in existing_employee_ids:
                error_message = f"Employee with ID '{user_id}' already exists."
                return JsonResponse({"error": error_message}, status=400)

            employee = ET.Element("employee")
            employee.set("id", request.POST["id"])

            firstname = ET.SubElement(employee, "firstname")
            firstname.text = request.POST["firstname"]

            lastname = ET.SubElement(employee, "lastname")
            lastname.text = request.POST["lastname"]

            title = ET.SubElement(employee, "title")
            title.text = request.POST["title"]

            division = ET.SubElement(employee, "division")
            division.text = request.POST["division"]

            building = ET.SubElement(employee, "building")
            building.text = request.POST["building"]

            room = ET.SubElement(employee, "room")
            room.text = request.POST["room"]

            # Append the new employee element to the root
            root.append(employee)
            # Save the updated XML back to the file
            current_time = datetime.now().strftime("%Y_%m_%d-%I-%M-%S")
            file_path = f'app_xml/static/xml/user_data-{current_time}.xml'
            tree.write(file_path)
            settings.XML_FILE_PATH = file_path
            # return redirect("/")
            return JsonResponse({"message": "success"})
        except Exception as e:
            return JsonResponse({"error_message": str(e)}, status=400)


def xml_list(request):
    path = 'app_xml/static/xml'
    xml_of_list = os.listdir(path)

    paginator = Paginator(xml_of_list, 5)
    page_number = request.GET.get("page")
    page_obj = paginator.get_page(page_number)

    return render(request, "xml_file_list.html", {"xml_of_list": xml_of_list, "page_obj": page_obj})


def compare_xml(request):
    if request.method == 'POST':
        file1 = request.POST.get('file1')
        file2 = request.POST.get('file2')

        file1_path = f'app_xml/static/xml/{file1}'
        file2_path = f'app_xml/static/xml/{file2}'

        with open(file1_path, 'r') as file1, open(file2_path, 'r') as file2:

            file1_read = file1.read()
            file2_read = file2.read()

            file1_dict = xmltodict.parse(file1_read)
            file2_dict = xmltodict.parse(file2_read)

            file1_data = file1_dict["employees"]
            file2_data = file2_dict["employees"]

            for value in file1_data["employee"]:
                value["id"] = value["@id"]
                del value["@id"]

            for value in file2_data["employee"]:
                value["id"] = value["@id"]
                del value["@id"]

            # tree1 = ET.parse(file1_path)
            # root1 = tree1.getroot()
            #
            # tree2 = ET.parse(file2_path)
            # root2 = tree2.getroot()

            file1_dict_data = []
            file2_dict_data = []

            # get file 1 dict data
            for key,value in file1_dict.items():
                for key1,value1 in value.items():
                    for nodes in value1:
                        file1_dict_data.append(nodes)

            # get file 2 dict data
            for key,value in file2_dict.items():
                for key1,value1 in value.items():
                    for nodes in value1:
                        file2_dict_data.append(nodes)

            insertions = []
            updates = []
            deletions = []

            dict1 = {idx: dict_item for idx, dict_item in enumerate(file1_dict_data)}
            dict2 = {idx: dict_item for idx, dict_item in enumerate(file2_dict_data)}

            for key, value in dict2.items():
                if key not in dict1:
                    insertions.append(value)
                else:
                    dict1_value = dict1[key]
                    if value != dict1_value:
                        # for key in dict1_value:
                        #     if key in value and dict1_value[key] != value[key]:
                        #         different_pairs = value[key]
                        #         # print("id=====",value["id"])
                        #         print("<<<<<<<<<<<<<<",different_pairs + value["id"])
                        #         updates.append(different_pairs)
                        #         updates.append(value["id"])
                        updates.append(value)
            for key, value in dict1.items():
                if key not in dict2:
                    deletions.append(value)

            insertions = [d for d in insertions if d not in deletions]
            deletions = [d for d in deletions if d not in insertions]
            context = {
                "file1_data": file1_data["employee"],
                "file2_data": file2_data["employee"],
                "updates": updates,
                "deletions": deletions,
                "insertions": insertions,
            }
        return JsonResponse(context)








