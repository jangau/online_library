from django.contrib.auth.models import *
from django.contrib.admin import AdminSite
from models import Library, Book, Review

class SuperUserSite(AdminSite):
    site_header = 'SuperUserSite'

# Default admin site for adding superusers.
super = SuperUserSite(name='admin')
super.register(Library)
super.register(Book)
super.register(Review)
