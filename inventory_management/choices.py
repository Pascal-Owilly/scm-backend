from django.db import models

BREED_CHOICES = [
    ('goats', 'Goats'),
    ('sheep', 'Sheep'),
    ('cows', 'Cows'),
    ('pigs', 'Pigs'),
    # Add more choices as needed
]

PART_CHOICES = [
    ('ribs', 'Ribs'),
    ('thighs', 'Thighs'),
    ('loin', 'Loin'),
    ('shoulder', 'Shoulder'),
    ('shanks', 'Shanks'),
    ('organ_meat', 'Organ Meat'),
    ('intestines', 'Intestines'),
    ('tripe', 'Tripe'),
    ('sweetbreads', 'Sweetbreads'),
]

STATUS_CHOICES = [
        ('in_the warehouse', 'In The Warehouse'),
        ('slaughtered', 'Slaughtered'),
        ('sold', 'Sold'),
]

SALE_CHOICES = [
    ('export_cut', 'Export Cut'),
    ('local_sale', 'Local Sale Cut'),
]