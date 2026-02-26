from django.contrib import admin
from .models import Skill, Project, Certification, Achievement, Education

@admin.register(Education)
class EducationAdmin(admin.ModelAdmin):
    list_display = ['title', 'institution', 'degree', 'start_date', 'currently_studying', 'featured', 'is_active']
    list_filter = ['degree', 'currently_studying', 'featured', 'is_active']
    list_editable = ['featured', 'is_active']
    search_fields = ['title', 'institution', 'description']
    readonly_fields = ['created_at', 'updated_at']
    
    fieldsets = (
        ('Basic Information', {
            'fields': ('degree', 'title', 'institution', 'location')
        }),
        ('Timeline', {
            'fields': ('start_date', 'end_date', 'currently_studying')
        }),
        ('Academic Details', {
            'fields': ('description', 'grade', 'courses', 'achievements')
        }),
        ('Media', {
            'fields': ('logo', 'certificate')
        }),
        ('Display Settings', {
            'fields': ('featured', 'display_order', 'is_active')
        }),
        ('Metadata', {
            'fields': ('created_at', 'updated_at'),
            'classes': ('collapse',)
        }),
    )

@admin.register(Certification)
class CertificationAdmin(admin.ModelAdmin):
    list_display = ['title', 'issuing_organization', 'certification_type', 'issue_date', 'featured', 'is_active']
    list_filter = ['certification_type', 'skill_level', 'featured', 'is_active']
    list_editable = ['featured', 'is_active']
    search_fields = ['title', 'issuing_organization', 'description']
    readonly_fields = ['created_at', 'updated_at']
    
    fieldsets = (
        ('Basic Information', {
            'fields': ('title', 'issuing_organization', 'description')
        }),
        ('Certification Details', {
            'fields': ('certification_type', 'skill_level', 'issue_date', 'expiration_date')
        }),
        ('Credentials', {
            'fields': ('credential_id', 'credential_url', 'certificate_image')
        }),
        ('Skills Covered', {
            'fields': ('skills_covered',)
        }),
        ('Display Settings', {
            'fields': ('featured', 'display_order', 'is_active')
        }),
        ('Metadata', {
            'fields': ('created_at', 'updated_at'),
            'classes': ('collapse',)
        }),
    )

@admin.register(Achievement)
class AchievementAdmin(admin.ModelAdmin):
    list_display = ['title', 'category', 'organization', 'date', 'result', 'featured', 'is_active']
    list_filter = ['category', 'featured', 'is_active']
    list_editable = ['featured', 'is_active']
    search_fields = ['title', 'organization', 'description']
    readonly_fields = ['created_at', 'updated_at']
    
    fieldsets = (
        ('Basic Information', {
            'fields': ('title', 'category', 'organization', 'date', 'location')
        }),
        ('Achievement Details', {
            'fields': ('description', 'result')
        }),
        ('Links & Media', {
            'fields': ('project_link', 'certificate_link', 'image')
        }),
        ('Technologies Used', {
            'fields': ('technologies_used',)
        }),
        ('Display Settings', {
            'fields': ('featured', 'display_order', 'is_active')
        }),
        ('Metadata', {
            'fields': ('created_at', 'updated_at'),
            'classes': ('collapse',)
        }),
    )

@admin.register(Project)
class ProjectAdmin(admin.ModelAdmin):
    list_display = ['title', 'project_type', 'status', 'featured', 'display_order', 'is_active', 'created_at']
    list_filter = ['project_type', 'status', 'featured', 'is_active']
    list_editable = ['featured', 'display_order', 'is_active']
    search_fields = ['title', 'description', 'tech_stack']
    prepopulated_fields = {'slug': ('title',)}
    readonly_fields = ['created_at', 'updated_at']
    
    fieldsets = (
        ('Basic Information', {
            'fields': ('title', 'slug', 'description', 'short_description')
        }),
        ('Project Details', {
            'fields': ('project_type', 'status', 'tech_stack', 'start_date', 'end_date')
        }),
        ('Links', {
            'fields': ('github_link', 'live_demo', 'documentation_link')
        }),
        ('Media', {
            'fields': ('featured_image', 'additional_images')
        }),
        ('Display Settings', {
            'fields': ('featured', 'display_order', 'is_active')
        }),
        ('Metadata', {
            'fields': ('created_at', 'updated_at'),
            'classes': ('collapse',)
        }),
    )
    
@admin.register(Skill)
class SkillAdmin(admin.ModelAdmin):
    list_display = ['name', 'category', 'proficiency', 'display_order', 'is_active']
    list_filter = ['category', 'is_active']
    list_editable = ['display_order', 'is_active']
    search_fields = ['name', 'description']
    ordering = ['display_order', 'name']
    
    fieldsets = (
        ('Basic Information', {
            'fields': ('name', 'category', 'description', 'icon')
        }),
        ('Display Settings', {
            'fields': ('proficiency', 'display_order', 'is_active')
        }),
    )