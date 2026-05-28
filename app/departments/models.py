from django.db import models
from django.core.exceptions import ValidationError


class Department(models.Model):
    name = models.CharField(max_length=200)
    parent = models.ForeignKey(
        "self",
        null=True,
        blank=True,
        on_delete=models.CASCADE,
        related_name="children",
    )
    created_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        constraints = [
            models.UniqueConstraint(
                fields=["parent", "name"],
                name="unique_department_name_per_parent",
            )
        ]

    def clean(self):
        if self.name:
            self.name = self.name.strip()

        if self.parent and self.parent_id == self.id:
            raise ValidationError("Department cannot be parent of itself.")