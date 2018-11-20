from django.contrib import admin
from calculate.models import Email, Applicant
# Register your models here.

class EmailAdmin(admin.ModelAdmin):
	list_display = ('name','email','message')

admin.site.register(Applicant)
admin.site.register(Email,EmailAdmin)
