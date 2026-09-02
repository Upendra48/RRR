from django.db import models

# Model representing a developer
class Developer(models.Model):
    name = models.CharField(max_length=100)
    active = models.BooleanField(default=True)
    
    def __str__(self):
        return self.name
    
class Bid(models.Model):
    class BidType(models.TextChoices):
        NEW = "New",
        UPDATE_REPAIR = "Update/Repair"
        
    class Priority(models.TextChoices):
        HIGH = "High",
        NORMAL = "Normal",
        
    class ProcurementType(models.TextChoices):
        PROCUREMENT_SPIDER = "Procurement Spider",
        BONFIRE_SPIDER = "Bonfire Spider",
        BIDNET_AMR = "Bidnet AMR",
        DEMANDSTAR_AMR = "Demandstar AMR",
        
    agency_name = models.CharField(max_length=255)
    ecgains = models.CharField(
        max_length=100,
        unique=True,
    )
    contact_email = models.EmailField()
    state = models.CharField(max_length=100)
    initials = models.CharField(max_length=20)
    
    date = models.DateField(auto_now_add=True)
    
    bid_url = models.URLField(max_length=1000)
    comments = models.TextField(blank=True) 
    module_name = models.CharField(max_length=255, blank=True)
    
    developer = models.ForeignKey(Developer, on_delete=models.PROTECT, related_name='bids')
    
    bid_type = models.CharField(max_length=20, choices=BidType.choices)
    
    priority = models.CharField(max_length=20, choices=Priority.choices, default=Priority.NORMAL)
    
    has_bids = models.BooleanField(default=False)
    
    procurement_type = models.CharField(max_length=50, choices=ProcurementType.choices,) 
    
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    
    def __str__(self):
        return f"{self.agency_name} - {self.ecgains}"          