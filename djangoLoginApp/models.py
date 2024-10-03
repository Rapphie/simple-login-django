from django.db import models
from django.contrib.auth.models import User
from django.utils import timezone
from datetime import timedelta


class UserLoginAttempt(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    failed_attempts = models.IntegerField(default=0)
    lockout_until = models.DateTimeField(null=True, blank=True)

    def is_locked_out(self):
        return self.lockout_until is not None and self.lockout_until > timezone.now()

    def reset_failed_attempts(self):
        self.failed_attempts = 0
        self.lockout_until = None
        self.save()

    def increment_failed_attempts(self):
        if not self.is_locked_out():
            self.failed_attempts += 1
            if self.failed_attempts == 3:
                self.lockout_until = timezone.now() + timedelta(minutes=5)
            self.save()
