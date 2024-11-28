from django.conf.urls import url
from . import views

urlpatterns = [
    url(r'^$', views.ticket, name="ticket"),
    url(r'^filters/(?P<typeID>\w{0,50})/$', views.ticket_filter, name="ticket_filter"),
    url(r'^ticket-listing$', views.ticketlisting, name="ticketlisting"),
    url(r'^add$', views.add, name="add"),
    url(r'^ticket-details/(?P<ticketId>\w{0,50})/$', views.ticket_details, name="ticket_details"),
    url(r'^post_comment/$', views.post_comment, name="post_comment"),
    url(r'^update/(?P<ticketId>\w{0,50})/$', views.update, name="update"),
    url(r'^delete/(?P<prodId>\w{0,50})/$', views.delete, name="delete"),
]
