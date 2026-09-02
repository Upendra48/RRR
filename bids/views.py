from django.shortcuts import get_object_or_404, redirect, render

from .forms import BidForm
from .models import Bid


def monitor(request):
    show_current_bids = request.GET.get("has_bids") == "true"
    bids = Bid.objects.select_related("developer").order_by("-date", "-id")

    if show_current_bids:
        bids = bids.filter(has_bids=True)

    return render(
        request,
        "bids/monitor.html",
        {
            "bids": bids,
            "show_current_bids": show_current_bids,
        },
    )


def create_bid(request):
    if request.method == "POST":
        form = BidForm(request.POST)

        if form.is_valid():
            bid = form.save()
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
        form = BidForm(request.POST, instance=bid)

        if form.is_valid():
            form.save()
            return redirect("bid_detail", ecgains=bid.ecgains)

    else:
        form = BidForm(instance=bid)

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
        return redirect("monitor")

    return render(
        request,
        "bids/bid_confirm_delete.html",
        {
            "bid": bid,
        },
    )