from django.contrib import admin

# Register your models here.

from .models import *

admin.site.register(ai)
admin.site.register(author)
admin.site.register(crop)
admin.site.register(Protocol)
admin.site.register(year)
admin.site.register(country)
admin.site.register(Presentation)


