from django.contrib import admin
from django.utils.html import format_html
from urllib.parse import quote
from .models import Problem


@admin.register(Problem)
class ProblemAdmin(admin.ModelAdmin):
    list_display = ('title', 'category', 'location', 'verification_status', 'map_link', 'status', 'created_at')
    list_filter = ('verification_status', 'status', 'category')
    search_fields = ('title', 'description', 'location')
    readonly_fields = ('created_at', 'map_link')
    actions = ('mark_verified', 'mark_cancelled', 'mark_resolved')
    date_hierarchy = 'created_at'
    ordering = ('-created_at',)
    list_per_page = 20

    @admin.action(description='Mark selected reports as verified')
    def mark_verified(self, request, queryset):
        queryset.update(verification_status='Verified')

    @admin.action(description='Cancel selected fake reports')
    def mark_cancelled(self, request, queryset):
        queryset.update(verification_status='Cancelled')

    @admin.action(description='Mark selected reports as resolved')
    def mark_resolved(self, request, queryset):
        queryset.update(status='Resolved')

    @admin.display(description='Google Maps')
    def map_link(self, problem):
        if problem.latitude is not None and problem.longitude is not None:
            url = f'https://www.google.com/maps?q={problem.latitude},{problem.longitude}'
            label = 'Open exact GPS location'
        elif problem.location:
            url = f'https://www.google.com/maps/search/?api=1&query={quote(problem.location)}'
            label = 'Search submitted address'
        else:
            return 'No location submitted'
        return format_html('<a href="{}" target="_blank" rel="noopener">{}</a>', url, label)
