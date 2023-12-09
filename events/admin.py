from django.contrib import admin

from .models import Event, Review


class EventAdmin(admin.ModelAdmin):
    list_display = ('title', 'start_date', 'end_date', 'is_expired', 'total_reviews', 'rating', 'user')
    list_filter = ('is_expired', 'user')
    search_fields = ('title', 'description')
    ordering = ('-created_at',)
    readonly_fields = ('is_expired', 'total_reviews', 'rating')

admin.site.register(Event, EventAdmin)
admin.site.register(Review)
