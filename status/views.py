from django.shortcuts import render, redirect
from django.http import HttpResponse
from django.conf import settings
from django.db.models import Q
from django.core.files.storage import FileSystemStorage
from django.contrib import messages
from django.db import connection


# Create your views here.

def listing(request):
    cursor = connection.cursor()
    cursor.execute("SELECT * FROM ticket_status")
    statuslist = dictfetchall(cursor)

    context = {
        "statuslist": statuslist
    }

    # Message according medicines Role #
    context['heading'] = "Status Details";
    return render(request, 'status-details.html', context)

def lists(request):
    cursor = connection.cursor()
    cursor.execute("SELECT * FROM ticket_status")
    statuslist = dictfetchall(cursor)

    context = {
        "statuslist": statuslist
    }

    # Message according medicines Role #
    context['heading'] = "Status Details";
    return render(request, 'status-list.html', context)

def dictfetchall(cursor):
    "Return all rows from a cursor as a dict"
    columns = [col[0] for col in cursor.description]
    return [
        dict(zip(columns, row))
        for row in cursor.fetchall()
    ]

def getData(id):
    cursor = connection.cursor()
    cursor.execute("SELECT * FROM ticket_status WHERE status_id = " + id)
    dataList = dictfetchall(cursor)
    return dataList[0];

def update(request, statusId):
    context = {
        "fn": "update",
        "statusDetails": getData(statusId),
        "heading": 'Update Status',
    }
    if (request.method == "POST"):
        cursor = connection.cursor()
        cursor.execute("""
                   UPDATE ticket_status
                   SET status_title=%s, status_description=%s WHERE status_id = %s
                """, (
            request.POST['status_title'],
            request.POST['status_description'],
            statusId
        ))
        context["statusDetails"] =  getData(statusId)
        messages.add_message(request, messages.INFO, "Status updated succesfully !!!")
        return redirect('status-listing')
    else:
        return render(request, 'status.html', context)


def add(request):
    context = {
        "fn": "add",
        "heading": 'Add Status'
    };
    if (request.method == "POST"):
        cursor = connection.cursor()
        cursor.execute("""
		   INSERT INTO ticket_status
		   SET status_title=%s, status_description=%s
		""", (
            request.POST['status_title'],
            request.POST['status_description']))
        return redirect('status-listing')
    return render(request, 'status.html', context)

def delete(request, id):
    cursor = connection.cursor()
    sql = 'DELETE FROM ticket_status WHERE status_id=' + id
    cursor.execute(sql)
    messages.add_message(request, messages.INFO, "Status Deleted succesfully !!!")
    return redirect('status-listing')
