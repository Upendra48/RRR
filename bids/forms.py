from django import forms

from .models import Bid, Developer


class BidForm(forms.ModelForm):
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

        # Only show active developers
        self.fields["developer"].queryset = (
            Developer.objects
            .all()
            .order_by("name")
        )

        # Add empty option to dropdowns
        self.fields["developer"].empty_label = "Select Developer"
        self.fields["bid_type"].empty_label = "Select Bid Type"
        self.fields["priority"].empty_label = "Select Priority"
        self.fields["procurement_type"].empty_label = "Select Procurement Type"