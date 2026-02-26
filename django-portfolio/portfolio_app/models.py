from django.db import models
from django.utils.text import slugify
import os

class Certification(models.Model):
    # UPDATED TYPE_CHOICES to match your data
    TYPE_CHOICES = [
        ('foundational', 'Foundational Certification'),
        ('associate', 'Associate Certification'), 
        ('technical', 'Technical Certification'),
        ('professional', 'Professional Certification'),
        ('university', 'University Course'),
        ('online', 'Online Course'),
        ('course_completion', 'Course Completion'),
    ]

    # UPDATED LEVEL_CHOICES - keep as is, just ensure case matches
    LEVEL_CHOICES = [
        ('beginner', 'Beginner'),
        ('intermediate', 'Intermediate'),
        ('advanced', 'Advanced'),
        ('expert', 'Expert'),
    ]

    # Rest of the model remains the same
    title = models.CharField(max_length=200)
    issuing_organization = models.CharField(max_length=200)
    issue_date = models.DateField()
    expiration_date = models.DateField(blank=True, null=True)
    credential_id = models.CharField(max_length=100, blank=True, null=True)
    credential_url = models.URLField(blank=True, null=True)
    certificate_image = models.ImageField(upload_to='certificates/', blank=True, null=True)
    
    # Categorization
    certification_type = models.CharField(max_length=20, choices=TYPE_CHOICES, default='technical')
    skill_level = models.CharField(max_length=20, choices=LEVEL_CHOICES, default='intermediate')
    
    # Description
    description = models.TextField(blank=True, null=True)
    skills_covered = models.TextField(help_text="Comma-separated list of skills covered", blank=True, null=True)
    
    # Display settings
    display_order = models.IntegerField(default=0)
    featured = models.BooleanField(default=False)
    is_active = models.BooleanField(default=True)
    
    # Timestamps
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        ordering = ['display_order', '-issue_date']
        verbose_name_plural = "Certifications"

    def __str__(self):
        return f"{self.title} - {self.issuing_organization}"

    def is_expired(self):
        if self.expiration_date:
            from django.utils import timezone
            return self.expiration_date < timezone.now().date()
        return False

    def is_expiring_soon(self):
        if self.expiration_date:
            from django.utils import timezone
            from datetime import timedelta
            return self.expiration_date <= timezone.now().date() + timedelta(days=90)
        return False

    def get_skills_list(self):
        """Return skills covered as list"""
        if self.skills_covered:
            return [skill.strip() for skill in self.skills_covered.split(',') if skill.strip()]
        return []

class Achievement(models.Model):
    CATEGORY_CHOICES = [
        ('hackathon', 'Hackathon'),
        ('competition', 'Competition'),
        ('award', 'Award'),
        ('publication', 'Publication'),
        ('volunteer', 'Volunteer Work'),
        ('leadership', 'Leadership'),
        ('other', 'Other'),
    ]

    title = models.CharField(max_length=200)
    category = models.CharField(max_length=20, choices=CATEGORY_CHOICES, default='other')
    organization = models.CharField(max_length=200)
    date = models.DateField()
    location = models.CharField(max_length=100, blank=True, null=True)
    
    # Details
    description = models.TextField()
    result = models.CharField(max_length=100, blank=True, null=True, help_text="e.g., 1st Place, Finalist, etc.")
    project_link = models.URLField(blank=True, null=True)
    certificate_link = models.URLField(blank=True, null=True)
    image = models.ImageField(upload_to='achievements/', blank=True, null=True)
    
    # Skills demonstrated
    technologies_used = models.TextField(help_text="Comma-separated list of technologies used", blank=True, null=True)
    
    # Display settings
    display_order = models.IntegerField(default=0)
    featured = models.BooleanField(default=False)
    is_active = models.BooleanField(default=True)
    
    # Timestamps
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        ordering = ['display_order', '-date']
        verbose_name_plural = "Achievements"

    def __str__(self):
        return f"{self.title} - {self.organization}"

    def get_technologies_list(self):
        """Return technologies used as list"""
        if self.technologies_used:
            return [tech.strip() for tech in self.technologies_used.split(',') if tech.strip()]
        return []

    def get_icon(self):
        icons = {
            'hackathon': '💻',
            'competition': '🏆',
            'award': '🎖️',
            'publication': '📄',
            'volunteer': '🤝',
            'leadership': '👥',
            'other': '🌟',
        }
        return icons.get(self.category, '🌟')
    
# In models.py - Update the Project model
class Project(models.Model):
    PROJECT_TYPE_CHOICES = [
        ('web', 'Web Application'),
        ('ml', 'Machine Learning'),
        ('mobile', 'Mobile App'),
        ('automation', 'Automation'),
        ('data', 'Data Analysis'),
        ('other', 'Other'),
    ]
    
    STATUS_CHOICES = [
        ('completed', 'Completed'),
        ('in_progress', 'In Progress'),
        ('planned', 'Planned'),
    ]

    title = models.CharField(max_length=200)
    slug = models.SlugField(max_length=200, unique=True, blank=True)
    
    # For projects page (listing)
    short_description = models.CharField(max_length=300, blank=True)
    
    # For project detail page - CHANGE THIS LINE
    description = models.TextField()  # Removed blank=True to make it required
    
    project_type = models.CharField(max_length=20, choices=PROJECT_TYPE_CHOICES, default='web')
    status = models.CharField(max_length=20, choices=STATUS_CHOICES, default='completed')
    
    # Technical details
    tech_stack = models.TextField(help_text="Comma-separated list of technologies used")
    github_link = models.URLField(blank=True, null=True)
    live_demo = models.URLField(blank=True, null=True)
    documentation_link = models.URLField(blank=True, null=True)
    
    # Media
    featured_image = models.ImageField(upload_to='projects/featured/', blank=True, null=True)
    additional_images = models.TextField(blank=True, help_text="Comma-separated list of image paths")
    
    # Metadata
    start_date = models.DateField(blank=True, null=True)
    end_date = models.DateField(blank=True, null=True)
    display_order = models.IntegerField(default=0)
    featured = models.BooleanField(default=False)
    is_active = models.BooleanField(default=True)
    
    # Timestamps
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        ordering = ['display_order', '-created_at']

    def __str__(self):
        return self.title

    def save(self, *args, **kwargs):
        if not self.slug:
            self.slug = slugify(self.title)
        # Only auto-generate short_description if it's empty
        if not self.short_description and self.description:
            self.short_description = self.description[:297] + '...' if len(self.description) > 300 else self.description
        super().save(*args, **kwargs)

    def get_tech_list(self):
        """Return tech stack as list"""
        return [tech.strip() for tech in self.tech_stack.split(',') if tech.strip()]

    def get_additional_images_list(self):
        """Return additional images as list"""
        if self.additional_images:
            return [img.strip() for img in self.additional_images.split(',') if img.strip()]
        return []

    def is_ongoing(self):
        return self.status == 'in_progress'

    def get_project_duration(self):
        if self.start_date and self.end_date:
            return f"{self.start_date.strftime('%b %Y')} - {self.end_date.strftime('%b %Y')}"
        elif self.start_date:
            return f"Started {self.start_date.strftime('%b %Y')}"
        return "Duration not specified"
        
class Skill(models.Model):
    CATEGORY_CHOICES = [
        ('programming', 'Programming Languages'),
        ('framework', 'Frameworks & Libraries'),
        ('tool', 'Tools & Technologies'),
        ('ml', 'AI/ML Tools'),
        ('database', 'Databases'),
        ('cloud', 'Cloud & DevOps'),
    ]
    
    name = models.CharField(max_length=100)
    category = models.CharField(max_length=20, choices=CATEGORY_CHOICES)
    proficiency = models.IntegerField(help_text="Proficiency level from 1 to 100", default=50)
    description = models.TextField(blank=True, null=True)
    icon = models.CharField(max_length=50, blank=True, help_text="Icon class or emoji")
    display_order = models.IntegerField(default=0, help_text="Order in which skills are displayed")
    is_active = models.BooleanField(default=True)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        ordering = ['display_order', 'name']

    def __str__(self):
        return f"{self.name} ({self.get_category_display()})"

    def proficiency_percentage(self):
        return f"{self.proficiency}%"
    

class Education(models.Model):
        
    DEGREE_CHOICES = [
        ('high_school', 'High School'),
        ('diploma', 'Diploma'),
        ('bachelor', 'Bachelor\'s Degree'),
        ('master', 'Master\'s Degree'),
        ('phd', 'PhD'),
        ('certificate', 'Certificate'),
        ('online', 'Online Course'),
    ]

    degree = models.CharField(max_length=20, choices=DEGREE_CHOICES, default='bachelor')
    title = models.CharField(max_length=200)
    institution = models.CharField(max_length=200)
    location = models.CharField(max_length=100)
    start_date = models.DateField()
    end_date = models.DateField(blank=True, null=True)
    currently_studying = models.BooleanField(default=False)
    
    # Details
    description = models.TextField(blank=True, null=True)
    grade = models.CharField(max_length=50, blank=True, null=True, help_text="e.g., GPA, Percentage, Grade")
    courses = models.TextField(blank=True, null=True, help_text="Comma-separated list of key courses")
    achievements = models.TextField(blank=True, null=True, help_text="Comma-separated list of achievements")
    
    # Media
    logo = models.ImageField(upload_to='education/logos/', blank=True, null=True)
    certificate = models.FileField(upload_to='education/certificates/', blank=True, null=True)
    
    # Display settings
    display_order = models.IntegerField(default=0)
    featured = models.BooleanField(default=False)
    is_active = models.BooleanField(default=True)
    
    # Timestamps
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        ordering = ['display_order', '-start_date']
        verbose_name_plural = "Education"

    def __str__(self):
        return f"{self.title} - {self.institution}"

    def get_duration(self):
        if self.currently_studying:
            return f"{self.start_date.strftime('%b %Y')} - Present"
        elif self.end_date:
            return f"{self.start_date.strftime('%b %Y')} - {self.end_date.strftime('%b %Y')}"
        return self.start_date.strftime('%b %Y')

    def get_courses_list(self):
        """Return courses as list"""
        if self.courses:
            return [course.strip() for course in self.courses.split(',') if course.strip()]
        return []

    def get_achievements_list(self):
        """Return achievements as list"""
        if self.achievements:
            return [achievement.strip() for achievement in self.achievements.split(',') if achievement.strip()]
        return []

    def get_icon(self):
        icons = {
            'high_school': '🏫',
            'diploma': '📜',
            'bachelor': '🎓',
            'master': '📚',
            'phd': '👨‍🎓',
            'certificate': '📄',
            'online': '💻',
        }
        return icons.get(self.degree, '🎓')