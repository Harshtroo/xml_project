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
from xmldiff import main, formatting
import xmltodict

def get_latest_file():
    files = glob.glob(settings.XML_FILE_PATH)
    return max(files, key=os.path.getctime)


def show_xml_file(request):
    latest_file_path = get_latest_file()
    with open(latest_file_path,"r", encoding="utf-8") as file:
        try:
            user_xml = file.read()

            user_dict = xmltodict.parse(user_xml)
            user_data = user_dict["employees"]

            for value in user_data["employee"]:
                value["id"] = value["@id"]
                del value["@id"]
            return render(request,"user_list.html", {"user_data": user_data["employee"]})
        except Exception as e:
            return JsonResponse({"error_message": str(e)}, status=500)


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
                                                "room": value.get("room"),}
                return render(request,self.template_name,{"select_employee_data": select_employee_data})
            except Exception as e:
                return JsonResponse({"error_message": str(e)}, status=500)

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
            return JsonResponse({"error_message": str(e)}, status=500)


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
            return JsonResponse({"error_message": str(e)}, status=500)


def xml_list(request):

    path = 'app_xml/static/xml'
    xml_of_list = os.listdir(path)

    paginator = Paginator(xml_of_list, 5)
    page_number = request.GET.get("page")
    page_obj = paginator.get_page(page_number)

    return render(request, "xml_file_list.html", {"xml_of_list": xml_of_list,"page_obj": page_obj})


def compare_xml(request):
    if request.method == 'POST':
        file1 = request.POST.get('file1')
        file2 = request.POST.get('file2')

        tree1 = ET.parse(f'app_xml/static/xml/{file1}')
        tree2 = ET.parse(f'app_xml/static/xml/{file2}')
        diff = main.diff_files(f'app_xml/static/xml/{file1}', f'app_xml/static/xml/{file2}',formatter=formatting.XMLFormatter())
        root = ET.Element('employees')
        print("diffff==========",diff)
        # for change in diff:
        #     print(change)
            # for pair in change:
            #     action, attributes = pair[0], pair[1]
            # print("tree===========",tree)
            # for action, attributes in change:
            #     action_element = ET.SubElement(root, action)
            #     for attr_name, attr_value in attributes.items():
            #         attr_element = ET.SubElement(action_element, attr_name)
            #         attr_element.text = attr_value
            # tree = ET.ElementTree(root)
        # diff_formatted = formatting(diff, indent=4)

        # Print the differences
        # print("diff_formatted=============00",diff_formatted)

        # root1 = tree1.getroot()
        # root2 = tree2.getroot()

        # new_elements = compare_elements(root1, root2)
        # print('---new_elements--',new_elements)
        return render(request,"xml_file_list.html", {"diff":diff})

    #     context = {
    #         'tree1': root1,
    #         'tree2': root2,
    #         'new_elements': new_elements
    #     }

    #     return render(request, 'xml_file_list.html', context)

    # return render(request, 'xml_file_list.html')

    # def compare_elements(elem1, elem2):
    #     if elem1.tag != elem2.tag:
    #         print("Element tag differs: '{}' != '{}'".format(elem1.tag, elem2.tag))
    #         return True
    #
    #     if elem1.text != elem2.text:
    #         print("Element text differs: '{}' != '{}'".format(elem1.text, elem2.text))
    #         return True
    #
    #     if elem1.attrib != elem2.attrib:
    #         print("Element attributes differ: '{}' != '{}'".format(elem1.attrib, elem2.attrib))
    #         return True
    #
    #     if len(elem1) != len(elem2):
    #         print("Number of child elements differs: '{}' != '{}'".format(len(elem1), len(elem2)))
    #         return True
    #
    #     for child1, child2 in zip(elem1, elem2):
    #         if compare_elements(child1, child2):
    #             return True
    #
    #     return False