from django.contrib import admin
from models import Rehearsal, Gig, Kamerer

class RehearsalAdmin(admin.ModelAdmin):
	fieldsets = (
        (None, {'fields': ('location', 'date', 
			"time_hole", "time_location", "signup", "fika",
			"info")} ),
        ('Hidden',{ 'fields': ("insiderinfo",),
                    'classes': ('collapse',) })
	)
admin.site.register(Rehearsal, RehearsalAdmin)
	
class GigAdmin(admin.ModelAdmin):
	fieldsets = (
        (None, {'fields': ('name', 'location', 'date', 
			"time_hole", "time_location", "time_playing", "signup",
			"info")} ),
        ('Hidden',{ 'fields': ("insiderinfo",),
                    'classes': ('collapse',) })
    )
admin.site.register(Gig, GigAdmin)

from django.contrib.auth.admin import UserAdmin
from django.contrib.auth.models import User

# Define an inline admin descriptor for UserProfile model
class KamererInline(admin.StackedInline):
	model = Kamerer
	fk_name = 'user'
	max_num = 1

class KamererAdmin(UserAdmin):
	inlines = [KamererInline]

admin.site.unregister(User)
admin.site.register(User, KamererAdmin)
