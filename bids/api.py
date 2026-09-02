from rest_framework import generics, permissions, serializers

from .models import Bid


class BidSerializer(serializers.ModelSerializer):
    developer_name = serializers.CharField(source="developer.name", read_only=True)

    class Meta:
        model = Bid
        fields = (
            "id",
            "agency_name",
            "ecgains",
            "contact_email",
            "state",
            "initials",
            "date",
            "bid_url",
            "comments",
            "module_name",
            "developer",
            "developer_name",
            "bid_type",
            "priority",
            "has_bids",
            "procurement_type",
            "created_at",
            "updated_at",
        )
        read_only_fields = (
            "id",
            "date",
            "created_at",
            "updated_at",
            "developer_name",
        )


class BidListCreateAPIView(generics.ListCreateAPIView):
    queryset = Bid.objects.select_related("developer").order_by("-date", "-id")
    serializer_class = BidSerializer
    permission_classes = [permissions.AllowAny]


class BidDetailAPIView(generics.RetrieveUpdateDestroyAPIView):
    queryset = Bid.objects.select_related("developer").order_by("-date", "-id")
    serializer_class = BidSerializer
    permission_classes = [permissions.AllowAny]
    lookup_field = "ecgains"
