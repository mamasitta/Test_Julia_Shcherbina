import ast
import csv
import os
import threading
from ast import literal_eval
from datetime import date
from io import StringIO
from os.path import join

from celery.result import AsyncResult
from rest_framework import status
from rest_framework.decorators import api_view
from rest_framework.response import Response

from test_app.task import creation_task
from django.contrib import auth
from django.contrib.auth import logout
from django.contrib.auth.decorators import login_required
from django.core.files.base import ContentFile, File
from django.shortcuts import render, redirect
from django.http import HttpResponse, JsonResponse

# Create your views here.

# main page
from test_app.helpers.csv import to_list
from .models import Schema


@login_required
def index(request):
    user_schemas = Schema.objects.all()
    counter = []
    for i in range(len(user_schemas)):
        counter.append(i + 1)
    return render(request, "test_app/index.html", {"user_schemas": user_schemas, "counter": counter})


@login_required
def schema_delete(request, schema_id):
    if schema_id != 0:
        # deleting from db
        schema = Schema.objects.get(id=schema_id)
        schema_path = schema.file_path
        # deleting from media
        os.remove(r"{}".format(schema_path))
        schema.delete()
        return redirect('index')
    redirect('index')


@login_required
def create_schema(request):
    user_id = request.user.id
    if request.method == 'POST':
        # processing data for csv
        column_separator = request.POST.get('column_separator')
        string_character = request.POST.get('string_character')
        schema_name = request.POST.get('name')
        add_number = int(request.POST.get('add_number'))
        data_to_file = []
        # creating list and inserting it with max items (if all integers each need 3 column)
        for i in range(add_number * 3):
            data_to_file.append("remove")
        # get data for csv (names created by java script)
        for i in range(add_number):
            name = request.POST.get('name{}'.format(i))
            order = request.POST.get('order{}'.format(i))
            if not order:
                order = len(data_to_file)
            type = request.POST.get('type{}'.format(i))
            if type == "Integer":
                range_from = request.POST.get('range_from{}'.format(i))
                range_to = request.POST.get('range_till{}'.format(i))
                data_to_file.insert(int(order), name)
                data_to_file.insert(int(order) + 1, range_from)
                data_to_file.insert(int(order) + 2, range_to)
            else:
                data_to_file.insert(int(order), name)
        # removing extra created items
        data_to = ([s for s in data_to_file if s != 'remove'])
        data_to = ([s for s in data_to if s is not None])
        check_name = Schema.objects.filter(schema_name=schema_name, user_create_id=user_id)
        # check schema name if exist add +1
        if check_name:
            was_duplicate = "{}(1)".format(schema_name)
            check_was_duplicate = Schema.objects.filter(schema_name=was_duplicate, user_create_id=user_id)
            if check_was_duplicate:
                for i in range(100):
                    checking_index = "{}({})".format(schema_name, i + 2)
                    exist = Schema.objects.filter(schema_name=checking_index, user_create_id=user_id)
                    if not exist:
                        schema_name = checking_index
                        break
            else:
                schema_name = was_duplicate
        today = date.today()
        user_schemas = Schema.objects.all()
        return render(request, "test_app/data_sets.html", {"user_schemas": user_schemas, "data_to": data_to,
                                                           "schema_name": schema_name,
                                                           "column_separator": column_separator,
                                                           "string_character": string_character, "today": today})
    return render(request, "test_app/crete_schema.html", {"user": request.user.username})


@login_required
def data_sets(request):
    user_id = request.user.id
    user_schemas = Schema.objects.all()
    return render(request, "test_app/data_sets.html", {"user_schemas": user_schemas})


@api_view(['POST', 'GET'])
@login_required
def generate_data(request):
    data = request.GET
    # processing data from get request
    d = data['data_to']
    data_to = to_list(d)
    schema_name = data['name']
    string_character = data['string_character']
    column_separator = data['column_separator']
    # registering dialect for csv
    if column_separator == "Semicolon(;)":
        delimiter = ';'
    elif column_separator == "Slash(/)":
        delimiter = '/'
    else:
        delimiter = ','
    if string_character == 'Double-quote(")':
        quotechar = '"'
    else:
        quotechar = "'"
    # call Celery to write csv
    # celery -A tes_project worker -l info -P gevent( use for windows)
    file_path = 'media/uploads/{}.csv'.format(schema_name)
    # to run celery as python function
    # creation_task.run(data_to=data_to, file_path=file_path, delimiter=delimiter, quotechar=quotechar)
    #
    # code to use for celery deploy when redis run
    #
    create = creation_task.delay(data_to=data_to, file_path=file_path, delimiter=delimiter, quotechar=quotechar)
    x = create.status
    while x != 'SUCCESS':
        result = create.status
        x = result
        if result == 'FAILURE':
            return Response(status=status.HTTP_418_IM_A_TEAPOT)
    new_user_schema = Schema(user_create_id=request.user.id, schema=data_to, schema_name=schema_name, generated=True,
                            modified=date.today(), file_path=file_path)
    new_user_schema.save()
    return Response(status=status.HTTP_200_OK)


@login_required
def download_schema(request, schema_name):
    user_id = request.user.id
    # taking data from db to download
    schema_to_download = Schema.objects.get(user_create_id=user_id, schema_name=schema_name)
    # creating name for file from name and date
    today = date.today()
    file = 'filename="{}{}.csv"'.format(schema_name, today)
    # processing data for csv
    s = schema_to_download.schema
    schema = to_list(s)
    # writing csv
    response = HttpResponse(content_type='text/csv')
    response['Content-Disposition'] = filename = '{}'.format(file)
    writer = csv.writer(response)
    writer.writerow(schema)

    return response


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
