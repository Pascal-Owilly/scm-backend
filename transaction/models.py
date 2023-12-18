from django.db import models
from django.db.models.signals import post_save
from django.dispatch import receiver
from phonenumber_field.modelfields import PhoneNumberField
from custom_registration.models import CustomUser

class Abattoir(models.Model):

    user = models.OneToOneField(CustomUser, on_delete=models.CASCADE)
    
    def __str__(self):

        return self.user.username

class Breader(models.Model):

    user = models.OneToOneField(CustomUser, on_delete=models.CASCADE)

    def __str__(self):

        return self.user.username


class BreaderTrade(models.Model):

    BREED_CHOICES = [
        ('goats', 'Goats'),
        ('sheep', 'Sheep'),
        ('cows', 'Cows'),
        ('pigs', 'Pigs'),
        # Add more choices as needed
    ]

    breeder = models.ForeignKey(CustomUser, on_delete=models.CASCADE, default=1)
    abattoir = models.ForeignKey(Abattoir, on_delete=models.CASCADE)
    transaction_date = models.DateTimeField(auto_now_add=True)
    breed = models.CharField(max_length=255, choices=BREED_CHOICES, default='goats')
    breeds_supplied = models.PositiveIntegerField(default=0)
    goat_weight = models.PositiveIntegerField(default=0)
    vaccinated = models.BooleanField(default=False)
    # Add the new fields
    price = models.DecimalField(max_digits=10, decimal_places=2, default=0.00)
    phone_number = PhoneNumberField(null=True)
    
    def __str__(self):
        formatted_date = self.transaction_date.strftime('%d %b %Y %H:%M:%S')
        return f"{self.breeder.market} from {self.breeder.community} supplied {self.breeds_supplied} {self.breed}'s to {self.abattoir} on {formatted_date}"

# @receiver(post_save, sender=BreaderTrade)
# def update_breads_supplied(sender, instance, **kwargs):
#     # Update breeds_supplied field after saving
#     aggregated_sum = BreaderTrade.objects.filter(breader=instance.breader).aggregate(models.Sum('breads_supplied'))['breads_supplied__sum']
#     print(f"Aggregated sum for {instance.breader}: {aggregated_sum}")
#     instance.breads_supplied = aggregated_sum if aggregated_sum is not None else 0
#     instance.save()

# # Connect the signal
# post_save.connect(update_breads_supplied, sender=BreaderTrade)


class AbattoirPaymentToBreader(models.Model):
    breader_trade = models.ForeignKey(BreaderTrade, on_delete=models.CASCADE)
    amount = models.DecimalField(max_digits=10, decimal_places=2)
    payment_date = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"Payment of {self.amount} to {self.breader_trade.breeder} for {self.breader_trade}"
