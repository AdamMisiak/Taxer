from django.db import models
from django.conf import settings
from utils.models import Broker
from core.celery import debug_task

class ReportFile(models.Model):
    file = models.FileField()
    user = models.ForeignKey(
        settings.AUTH_USER_MODEL,
        on_delete=models.CASCADE,
    )
    broker = models.ForeignKey(Broker, blank=True, null=True, on_delete=models.CASCADE)
    created_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        verbose_name = "Report file"
        verbose_name_plural = "Report files"

    def __str__(self):
        return f"{ReportFile.__name__} - {self.file} - {self.broker} - by: {self.user}"

    def save(self, *args, **kwargs):
        if self.id is not None:
            print(f"♻️  Updated: {self}\n")
        else:
            print(f"✅ Created: {self}\n")
        debug_task.delay()
        super(ReportFile, self).save(*args, **kwargs)
