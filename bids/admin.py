from django.contrib import admin

from .models import ArchivedBid, Bid, Developer


@admin.register(ArchivedBid)
class ArchivedBidAdmin(admin.ModelAdmin):
    list_display = (
        "agency_name",
        "ecgains",
        "developer_name",
        "deleted_at",
    )
    search_fields = ("agency_name", "ecgains", "developer_name")
    list_filter = ("priority", "bid_type", "procurement_type")
    readonly_fields = tuple(field.name for field in ArchivedBid._meta.fields)


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