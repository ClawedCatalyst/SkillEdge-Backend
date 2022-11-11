from django.db import models
from base.models import NewUserRegistration

# Create your models here.

class Order(models.Model):
    user_mail = models.ForeignKey(NewUserRegistration, on_delete=models.CASCADE)
    order_amount = models.CharField(max_length=25)
    order_payment_id = models.CharField(max_length=100)
    order_date = models.DateTimeField(auto_now=True)

    def __str__(self):
        return self.order_payment_id
