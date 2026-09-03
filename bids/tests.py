from django.test import TestCase
from django.urls import reverse

from .models import ArchivedBid, Bid, Developer


class BidFeatureTests(TestCase):
    def setUp(self):
        self.developer = Developer.objects.create(name="Test Developer", active=True)

    def _make_bid(self, **kwargs):
        defaults = {
            "agency_name": "Test Agency",
            "ecgains": "02-03-002-0001-000000",
            "contact_email": "agency@example.com",
            "state": "TX",
            "initials": "TR",
            "bid_url": "https://example.com/bid",
            "comments": "Test comments",
            "module_name": "Test Module",
            "developer": self.developer,
            "bid_type": Bid.BidType.NEW,
            "priority": Bid.Priority.NORMAL,
            "has_bids": False,
            "procurement_type": Bid.ProcurementType.BIDNET_AMR,
        }
        defaults.update(kwargs)
        return Bid.objects.create(**defaults)

    def test_duplicate_ecgains_is_rejected(self):
        self._make_bid()

        form = self.client.post(
            reverse("create_bid"),
            {
                "agency_name": "Another Agency",
                "ecgains": "02-03-002-0001-000000",
                "contact_email": "another@example.com",
                "state": "CA",
                "initials": "AB",
                "bid_url": "https://example.com/another",
                "comments": "Duplicate",
                "module_name": "Another Module",
                "developer": str(self.developer.pk),
                "bid_type": Bid.BidType.NEW,
                "priority": Bid.Priority.HIGH,
                "has_bids": "True",
                "procurement_type": Bid.ProcurementType.DEMANDSTAR_AMR,
            },
        )

        self.assertEqual(form.status_code, 200)
        self.assertContains(form, "already exists")

    def test_monitor_filters_by_search_and_priority(self):
        self._make_bid(agency_name="Alpha Agency", ecgains="02-03-002-0001-000001", priority=Bid.Priority.HIGH, has_bids=True)
        self._make_bid(agency_name="Beta Agency", ecgains="02-03-002-0001-000002", priority=Bid.Priority.NORMAL, has_bids=False)

        response = self.client.get(reverse("monitor"), {"q": "Alpha", "priority": Bid.Priority.HIGH})

        self.assertContains(response, "Alpha Agency")
        self.assertNotContains(response, "Beta Agency")

    def test_delete_archives_bid_before_removing_it(self):
        bid = self._make_bid()

        response = self.client.post(reverse("delete_bid", args=[bid.ecgains]))

        self.assertRedirects(response, reverse("monitor"))
        self.assertFalse(Bid.objects.filter(pk=bid.pk).exists())
        archived_bid = ArchivedBid.objects.get(original_bid_id=bid.pk)
        self.assertEqual(archived_bid.ecgains, bid.ecgains)
        self.assertEqual(archived_bid.agency_name, bid.agency_name)
        self.assertEqual(archived_bid.developer_name, self.developer.name)
