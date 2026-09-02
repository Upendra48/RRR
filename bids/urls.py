from django.urls import path

from . import views


urlpatterns = [
    path("", views.monitor, name="monitor"),

    path(
        "bids/",
        views.create_bid,
        name="create_bid",
    ),

    path(
        "bids/<str:ecgains>/",
        views.bid_detail,
        name="bid_detail",
    ),

    path(
        "bids/<str:ecgains>/edit/",
        views.edit_bid,
        name="edit_bid",
    ),

    path(
        "bids/<str:ecgains>/delete/",
        views.delete_bid,
        name="delete_bid",
    ),
]