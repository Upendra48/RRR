from django.contrib import admin

from .models import Bid, Developer


@admin.register(Developer)
class DeveloperAdmin(admin.ModelAdmin):
    list_display = ("name", "active")
    list_filter = ("active",)
    search_fields = ("name",)


@admin.register(Bid)
class BidAdmin(admin.ModelAdmin):
    list_display = (
        "agency_name",
        "ecgains",
        "developer",
        "bid_type",
        "priority",
        "has_bids",
        "procurement_type",
        "date",
    )
    list_filter = (
        "developer",
        "state",
        "bid_type",
        "priority",
        "has_bids",
        "procurement_type",
    )
    search_fields = (
        "agency_name",
        "ecgains",
    )