from django.contrib import admin
from .models import *
# from auditlog.models import LogEntry

# Register your models here.
# admin.site.register(LogEntry)
admin.site.register(Author)
admin.site.register(Publisher)
admin.site.register(Book)
admin.site.register(BookCopy)
admin.site.register(Category)