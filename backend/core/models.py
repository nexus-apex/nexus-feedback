from django.db import models

class FeedbackItem(models.Model):
    title = models.CharField(max_length=255)
    customer_name = models.CharField(max_length=255, blank=True, default="")
    customer_email = models.EmailField(blank=True, default="")
    category = models.CharField(max_length=50, choices=[("bug", "Bug"), ("feature", "Feature"), ("complaint", "Complaint"), ("praise", "Praise"), ("suggestion", "Suggestion")], default="bug")
    rating = models.IntegerField(default=0)
    status = models.CharField(max_length=50, choices=[("new", "New"), ("acknowledged", "Acknowledged"), ("in_progress", "In Progress"), ("resolved", "Resolved")], default="new")
    priority = models.CharField(max_length=50, choices=[("low", "Low"), ("medium", "Medium"), ("high", "High")], default="low")
    description = models.TextField(blank=True, default="")
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        ordering = ['-created_at']

    def __str__(self):
        return self.title

class FeedbackCategory(models.Model):
    name = models.CharField(max_length=255)
    items_count = models.IntegerField(default=0)
    avg_rating = models.DecimalField(max_digits=12, decimal_places=2, default=0)
    response_time_hrs = models.DecimalField(max_digits=12, decimal_places=2, default=0)
    owner = models.CharField(max_length=255, blank=True, default="")
    active = models.BooleanField(default=False)
    description = models.TextField(blank=True, default="")
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        ordering = ['-created_at']

    def __str__(self):
        return self.name

class FBResponse(models.Model):
    feedback_title = models.CharField(max_length=255)
    responder = models.CharField(max_length=255, blank=True, default="")
    response = models.TextField(blank=True, default="")
    date = models.DateField(null=True, blank=True)
    internal_note = models.TextField(blank=True, default="")
    status = models.CharField(max_length=50, choices=[("draft", "Draft"), ("sent", "Sent")], default="draft")
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        ordering = ['-created_at']

    def __str__(self):
        return self.feedback_title
