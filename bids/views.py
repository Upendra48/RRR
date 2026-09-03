from django.contrib import messages
from django.shortcuts import get_object_or_404, redirect, render

from .forms import BidForm, BidUpdateForm
from .models import Bid
from django.db.models import Q


def monitor(request):
    show_current_bids = request.GET.get("has_bids") == "true"
    priority = request.GET.get("priority")
    q = request.GET.get("q", "").strip()

    bids = Bid.objects.select_related("developer").order_by("-date", "-id")

    if q:
        bids = bids.filter(
        Q(agency_name__icontains=q) |
        Q(ecgains__icontains=q)
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