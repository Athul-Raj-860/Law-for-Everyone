from django.contrib import admin
from .models import Emergency_Numbers, Basic_Laws, Lawyer_Register

# Register your models here.
admin.site.register(Emergency_Numbers)
admin.site.register(Basic_Laws)
admin.site.register(Lawyer_Register)
