from django.contrib import admin

from allapps.models import Location, Hospital, Doctor, sessions, resetids

# Register your models here.
admin.site.register(Location)
admin.site.register(Hospital)
admin.site.register(Doctor)
admin.site.register(sessions)
admin.site.register(resetids)