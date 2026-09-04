from django.urls import path
from drf_yasg import openapi
from drf_yasg.views import get_schema_view
from rest_framework import permissions

from . import views
from .api import BidDetailAPIView, BidListCreateAPIView


schema_view = get_schema_view(
    openapi.Info(
        title="Bid Repair API",
        default_version="v1",
        description="API documentation for the bid repair application.",
        terms_of_service="https://www.google.com/policies/terms/",
        contact=openapi.Contact(email="support@example.com"),
        license=openapi.License(name="BSD License"),
    ),
    public=True,
    permission_classes=(permissions.AllowAny,),
)


urlpatterns = [
    path("", schema_view.with_ui("swagger", cache_timeout=0), name="schema-swagger-ui"),
    path("api/bids/", BidListCreateAPIView.as_view(), name="api_bid_list"),
    path("api/bids/<str:ecgains>/", BidDetailAPIView.as_view(), name="api_bid_detail"),
    path("monitor/", views.monitor, name="monitor"),

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
    
    path(
        "agencies/",
        views.agency_autocomplete,
        name="agency_autocomplete",
    )
]