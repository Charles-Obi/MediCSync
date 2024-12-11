from django.contrib import admin
from myapp.models import Member, Appointment1, Contact, ImageModel, Users

# Register your models here.
admin.site.register(Member)
admin.site.register(Appointment1)
admin.site.register(Contact)
admin.site.register(ImageModel)
admin.site.register(Users)
