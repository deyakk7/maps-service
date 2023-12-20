from django.contrib import admin

from .models import Review, Event


@admin.register(Event)
class EventAdmin(admin.ModelAdmin):
    list_display = ('title', 'start_date', 'end_date', 'is_expired', 'total_reviews', 'rating', 'user')
    list_filter = ('is_expired', 'user')
    search_fields = ('title', 'description')
    ordering = ('-created_at',)
    readonly_fields = ('is_expired', 'total_reviews', 'rating')
    list_per_page = 5


admin.site.register(Review)
