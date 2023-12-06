# from django.db.models.signals import post_save, post_delete
# from django.dispatch import receiver
# from django.db import models
# from transaction.models import BreaderTrade
# from inventory_management.models import PartsSales, Inventory

# @receiver(post_save, sender=BreaderTrade)
# @receiver(post_delete, sender=BreaderTrade)
# @receiver(post_save, sender=PartsSales)
# @receiver(post_delete, sender=PartsSales)
# def update_inventory(sender, instance, **kwargs):
#     animal_name = instance.animal_name

#     total_breads_supplied = BreaderTrade.objects.filter(animal_name=animal_name).aggregate(models.Sum('breads_supplied'))['breads_supplied__sum'] or 0
#     total_quantity_sold = PartsSales.objects.filter(animal_name=animal_name).aggregate(models.Sum('quantity_sold'))['quantity_sold__sum'] or 0

#     inventory_item, created = Inventory.objects.get_or_create(animal_name=animal_name, status='in_yard')
#     inventory_item.quantity_total = total_breads_supplied
#     inventory_item.quantity_left = total_breads_supplied - total_quantity_sold
#     inventory_item.save()

# @receiver(post_save, sender=BreaderTrade)
# def update_inventory_on_breader_trade(sender, instance, created, **kwargs):
#     if created:  # Only perform this on the creation of a new BreaderTrade instance
#         animal_name = instance.animal_name

#         # Retrieve all Inventory objects for the given breed
#         inventory_items = Inventory.objects.filter(animal_name=animal_name, status='in_yard')

#         # Update each Inventory object
#         for inventory_item in inventory_items:
#             inventory_item.quantity_total += instance.breads_supplied
#             inventory_item.quantity_left += instance.breads_supplied
#             inventory_item.save()

# @receiver(post_save, sender=PartsSales)
# @receiver(post_delete, sender=PartsSales)
# def update_inventory_on_parts_sale(sender, instance, **kwargs):
#     # Update inventory when a new PartsSales is added or an existing one is deleted
#     animal_name = instance.animal_name
#     total_breads_supplied = BreaderTrade.objects.filter(animal_name=animal_name).aggregate(models.Sum('breads_supplied'))['breads_supplied__sum'] or 0

#     inventory_item, created = Inventory.objects.get_or_create(animal_name=animal_name, status='in_yard')
#     inventory_item.quantity_total = total_breads_supplied
#     quantity_sold_sum = PartsSales.objects.filter(animal_name=animal_name).aggregate(models.Sum('quantity_sold'))['quantity_sold__sum']
#     inventory_item.quantity_left = total_breads_supplied - quantity_sold_sum if quantity_sold_sum is not None else 0
#     inventory_item.save()
