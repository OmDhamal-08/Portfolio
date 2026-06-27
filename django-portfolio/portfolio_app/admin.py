from django.contrib import admin

from .models import ContactMessage, Resume


@admin.register(ContactMessage)
class ContactMessageAdmin(admin.ModelAdmin):
    list_display = ['subject', 'name', 'email', 'reply_status', 'email_status', 'is_read', 'created_at']
    list_filter = ['reply_status', 'email_status', 'is_read', 'created_at']
    list_editable = ['reply_status', 'is_read']
    search_fields = ['name', 'email', 'subject', 'message']
    readonly_fields = [
        'name',
        'email',
        'subject',
        'message',
        'ip_address',
        'user_agent',
        'email_status',
        'email_error',
        'created_at',
        'updated_at',
    ]
    actions = ['mark_as_read', 'mark_as_replied', 'archive_messages']

    fieldsets = (
        ('Message', {
            'fields': ('name', 'email', 'subject', 'message'),
        }),
        ('Tracking', {
            'fields': ('is_read', 'reply_status', 'email_status', 'email_error'),
        }),
        ('Request Metadata', {
            'fields': ('ip_address', 'user_agent'),
            'classes': ('collapse',),
        }),
        ('Timestamps', {
            'fields': ('created_at', 'updated_at'),
            'classes': ('collapse',),
        }),
    )

    @admin.action(description='Mark selected messages as read')
    def mark_as_read(self, request, queryset):
        queryset.update(is_read=True)

    @admin.action(description='Mark selected messages as replied')
    def mark_as_replied(self, request, queryset):
        queryset.update(is_read=True, reply_status='replied')

    @admin.action(description='Archive selected messages')
    def archive_messages(self, request, queryset):
        queryset.update(is_read=True, reply_status='archived')


@admin.register(Resume)
class ResumeAdmin(admin.ModelAdmin):
    list_display = ['title', 'version', 'is_active', 'uploaded_at', 'updated_at']
    list_filter = ['is_active', 'uploaded_at']
    search_fields = ['title', 'version', 'notes']
    readonly_fields = ['uploaded_at', 'updated_at']

    fieldsets = (
        ('Resume File', {
            'fields': ('title', 'version', 'file', 'is_active'),
        }),
        ('Notes', {
            'fields': ('notes',),
        }),
        ('Timestamps', {
            'fields': ('uploaded_at', 'updated_at'),
            'classes': ('collapse',),
        }),
    )
