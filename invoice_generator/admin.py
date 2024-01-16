from django.contrib import admin, messages
from invoice_generator.models import Invoice, Buyer, Product, Item, PurchaseOrder

from django.http import HttpResponseRedirect
from django.urls import reverse
from django.core.mail import send_mail
from django.shortcuts import get_object_or_404


@admin.register(Invoice)
class InvoiceAdmin(admin.ModelAdmin):
    list_display = ('invoice_number', 'buyer', 'invoice_date', 'total_amount')

@admin.register(Buyer)
class BuyerAdmin(admin.ModelAdmin):
    list_display = ('username',)

@admin.register(Product)
class ProductAdmin(admin.ModelAdmin):
    list_display = ('breed', 'part_name', 'sale_type', 'unit_price')

@admin.register(Item)
class ItemAdmin(admin.ModelAdmin):
    list_display = ('product', 'quantity', 'total_price')

@admin.register(PurchaseOrder)
class PurchaseOrderAdmin(admin.ModelAdmin):
    list_display = ('purchase_order_number', 'buyer', 'purchase_order_date', 'status')
    actions = ['notify_buyer_action']

    def notify_buyer_action(self, request, queryset):
        for purchase_order in queryset:
            if purchase_order.status == 'pending':
                # Update the purchase order status to 'under review'
                purchase_order.status = 'under_review'
                purchase_order.save()

                # Send a notification to the buyer
                buyer_message = f"Your purchase order (#{purchase_order.purchase_order_number}) has been received and is under review."
                messages.success(request, buyer_message)

                # Send an email to the buyer
                subject = 'Purchase Order Received and Under Review'
                message = f"Dear {purchase_order.buyer.username},\n\n{buyer_message}\n\nThank you!"
                from_email = 'pascalouma54@gmail.com' 
                to_email = [purchase_order.buyer.username.email]

                send_mail(subject, message, from_email, to_email, fail_silently=False)

            else:
                messages.warning(request, f"This purchase order ({purchase_order.purchase_order_number}) is already under review.")

        return HttpResponseRedirect(reverse('admin:invoice_generator_purchaseorder_changelist'))

    notify_buyer_action.short_description = "Notify Buyers and Mark as Under Review"
