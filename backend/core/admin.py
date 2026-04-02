from django.contrib import admin
from .models import FeedbackItem, FeedbackCategory, FBResponse

@admin.register(FeedbackItem)
class FeedbackItemAdmin(admin.ModelAdmin):
    list_display = ["title", "customer_name", "customer_email", "category", "rating", "created_at"]
    list_filter = ["category", "status", "priority"]
    search_fields = ["title", "customer_name", "customer_email"]

@admin.register(FeedbackCategory)
class FeedbackCategoryAdmin(admin.ModelAdmin):
    list_display = ["name", "items_count", "avg_rating", "response_time_hrs", "owner", "created_at"]
    search_fields = ["name", "owner"]

@admin.register(FBResponse)
class FBResponseAdmin(admin.ModelAdmin):
    list_display = ["feedback_title", "responder", "date", "status", "created_at"]
    list_filter = ["status"]
    search_fields = ["feedback_title", "responder"]
