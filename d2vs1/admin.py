from django.contrib import admin
from .models import *
# Register your models here.

class LogsAdmin(admin.ModelAdmin):
    list_display = ('id', 'logs_user', 'status', 'timestamp')

admin.site.register(User)
admin.site.register(Logs,LogsAdmin)