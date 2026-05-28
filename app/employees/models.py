from django.db import models
from django.core.exceptions import ValidationError


class Employee(models.Model):
    department = models.ForeignKey(
        "departments.Department",
        on_delete=models.CASCADE,
        related_name="employees",
    )

    full_name = models.CharField(max_length=200)
    position = models.CharField(max_length=200)
    hired_at = models.DateField(null=True, blank=True)

    created_at = models.DateTimeField(auto_now_add=True)

    def clean(self):
        if self.full_name:
            self.full_name = self.full_name.strip()

        if self.position:
            self.position = self.position.strip()

        if not self.department:
            raise ValidationError("Employee must belong to a department.")