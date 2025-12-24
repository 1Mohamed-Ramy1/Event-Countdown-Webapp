import uuid
from django.db import models

class Event(models.Model):
    STATUS_RUNNING = "running"
    STATUS_PAUSED = "paused"
    STATUS_FINISHED = "finished"

    STATUS_CHOICES = [
        (STATUS_RUNNING, "Running"),
        (STATUS_PAUSED, "Paused"),
        (STATUS_FINISHED, "Finished"),
    ]

    uid = models.UUIDField(default=uuid.uuid4, editable=False, unique=True)
    name = models.CharField(max_length=200)
    event_date = models.DateTimeField()  # target datetime when running
    created_at = models.DateTimeField(auto_now_add=True)

    # persist pause/resume state:
    remaining_seconds = models.BigIntegerField(null=True, blank=True,
                                               help_text="Remaining seconds when paused. Null = running.")
    status = models.CharField(max_length=16, choices=STATUS_CHOICES, default=STATUS_RUNNING)
    updated_at = models.DateTimeField(auto_now=True)

    def __str__(self):
        return f"{self.name} ({self.uid})"
