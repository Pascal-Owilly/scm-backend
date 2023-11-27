from django.db import models
from django.contrib.auth.models import User

class Abattoir(models.Model):
    name = models.CharField(max_length=100)

    def __str__(self):
        return self.name

class Breader(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE)
   
    def __str__(self):
        return self.user.username

class BreaderTrade(models.Model):
    breader = models.ForeignKey(Breader, on_delete=models.CASCADE)
    abattoir = models.ForeignKey(Abattoir, on_delete=models.CASCADE)
    transaction_date = models.DateTimeField(auto_now_add=True)
    breads_supplied = models.PositiveIntegerField()

    def __str__(self):
        return f"{self.breader} supplied {self.breads_supplied} to {self.abattoir} on {self.transaction_date}"

class AbattoirPayment(models.Model):
    abattoir = models.ForeignKey(Abattoir, on_delete=models.CASCADE)
    transaction = models.OneToOneField(BreaderTrade, on_delete=models.CASCADE)
    amount = models.DecimalField(max_digits=10, decimal_places=2)
    payment_date = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"Payment of {self.amount} to {self.abattoir} for {self.transaction}"
