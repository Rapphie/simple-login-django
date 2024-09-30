from django.db import models
from django.contrib.auth.models import User
from django.utils import timezone
from datetime import timedelta


class UserLoginAttempt(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    failed_attempts = models.IntegerField(default=0)
    lockout_until = models.DateTimeField(null=True, blank=True)

    def is_locked_out(self):
        if self.lockout_until and self.lockout_until > timezone.now():
            return True
        # Reset failed attempts if lockout period has expired
        self.reset_failed_attempts()
        return False

    def reset_failed_attempts(self):
        self.failed_attempts = 0
        self.lockout_until = None
        self.save()

    def increment_failed_attempts(self):
        self.failed_attempts += 1
        if self.failed_attempts == 3:
            self.lockout_until = timezone.now() + timedelta(minutes=3)
        elif self.failed_attempts >= 3 and self.failed_attempts <= 5:
            self.lockout_until = timezone.now() + timedelta(minutes=5)
        elif self.failed_attempts >= 10:
            self.lockout_until = timezone.now() + timedelta(days=1)
        elif self.failed_attempts >= 50:
            self.lockout_until = timezone.now() + timedelta(days=10)
        self.save()
