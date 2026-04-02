from django.core.management.base import BaseCommand
from django.contrib.auth.models import User
from core.models import FeedbackItem, FeedbackCategory, FBResponse
from datetime import date, timedelta
import random


class Command(BaseCommand):
    help = 'Seed NexusFeedback with demo data'

    def handle(self, *args, **kwargs):
        if not User.objects.filter(username='admin').exists():
            User.objects.create_superuser('admin', 'admin@nexusfeedback.com', 'Admin@2024')
            self.stdout.write(self.style.SUCCESS('Admin user created'))

        if FeedbackItem.objects.count() == 0:
            for i in range(10):
                FeedbackItem.objects.create(
                    title=f"Sample FeedbackItem {i+1}",
                    customer_name=f"Sample FeedbackItem {i+1}",
                    customer_email=f"demo{i+1}@example.com",
                    category=random.choice(["bug", "feature", "complaint", "praise", "suggestion"]),
                    rating=random.randint(1, 100),
                    status=random.choice(["new", "acknowledged", "in_progress", "resolved"]),
                    priority=random.choice(["low", "medium", "high"]),
                    description=f"Sample description for record {i+1}",
                )
            self.stdout.write(self.style.SUCCESS('10 FeedbackItem records created'))

        if FeedbackCategory.objects.count() == 0:
            for i in range(10):
                FeedbackCategory.objects.create(
                    name=f"Sample FeedbackCategory {i+1}",
                    items_count=random.randint(1, 100),
                    avg_rating=round(random.uniform(1000, 50000), 2),
                    response_time_hrs=round(random.uniform(1000, 50000), 2),
                    owner=f"Sample {i+1}",
                    active=random.choice([True, False]),
                    description=f"Sample description for record {i+1}",
                )
            self.stdout.write(self.style.SUCCESS('10 FeedbackCategory records created'))

        if FBResponse.objects.count() == 0:
            for i in range(10):
                FBResponse.objects.create(
                    feedback_title=f"Sample FBResponse {i+1}",
                    responder=f"Sample {i+1}",
                    response=f"Sample response for record {i+1}",
                    date=date.today() - timedelta(days=random.randint(0, 90)),
                    internal_note=f"Sample internal note for record {i+1}",
                    status=random.choice(["draft", "sent"]),
                )
            self.stdout.write(self.style.SUCCESS('10 FBResponse records created'))
