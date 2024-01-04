from django.db import models


class ImportFile(models.Model):
    file = models.FileField()
    # NOTE user
    # owner = models.ForeignKey(
    #     settings.AUTH_USER_MODEL,
    #     on_delete=models.CASCADE,
    # )
    # NOTE broker
    # broker = models.relation(max_length=100, default="API")
    created_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        verbose_name = "Import file"
        verbose_name_plural = "Import files"

    def __str__(self):
        return f"{self.file}"
