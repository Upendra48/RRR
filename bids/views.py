from django.contrib import messages
from django.db import transaction
from django.shortcuts import get_object_or_404, redirect, render

from .forms import BidForm, BidUpdateForm
from .models import ArchivedBid, Bid
from django.db.models import Q


def monitor(request):
    show_current_bids = request.GET.get("has_bids") == "true"
    priority = request.GET.get("priority")
    q = request.GET.get("q", "").strip()

    bids = Bid.objects.select_related("developer").order_by("-date", "-id")

    if q:
        bids = bids.filter(
        Q(ecgains__icontains=q) |
        Q(developer__name__istartswith=q)
        )

    if priority:
        bids = bids.filter(priority=priority)

    if show_current_bids:
        bids = bids.filter(has_bids=True)

    return render(
        request,
        "bids/monitor.html",
        {
            "bids": bids,
            "show_current_bids": show_current_bids,
            "query": q,
            "selected_priority": priority,
        },
    )


def create_bid(request):
    if request.method == "POST":
        form = BidForm(request.POST)

        if form.is_valid():
            bid = form.save()
            messages.success(request, "Bid request created successfully.")
            return redirect("bid_detail", ecgains=bid.ecgains)
    else:
        form = BidForm()

    return render(
        request,
        "bids/bid_form.html",
        {
            "form": form,
            "page_title": "Create Request",
        },
    )


def bid_detail(request, ecgains):
    bid = get_object_or_404(Bid, ecgains=ecgains)

    return render(
        request,
        "bids/bid_detail.html",
        {
            "bid": bid,
        },
    )


def edit_bid(request, ecgains):
    bid = get_object_or_404(Bid, ecgains=ecgains)

    if request.method == "POST":
        form = BidUpdateForm(request.POST, instance=bid)

        if form.is_valid():
            form.save()
            messages.success(request, "Bid request updated successfully.")
            return redirect("bid_detail", ecgains=bid.ecgains)
    else:
        form = BidUpdateForm(instance=bid)

    return render(
        request,
        "bids/bid_form.html",
        {
            "form": form,
            "bid": bid,
            "page_title": "Edit Request",
        },
    )


def delete_bid(request, ecgains):
    bid = get_object_or_404(Bid, ecgains=ecgains)

    if request.method == "POST":
        with transaction.atomic():
            ArchivedBid.objects.create(
                original_bid_id=bid.pk,
                agency_name=bid.agency_name,
                ecgains=bid.ecgains,
                contact_email=bid.contact_email,
                state=bid.state,
                initials=bid.initials,
                date=bid.date,
                bid_url=bid.bid_url,
                comments=bid.comments,
                module_name=bid.module_name,
                developer_name=bid.developer.name,
                bid_type=bid.bid_type,
                priority=bid.priority,
                has_bids=bid.has_bids,
                procurement_type=bid.procurement_type,
                created_at=bid.created_at,
                updated_at=bid.updated_at,
            )
            bid.delete()
        messages.success(request, "Bid request deleted successfully.")
        return redirect("monitor")

    return render(
        request,
        "bids/bid_confirm_delete.html",
        {
            "bid": bid,
        },
    )