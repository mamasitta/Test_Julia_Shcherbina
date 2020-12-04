import csv
import os
from io import StringIO
from os.path import join

from django.contrib import auth
from django.contrib.auth import logout
from django.contrib.auth.decorators import login_required
from django.core.files.base import ContentFile, File
from django.shortcuts import render, redirect
from django.http import HttpResponse

# Create your views here.

# main page

from .models import CsvStorage


@login_required
def index(request):
    user_schemas = CsvStorage.objects.all()
    counter = []
    for i in range(len(user_schemas)):
        counter.append(i + 1)

    return render(request, "test_app/index.html", {"user_schemas": user_schemas, "counter": counter})


def schema_delete(request, schema_id):
    if schema_id != 0:

        schema = CsvStorage.objects.get(id=schema_id)
        schema_path = schema.file_path
        print(schema_path)

        os.remove(r"{}".format(schema_path))
        schema.delete()
        return redirect('index')
    redirect('index')


@login_required
def create_schema(request):
    user_id = request.user.id
    if request.method == 'POST':
        # registering dialect for csv
        column_separator = request.POST.get('column_separator')
        string_character = request.POST.get('string_character')
        if column_separator == "Semicolon(;)":
            if string_character == 'Double-quote(")':
                csv.register_dialect('myDialect', delimiter=';', quotechar='"', quoting=csv.QUOTE_NONNUMERIC)
            else:
                csv.register_dialect('myDialect', delimiter=';', quotechar="'", quoting=csv.QUOTE_NONNUMERIC)
        elif column_separator == "Slash(/)":
            if string_character == 'Double-quote(")':
                csv.register_dialect('myDialect', delimiter='/', quotechar='"', quoting=csv.QUOTE_NONNUMERIC)
            else:
                csv.register_dialect('myDialect', delimiter='/', quotechar="'", quoting=csv.QUOTE_NONNUMERIC)
        else:
            if string_character == 'Double-quote(")':
                csv.register_dialect('myDialect', delimiter=',', quotechar='"', quoting=csv.QUOTE_NONNUMERIC)
            else:
                csv.register_dialect('myDialect', delimiter=',', quotechar="'", quoting=csv.QUOTE_NONNUMERIC)
        # processing data for csv
        schema_name = request.POST.get('name')
        add_number = int(request.POST.get('add_number'))
        data_to_file = []
        for i in range(add_number*3):
            data_to_file.append("remove")
        for i in range(add_number):
            name = request.POST.get('name{}'.format(i))
            order = request.POST.get('order{}'.format(i))
            if not order:
                order =len(data_to_file)
            type = request.POST.get('type{}'.format(i))
            if type == "Integer":
                range_from = request.POST.get('range_from{}'.format(i))
                range_to = request.POST.get('range_till{}'.format(i))
                data_to_file.insert(int(order), name)
                data_to_file.insert(int(order)+1, range_from)
                data_to_file.insert(int(order)+2, range_to)
                print(data_to_file)
            else:
                print(data_to_file)
                data_to_file.insert(int(order), name)
        data_to = ([s for s in data_to_file if s != 'remove'])
        file_path = 'media/uploads/{}.csv'.format(schema_name)
        with open(file_path, "w") as file:
            writer = csv.writer(file, dialect='myDialect')
            writer.writerow(data_to)
        file.closed
        new_file_obj = CsvStorage(user_create_id=user_id, file_name=schema_name, file_path=file_path)
        new_file_obj.save()
        return redirect("index")
    return render(request, "test_app/crete_schema.html", {"user": request.user.username})


def logout_view(request):
    logout(request)
    return redirect('login')


# login view
def login(request):
    if request.user.is_authenticated:
        return redirect('index')
    if request.method == 'POST':
        username = request.POST.get('username')
        password = request.POST.get('password')
        user = auth.authenticate(username=username, password=password)
        if user is not None:
            auth.login(request, user)
            return redirect('index')
        else:
            return render(request, 'test_app/login.html', {'message': "Invalid username or password"})
    return render(request, "test_app/login.html")


@login_required
def data_sets(request):
    return render(request, "test_app/data_sets.html")


def some_view(request):
    # Create the HttpResponse object with the appropriate CSV header.
    response = HttpResponse(content_type='text/csv')
    response['Content-Disposition'] = 'attachment; filename="somefilename.csv"'

    writer = csv.writer(response)
    writer.writerow(['First row', 'Foo', 'Bar', 'Baz'])
    writer.writerow(['Second row', 'A', 'B', 'C', '"Testing"', "Here's a quote"])

    return response