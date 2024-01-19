from django import forms
from django.contrib.auth import get_user_model

User = get_user_model()


class UserProfileForm(forms.ModelForm):
    class Meta:
        model = User
        fields = (
            "first_name",
            "last_name",
            "default_phone_number",
            "default_street_address1",
            "default_street_address2",
            "default_town_or_city",
            "default_postcode",
            "default_country",
            "default_county",
        )

    def __init__(self, *args, **kwargs):
        """Add placeholders and classes, remove auto-generated
        labels and set autofocus on first field.
        """
        super().__init__(*args, **kwargs)
        placeholders = {
            "first_name": "First Name",
            "last_name": "Last Name",
            "default_phone_number": "Phone Number",
            "default_postcode": "Postal Code",
            "default_town_or_city": "Town or City",
            "default_street_address1": "Street Address 1",
            "default_street_address2": "Street Address 2",
            "default_county": "County, State or Locality",
        }

        self.fields["first_name"].widget.attrs["autofocus"] = True
        for field in self.fields:
            if field != "default_country":
                if self.fields[field].required:
                    placeholder = f"{placeholders[field]} *"
                else:
                    placeholder = placeholders[field]
                self.fields[field].widget.attrs["placeholder"] = placeholder
                self.fields[field].widget.attrs["class"] = "stripe-style-input"
                self.fields[field].label = False
