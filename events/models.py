from datetime import datetime

from django.contrib.auth import get_user_model
from django.core.validators import MaxValueValidator, MinValueValidator
from django.db import models
from django.utils import timezone

User = get_user_model()


class Event(models.Model):
    title = models.CharField(max_length=255)
    description = models.TextField(null=True, blank=True)
    start_date = models.DateTimeField(null=True, blank=True)
    end_date = models.DateTimeField(null=True, blank=True)
    image = models.ImageField(upload_to='events', blank=True, null=True, default='events/default-event.jpg')
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    position_x = models.FloatField(null=True, blank=True)
    position_y = models.FloatField(null=True, blank=True)
    is_expired = models.BooleanField(default=False)
    total_reviews = models.PositiveIntegerField(default=0, null=True, blank=True)
    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name='events')
    rating = models.FloatField(default=0, null=True, blank=True)

    class Meta:
        verbose_name = 'Event'
        verbose_name_plural = 'Events'
        ordering = ['-created_at']

    def __str__(self):
        return self.title

    def save(self, *args, **kwargs):
        self.is_expired = self.end_date < datetime.now(timezone.utc)
        super(Event, self).save(*args, **kwargs)


class Review(models.Model):
    event = models.ForeignKey(Event, on_delete=models.CASCADE, related_name='reviews')
    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name='reviews')
    rating = models.PositiveIntegerField(validators=[MinValueValidator(1), MaxValueValidator(5)], null=True, blank=True)
    comment = models.TextField(null=True, blank=True)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        verbose_name = 'Review'
        verbose_name_plural = 'Reviews'
        ordering = ['-created_at']
        unique_together = ['event', 'user']

    def __str__(self):
        return f'{self.event.title} - {self.user.email}'

    def save(self, *args, **kwargs):
        super().save(*args, **kwargs)

        self.event.total_reviews = self.event.reviews.count()
        self.event.rating = self.event.reviews.all().aggregate(models.Avg('rating'))['rating__avg']
        self.event.save()
