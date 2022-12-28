from django.db import models

# Create your models here.
class SchoolModel(models.Model):
    name = models.CharField(max_length=50)
    start_date = models.DateField()
    distance = models.FloatField()

    def __str__(self) -> str:
        return self.name