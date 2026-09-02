from django import forms
from django.core.validators import RegexValidator

from .models import Bid, Developer


class BidForm(forms.ModelForm):
    ecgains = forms.CharField(
        validators=[
            RegexValidator(
                regex=r"^\d{2}-\d{2}-\d{3}-\d{4}-\d{6}$",
                message="ECGAINS must be in the format 02-03-002-0001-000000.",
            )
        ],
        widget=forms.TextInput(attrs={
            "class": "form-control",
            "placeholder": "Enter ECGAINS",
        }),
    )

    class Meta:
        model = Bid

        fields = [
            "agency_name",
            "ecgains",
            "contact_email",
            "state",
            "initials",
            "bid_url",
            "comments",
            "module_name",
            "developer",
            "bid_type",
            "priority",
            "has_bids",
            "procurement_type",
        ]

        widgets = {
            "agency_name": forms.TextInput(attrs={
                "class": "form-control",
                "placeholder": "Enter agency name",
            }),

            "ecgains": forms.TextInput(attrs={
                "class": "form-control",
                "placeholder": "Enter ECGAINS",
            }),

            "contact_email": forms.EmailInput(attrs={
                "class": "form-control",
                "placeholder": "Enter contact email",
            }),

            "state": forms.TextInput(attrs={
                "class": "form-control",
                "placeholder": "Enter state",
            }),

            "initials": forms.TextInput(attrs={
                "class": "form-control",
                "placeholder": "Enter initials",
            }),

            "bid_url": forms.URLInput(attrs={
                "class": "form-control",
                "placeholder": "https://example.com/bid",
            }),

            "comments": forms.Textarea(attrs={
                "class": "form-control",
                "placeholder": "Enter comments",
                "rows": 4,
            }),

            "module_name": forms.TextInput(attrs={
                "class": "form-control",
                "placeholder": "Enter module name",
            }),

            "developer": forms.Select(attrs={
                "class": "form-select",
            }),

            "bid_type": forms.Select(attrs={
                "class": "form-select",
            }),

            "priority": forms.Select(attrs={
                "class": "form-select",
            }),

            "has_bids": forms.Select(
                choices=[
                    (True, "Yes"),
                    (False, "No"),
                ],
                attrs={
                    "class": "form-select",
                },
            ),

            "procurement_type": forms.Select(attrs={
                "class": "form-select",
            }),
        }

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)

        self.fields["developer"].queryset = (
            Developer.objects
            .all()
            .order_by("name")
        )

        self.fields["developer"].empty_label = "Select Developer"
        self.fields["bid_type"].empty_label = "Select Bid Type"
        self.fields["priority"].empty_label = "Select Priority"
        self.fields["procurement_type"].empty_label = "Select Procurement Type"

    def clean_ecgains(self):
        ecgains = self.cleaned_data.get("ecgains")
        if not ecgains:
            return ecgains

        queryset = Bid.objects.filter(ecgains__iexact=ecgains)
        if self.instance and self.instance.pk:
            queryset = queryset.exclude(pk=self.instance.pk)

        if queryset.exists():
            raise forms.ValidationError("A bid with this ECGAINS already exists.")

        return ecgains

    def clean_bid_url(self):
        bid_url = self.cleaned_data.get("bid_url")
        if bid_url and not bid_url.startswith(("http://", "https://")):
            raise forms.ValidationError("Bid URL must start with http:// or https://.")
        return bid_url
