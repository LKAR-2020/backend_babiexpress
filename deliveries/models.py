from django.db import models
from django.conf import settings

class Package(models.Model):
    sender = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE, related_name='sent_packages')
    recipient_name = models.CharField(max_length=255)
    recipient_phone = models.CharField(max_length=15)
    pickup_address = models.CharField(max_length=255)
    delivery_address = models.CharField(max_length=255)
    estimated_delivery_date = models.DateField(null=True, blank=True)
    special_instructions = models.TextField(null=True, blank=True) #Instructions de livraison spéciales
    photo = models.ImageField(upload_to='package_photos/', null=True, blank=True) #Photo du colis (pour vérifier l'état du colis à la livraison)
    weight = models.DecimalField(max_digits=5, decimal_places=2)
    dimensions = models.CharField(max_length=50)
    description = models.TextField(null=True, blank=True)
    created_at = models.DateTimeField(auto_now_add=True)
    status = models.CharField(max_length=20, choices=[
        ('en_attente', 'En attente'),
        ('en_cours', 'En cours'),
        ('délivré', 'Délivré'),
        ('annulé', 'Annulé')
    ])

class Delivery(models.Model):
    package = models.OneToOneField(Package, on_delete=models.CASCADE)
    courier = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE, related_name='deliveries')
    pickup_latitude = models.DecimalField(max_digits=9, decimal_places=6, null=True, blank=True) #Coordonnées GPS du point de ramassage:
    pickup_longitude = models.DecimalField(max_digits=9, decimal_places=6, null=True, blank=True) #Coordonnées GPS du point de ramassage:
    delivery_latitude = models.DecimalField(max_digits=9, decimal_places=6, null=True, blank=True) #Coordonnées GPS du point de livraison:
    delivery_longitude = models.DecimalField(max_digits=9, decimal_places=6, null=True, blank=True) #Coordonnées GPS du point de livraison:
    pickup_time = models.DateTimeField(null=True, blank=True)
    total_distance = models.DecimalField(max_digits=10, decimal_places=2, null=True, blank=True) #Distance totale parcourue
    delivery_time = models.DateTimeField(null=True, blank=True)
    status = models.CharField(max_length=20, choices=[
        ('attribué', 'Attribué'),
        ('récupéré', 'Récupéré'),
        ('en_cours', 'En cours'),
        ('délivré', 'Délivré'),
        ('annulé', 'Annulé')
    ])
    price = models.DecimalField(max_digits=10, decimal_places=2, null=True, blank=True)

class Payment(models.Model):
    delivery = models.OneToOneField(Delivery, on_delete=models.CASCADE)
    amount = models.DecimalField(max_digits=10, decimal_places=2)
    payment_method = models.CharField(max_length=50, choices=[
        ('credit_card', 'Credit Card'),
        ('paypal', 'PayPal'),
        ('mobile_money','Mobile money'),
        ('wave', 'Wave'),
        ('cash', 'Cash')
    ])
    payment_status = models.CharField(max_length=20, choices=[
        ('en_attente', 'En attente'),
        ('terminé', 'Terminé'),
        ('échoué', 'Echoué')
    ])
    created_at = models.DateTimeField(auto_now_add=True)

class Notification(models.Model):
    user = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE)
    message = models.CharField(max_length=255)
    read = models.BooleanField(default=False)
    created_at = models.DateTimeField(auto_now_add=True)
    notification_type = models.CharField(max_length=50, choices=[
    ('info', 'Info'),
    ('attention', 'Attention'),
    ('succès', 'Succès')
])


class PackageHistory(models.Model):
    package = models.ForeignKey(Package, on_delete=models.CASCADE)
    action = models.CharField(max_length=50, choices=[
        ('created', 'Created'),
        ('updated', 'Updated'),
        ('deleted', 'Deleted'),
        ('status_changed', 'Status Changed')
    ])
    timestamp = models.DateTimeField(auto_now_add=True)

class SupportTicket(models.Model):
    user = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE)
    subject = models.CharField(max_length=255)
    description = models.TextField()
    status = models.CharField(max_length=20, choices=[
        ('open', 'Open'),
        ('in_progress', 'In Progress'),
        ('closed', 'Closed')
    ])
    created_at = models.DateTimeField(auto_now_add=True)
    priority = models.CharField(max_length=20, choices=[
    ('faible', 'Faible'),
    ('medium', 'Medium'),
    ('élevé', 'Elevé'),
    ('urgent', 'Urgent')
])

