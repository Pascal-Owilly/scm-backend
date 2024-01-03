# from django.db import models
# from custom_registration.models import CustomUser
# from transaction.models import BreaderTrade

# class Status(models.Model):
#     is_dormant = models.BooleanField()  
#     status_title = models.CharField(max_length=100)
#     status_id = models.AutoField(primary_key=True)
#     is_deleted = models.BooleanField()
#     status_narration = models.CharField(max_length=255)
    
#     def __str__(self):
#         return f"Status - {self.status_id}"
# class Bank(models.Model):
#     bank_id = models.AutoField(primary_key=True)
#     bank_name = models.CharField(max_length=50)
#     bank_code = models.CharField(max_length=50, unique=True)
#     bank_abbreviation = models.CharField(max_length=50)
#     swift_code = models.CharField(max_length=50, unique=True)
#     # status_id = models.ForeignKey(Status, on_delete=models.CASCADE)
#     def __str__(self):
#         return self.bank_name 
          
# class BankBranch(models.Model):
#     bank_branch_id = models.AutoField(primary_key=True)
#     # bank_id = models.ForeignKey(Bank, on_delete=models.CASCADE)
#     bank_branch_name = models.CharField(max_length=100)
#     branch_code = models.CharField(max_length=50, unique=True)
#     status_id = models.ForeignKey(Status, on_delete=models.CASCADE)
#     head_office = models.CharField(max_length=100)
#     def __str__(self):
#         return self.bank_branch_name
    
# class Payment(models.Model):
#     payments_id = models.AutoField(primary_key=True)
#     payment_code = models.CharField(max_length=50)
#     amount = models.DecimalField(max_digits=18, decimal_places=2)
#     payment_initiation_date = models.DateTimeField(auto_now_add=True)
#     # breeder_trade = models.ForeignKey(BreaderTrade, on_delete=models.CASCADE, related_name='breeder_payments')
#     national_id = models.CharField(max_length=50, unique=True)
#     mobile_number = models.CharField(max_length=15)  # Adjust the max_length as needed
#     breeder_id = models.ForeignKey(CustomUser, on_delete=models.CASCADE)
#     # bank_id = models.ForeignKey(Bank, on_delete=models.CASCADE)
#     # bank_branch_id = models.ForeignKey(BankBranch, on_delete=models.CASCADE)
#     teller_id = models.ForeignKey(CustomUser, on_delete=models.CASCADE, related_name='payment_teller', related_query_name='payment_tellers')
#     status_id = models.ForeignKey(Status, on_delete=models.CASCADE)
#     def __str__(self):
#         return f"Payment - {self.payments_id}"

# class BankUser(models.Model):
#     bank_user_id = models.AutoField(primary_key=True)
#     user_id = models.ForeignKey(CustomUser, on_delete=models.CASCADE)
#     bank_id = models.ForeignKey(Bank, on_delete=models.CASCADE)
#     status_id = models.ForeignKey(Status, on_delete=models.CASCADE)
#     def __str__(self):
#         return f"Bank User - {self.bank_user_id}"

# class AuditTrail(models.Model):
#     audit_trail_id = models.AutoField(primary_key=True)
#     action = models.CharField(max_length=255)
#     action_date = models.DateTimeField()
#     ip_address = models.GenericIPAddressField()
#     user_id = models.IntegerField()
#     narration = models.TextField()
#     hash_code = models.CharField(max_length=255)
#     module_url = models.URLField()
# class Currency(models.Model):
#     currency_id = models.AutoField(primary_key=True)
#     currency_code = models.CharField(max_length=10)
#     currency_name = models.CharField(max_length=255)
#     symbol = models.CharField(max_length=10)
#     country = models.CharField(max_length=255)
# class DisbursementMode(models.Model):
#     disbursement_mode_id = models.AutoField(primary_key=True)
#     disbursement_type = models.CharField(max_length=255)
#     status_id = models.IntegerField()
# class Alert(models.Model):
#     alert_id = models.AutoField(primary_key=True)
#     message = models.TextField()
#     receiver = models.CharField(max_length=255)
#     sender = models.CharField(max_length=255)
#     sender_password = models.CharField(max_length=255)
#     delivery_channel = models.CharField(max_length=255)
#     attachment = models.CharField(max_length=255)
#     email = models.EmailField()
#     password = models.CharField(max_length=255)
#     recipient = models.CharField(max_length=255)
#     status = models.CharField(max_length=255)
#     retry_attempts = models.IntegerField()
#     alert_time = models.DateTimeField()
#     status_id = models.IntegerField()
# class Financier(models.Model):
#     financier_id = models.AutoField(primary_key=True)
#     first_name = models.CharField(max_length=50)
#     other_name = models.CharField(max_length=100)
#     mobile_number = models.CharField(max_length=10, unique=True)
#     email = models.EmailField(unique=True)
#     narration = models.CharField(max_length=255)
#     user_id = models.ForeignKey(CustomUser  , on_delete=models.CASCADE)
#     status_id = models.ForeignKey(Status, on_delete=models.CASCADE)
#     def __str__(self):
#         return f"Financier - {self.financier_id}"
# class FinancierUser(models.Model):
#     financier_user_id = models.AutoField(primary_key=True)
#     user_id = models.ForeignKey(CustomUser, on_delete=models.CASCADE)
#     financier_id = models.ForeignKey(Financier, on_delete=models.CASCADE)
#     status_id = models.ForeignKey(Status, on_delete=models.CASCADE)
#     def __str__(self):
#         return f"Financier User - {self.financier_user_id}" 