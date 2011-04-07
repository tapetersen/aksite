from django.contrib import admin
from feincms.admin import editor, item_editor
from core.models import Repetition, Gig

class RepetitionAdmin(admin.ModelAdmin):
	fieldsets = (
        (None, {'fields': ('location', 'date', 
			"time_hole", "time_location", "signup", "fika",
			"info")} ),
        ('Hidden',{ 'fields': ("insiderinfo",),
                    'classes': ('collapse',) })
	)
admin.site.register(Repetition, RepetitionAdmin)
	
class GigAdmin(admin.ModelAdmin):
	fieldsets = (
        (None, {'fields': ('name', 'location', 'date', 
			"time_hole", "time_location", "time_playing", "signup",
			"info")} ),
        ('Hidden',{ 'fields': ("insiderinfo",),
                    'classes': ('collapse',) })
    )
admin.site.register(Gig, GigAdmin)