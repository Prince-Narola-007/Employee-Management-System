from django.shortcuts import render, HttpResponse
from .models import Employee
from datetime import datetime
from django.db.models import Q


def index(request):
    return render(request, 'index.html')


def all_emp(request):
    emps = Employee.objects.all()
    context = {'emps': emps}
    print(context)
    return render(request, 'all_emp.html', context)


def add_emp(request):

    if request.method == "POST":
        first_name = request.POST['first_name']
        last_name = request.POST['last_name']
        phone = request.POST['phone']
        salary = request.POST['salary']
        bonus = request.POST['bonus']
        dept = request.POST['dept']
        role = request.POST['role']

        new_emp = Employee(first_name=first_name, last_name=last_name, phone=phone,
                           salary=salary, bonus=bonus, dept_id=dept, role_id=role, hire_date=datetime.now())
        new_emp.save()
        return HttpResponse("added successfully")

    elif (request.method == "GET"):
        return render(request, 'add_emp.html')

    else:
        return HttpResponse("failed to added")


def remove_emp(request, emp_id=0):
    if emp_id:
        try:
            remove_the_emp = Employee.objects.get(id=emp_id)
            remove_the_emp.delete()
            return HttpResponse("Removed Successfully")
        except:
            return HttpResponse("Something Wrong!!")

    emps = Employee.objects.all()
    context = {'emps': emps}
    return render(request, 'remove_emp.html', context)


def filter_emp(request):
    if request.method == "POST":
        name = request.POST['name']
        dept = request.POST['dept']
        role = request.POST['role']

        emps = Employee.objects.all()

        if name:
            emps = emps.filter(Q(first_name__icontains=name)
                               | Q(last_name__icontains=name))

        if dept:
            emps = emps.filter(dept__name__icontains=dept)

        if role:
            emps = emps.filter(role__name__icontains=role)

        context = {'emps': emps}

        return render(request, "all_emp.html", context)

    elif request.method == "GET":
        return render(request, 'filter_emp.html')

    else:
        return HttpResponse("exception occur")
