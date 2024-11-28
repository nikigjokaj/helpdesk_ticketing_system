from django.shortcuts import render, redirect
from django.http import HttpResponse
from django.conf import settings
from django.db.models import Q
from django.core.files.storage import FileSystemStorage
from .models import ticket
from django.contrib import messages
from django.db import connection
from helpdesk_ticketing_system.utils import getDropDown, dictfetchall
from datetime import date
today = date.today()


# Create your views here.
def ticketlisting(request):
    cursor = connection.cursor()
    userID = request.session.get('user_id', None)
    if(request.session.get('user_level_id', None) == 2):
        SQL =  "SELECT * FROM ticket, ticket_type, ticket_status, users_user WHERE ticket_user_id = user_id AND status_id = ticket_status_id AND type_id = ticket_type_id AND user_id = "+str(userID)
    else:
        SQL =  "SELECT * FROM ticket, ticket_type, ticket_status, users_user WHERE ticket_user_id = user_id AND status_id = ticket_status_id AND type_id = ticket_type_id"
    cursor.execute(SQL)
    ticketlist = dictfetchall(cursor)

    context = {
        "ticketlist": ticketlist
    }

    # Message according Ticket #
    context['heading'] = "Ticket Details";
    return render(request, 'ticket-listing.html', context)

# Create your views here.
def get_ticket_details(id):
    cursor = connection.cursor()
    cursor.execute(
        "SELECT * FROM ticket, ticket_type, ticket_status WHERE status_id = ticket_status_id AND type_id = ticket_type_id AND ticket_id = "+id)
    ticketlist = dictfetchall(cursor)
    return ticketlist[0]

# Create your views here.
def ticket(request):
    cursor = connection.cursor()
    cursor.execute("SELECT * FROM ticket, ticket_type, ticket_status WHERE status_id = ticket_status_id AND type_id = ticket_type_id")
    ticketlist = dictfetchall(cursor)

    context = {
        "ticketlist": ticketlist
    }

    # Message according Ticket #
    context['heading'] = "Ticket Details";
    return render(request, 'ticket.html', context)

# Create your views here.
def ticket_filter(request, typeID):
    cursor = connection.cursor()
    cursor.execute(
        "SELECT * FROM ticket, ticket_status, ticket_type WHERE status_id = ticket_status_id AND type_id = ticket_type_id AND type_id = "+ str(typeID))
    ticketlist = dictfetchall(cursor)

    context = {
        "ticketlist": ticketlist
    }

    # Message according Ticket #
    context['heading'] = "Ticket Details";
    return render(request, 'ticket.html', context)

def getComments(id):
    cursor = connection.cursor()
    cursor.execute("SELECT * FROM comment, users_user, ticket WHERE ticket_id = comment_ticket_id AND comment_user_id = user_id AND comment_ticket_id = " + id)
    dataList = dictfetchall(cursor)
    return dataList

def update(request, ticketId):
    ticketdetails = get_ticket_details(ticketId)
    context = {
        "fn": "add",
        "ticket_status":getDropDown('ticket_status', 'status_id', 'status_title', ticketdetails['ticket_status_id'], '1'),
        "ticket_type":getDropDown('ticket_type', 'type_id', 'type_title', ticketdetails['ticket_type_id'], '1'),
        "ticketdetails":ticketdetails
    }
    if (request.method == "POST"):
        try:
            cursor = connection.cursor()
            cursor.execute("""
                UPDATE ticket  
                SET ticket_type_id=%s,ticket_status_id=%s, ticket_description=%s,ticket_title=%s
                WHERE ticket_id = %s
                """, (
                    request.POST['ticket_type_id'],
                    request.POST['ticket_status_id'],
                    request.POST['ticket_description'],
                    request.POST['ticket_title'],
                    request.POST['ticket_id']
            ))
        except Exception as e:
            return HttpResponse('Something went wrong. Error Message : '+ str(e))

        context["ticketdetails"] = get_ticket_details(ticketId)
        messages.add_message(request, messages.INFO, "Ticket updated succesfully !!!")
        return redirect('ticketlisting')

    else:
        return render(request,'ticket-add.html', context)

def post_comment(request):
    if (request.method == "POST"):
        userID = request.session.get('user_id', None)
        date = today.strftime("%Y-%m-%d %H:%M")
        cursor = connection.cursor()
        cursor.execute("""
        INSERT INTO comment
        SET comment_user_id=%s, comment_title=%s, comment_ticket_id=%s,  comment_description=%s, comment_date = %s
        """, (
        userID,
        request.POST['comment_title'],
        request.POST['comment_ticket_id'],
        request.POST['comment_description'],
        date            
        ))
      
    return redirect('/ticket/ticket-details/'+request.POST['comment_ticket_id']+'/')

def ticket_details(request, ticketId):
    if(request.session.get('authenticated', False) == False):
        messages.add_message(request, messages.ERROR, "Login to your account. To access this page !!!")
        return redirect('/users')
    cursor = connection.cursor()
    cursor.execute("SELECT * FROM ticket, ticket_type, ticket_status, users_user WHERE user_id = ticket_user_id AND status_id = ticket_status_id AND type_id = ticket_type_id AND ticket_id = "+ticketId)
    ticketdetails = dictfetchall(cursor)

    context = {
        "fn": "add",
        "ticketdetails":ticketdetails[0],
        "allComments": getComments(ticketId)
    }
    if (request.method == "POST"):
        customer_id = request.session.get('user_id', None);
        date = today.strftime("%B %d, %Y")
        cursor = connection.cursor()
        cursor.execute("""
		   INSERT INTO enquiry
		   SET enquiry_customer_id=%s, enquiry_ticket_id=%s, enquiry_date=%s
		""", (
            customer_id,
            ticketId,
            date
            ))
        messages.add_message(request, messages.INFO, "We got your enquriy for this ticket. We will contact you soon !!!")
    return render(request,'ticket-details.html', context)

def add(request):
    context = {
        "fn": "add",
        "ticket_status":getDropDown('ticket_status', 'status_id', 'status_title',0, '1'),
        "ticket_type":getDropDown('ticket_type', 'type_id', 'type_title',0, '1'),
        "heading": 'Raise Helpdesk Ticket'
    }
    customer_id = request.session.get('user_id', None);
    if (request.method == "POST"):
        try:
            cursor = connection.cursor()
            cursor.execute("""
                INSERT INTO ticket  
                SET ticket_user_id=%s, ticket_type_id=%s,ticket_status_id=%s, ticket_description=%s,ticket_title=%s
                """, (
                    customer_id,
                    request.POST['ticket_type_id'],
                    request.POST['ticket_status_id'],
                    request.POST['ticket_description'],
                    request.POST['ticket_title']
            ))
                
        except Exception as e:
            
            return HttpResponse('Something went wrong. Error Message : '+ str(e))

        return redirect('ticketlisting')

    else:
        return render(request,'ticket-add.html', context)

def delete(request, prodId):
    cursor = connection.cursor()
    sql = 'DELETE FROM ticket WHERE ticket_id ='+ str(prodId)

    cursor.execute(sql)
    
    messages.add_message(request, messages.INFO, "Ticket Deleted Successfully !!!")
    return redirect('ticketlisting')
