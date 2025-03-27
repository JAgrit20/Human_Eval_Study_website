from django.db import models
from django.utils import timezone
class Todo(models.Model):
    # Remove the 'user' ForeignKey field if you added it previously
    # user = models.ForeignKey(...) # <-- DELETE or COMMENT OUT this line

    # Add this field to store the session key
    session_key = models.CharField(max_length=40, db_index=True, null=True, blank=True)

    # Keep other fields
    title = models.CharField(max_length=200)
    completed = models.BooleanField(default=False)
    created_at = models.DateTimeField(default=timezone.now)

    def __str__(self):
        # Update string representation if needed
        return f"{self.title} (Session: {self.session_key or 'N/A'})"

