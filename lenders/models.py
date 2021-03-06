from django.db import models


class Lender(models.Model):
    name = models.CharField(max_length=200)
    code = models.CharField(max_length=3)
    upfront_commistion_rate = models.DecimalField(max_digits=7, decimal_places=2)
    trait_commistion_rate = models.DecimalField(max_digits=7, decimal_places=2)
    active = models.BooleanField(default=False, null=False)

    class Meta:
        ordering = ['-id']

    def __str__(self):
        return self.name
