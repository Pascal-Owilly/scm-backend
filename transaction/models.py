from django.db import models
from django.contrib.auth.models import User
from phonenumber_field.modelfields import PhoneNumberField


class Abattoir(models.Model):
    name = models.CharField(max_length=100)

    def __str__(self):
        return self.name

class Breader(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE)
   
    def __str__(self):
        return self.user.username

class BreaderTrade(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE, null=True)
    breader = models.ForeignKey(Breader, on_delete=models.CASCADE)
    abattoir = models.ForeignKey(Abattoir, on_delete=models.CASCADE)
    transaction_date = models.DateTimeField(auto_now_add=True)
    breads_supplied = models.PositiveIntegerField(default=0)
    goat_weight = models.PositiveIntegerField(default=0)
    community = models.CharField(max_length=255, default='Example ABC Community')
    market = models.CharField(max_length=255, default='ABC Market')
    head_of_family = models.CharField(max_length=255, default='Example ABC Family')
    vaccinated = models.BooleanField(default=False)
    animal_name = models.CharField(max_length=255, default='eg goats, cows... etc')
    
    # Add the new fields
    price = models.DecimalField(max_digits=10, decimal_places=2, default=0.00)
    phone_number = PhoneNumberField(null=True)
    
    def __str__(self):
        formatted_date = self.transaction_date.strftime('%d %b %Y %H:%M:%S')
        return f"{self.market} from {self.community} supplied {self.breads_supplied} {self.animal_name}'s to {self.abattoir} on {formatted_date}"

class AbattoirPaymentToBreader(models.Model):
    breader_trade = models.ForeignKey(BreaderTrade, on_delete=models.CASCADE)
    amount = models.DecimalField(max_digits=10, decimal_places=2)
    payment_date = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"Payment of {self.amount} to {self.breader_trade.breader} for {self.breader_trade}"
