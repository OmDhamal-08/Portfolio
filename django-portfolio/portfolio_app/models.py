from django.core.validators import FileExtensionValidator
from django.db import models


class ContactMessage(models.Model):
    REPLY_STATUS_CHOICES = [
        ('new', 'New'),
        ('in_progress', 'In Progress'),
        ('replied', 'Replied'),
        ('archived', 'Archived'),
    ]

    EMAIL_STATUS_CHOICES = [
        ('pending', 'Pending'),
        ('sent', 'Sent'),
        ('failed', 'Failed'),
    ]

    name = models.CharField(max_length=100)
    email = models.EmailField()
    subject = models.CharField(max_length=200)
    message = models.TextField()
    ip_address = models.GenericIPAddressField(blank=True, null=True)
    user_agent = models.CharField(max_length=255, blank=True)
    is_read = models.BooleanField(default=False)
    reply_status = models.CharField(max_length=20, choices=REPLY_STATUS_CHOICES, default='new')
    email_status = models.CharField(max_length=20, choices=EMAIL_STATUS_CHOICES, default='pending')
    email_error = models.TextField(blank=True)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        ordering = ['-created_at']

    def __str__(self):
        return f'{self.name} - {self.subject}'


class Resume(models.Model):
    title = models.CharField(max_length=150)
    file = models.FileField(
        upload_to='resumes/',
        validators=[FileExtensionValidator(['pdf'])],
    )
    version = models.CharField(max_length=50, blank=True)
    is_active = models.BooleanField(default=False)
    notes = models.TextField(blank=True)
    uploaded_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        ordering = ['-is_active', '-uploaded_at']

    def __str__(self):
        if self.version:
            return f'{self.title} ({self.version})'
        return self.title

    def save(self, *args, **kwargs):
        super().save(*args, **kwargs)
        if self.is_active:
            Resume.objects.exclude(pk=self.pk).update(is_active=False)
