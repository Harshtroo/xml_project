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
from lxml import etree

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
    print(request)
    if request.method == 'POST':
        file1 = request.POST.get('file1')
        file2 = request.POST.get('file2')

        file1_path = f'app_xml/static/xml/{file1}'
        file2_path = f'app_xml/static/xml/{file2}'
        # print("file1_path",file1_path)
        with open(file1_path, 'r') as file1, open(file2_path, 'r') as file2:
            f1_data = file1.readlines()
            f2_data = file2.readlines()
            # print("f2_data======",f2_data)
            file1_content = file1.read()
            # print("file1_content",file1_content)
            file2_content = file2.read()
            # print("file1_content",file2_content)
            i = 0
            
            for line1 in f1_data:
                i += 1
                
                for line2 in f2_data:
                    
                    # matching line1 from both files
                    if line1 == line2: 
                        # print IDENTICAL if similar
                        print("Line ", i, ": IDENTICAL")
                    else:
                        # print("Line ", i, ":")
                        # # else print that line from both files
                        print("\tFile 1:", line1, end='')
                        print("\tFile 2:", line2, end='')
                        file1_data = line1
                        file2_data = line2
                        # print("file 1 data",file1_data)
                        # print("file 2 data====",file2_data)
                    break

        print("******","\n".join(f2_data))
        context = {
            'file1_content': "\n".join(f1_data),
            'file2_content': "\n".join(f2_data),
        }
        
        # with open(file1_path) as f:
        #     content = f.readlines()
        #     print("content=============",content)
        #     xml_file1 = f.write(xmlstr)
        # print("xml_file1====",xml_file1)
        # print("file1",file1_path,"file2",file2_path)
        # breakpoint()

        # tree1 = ET.parse(f'app_xml/static/xml/{file1}')
        # tree2 = ET.parse(f'app_xml/static/xml/{file2}')
        # diff = main.diff_files(f'app_xml/static/xml/{file1}', f'app_xml/static/xml/{file2}',formatter=formatting.XMLFormatter())
        # root = ET.Element('employees')
        # print("diffff==========",diff)
        # print("context",context)
        return JsonResponse(context)

