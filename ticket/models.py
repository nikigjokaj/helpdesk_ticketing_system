# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models

# Create your models here.

class ticket(models.Model):
    ticket_id = models.AutoField(primary_key=True)
    ticket_user_id = models.CharField(max_length=255, default = '')
    ticket_type_id = models.CharField(max_length=255, default = "")
    ticket_status_id = models.CharField(max_length=255, default = "")
    ticket_cost = models.CharField(max_length=255, default = "")
    ticket_image = models.CharField(max_length=255, null = True)
    ticket_description = models.TextField(default = "")
    ticket_title = models.CharField(max_length=255, default = "")
    ticket_contact = models.CharField(max_length=255, default = "")
    ticket_email = models.CharField(max_length=255, default = '')
    ticket_amenities = models.CharField(max_length=255, default = "")
    ticket_specifications = models.CharField(max_length=255, default = "")
    ticket_rooms = models.CharField(max_length=255, default = "")
    ticket_no_balcony = models.CharField(max_length=255, null = True)
    ticket_no_bathrooms = models.TextField(default = "")
    ticket_address = models.CharField(max_length=255, default = "")
    def __str__(self):
        return self.ticket_user_id
