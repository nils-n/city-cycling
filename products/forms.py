from django import forms
from products.models import Product, Category, Season


class ProductForm(forms.ModelForm):
    class Meta:
        model = Product
        fields = "__all__"
        exclude = ("rating", "has_comments", "has_sizes", "has_rating")

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        categories = Category.objects.all()
        seasons = Season.objects.all()

        friendly_category_names = [
            (c.id, c.get_friendly_name()) for c in categories
        ]
        self.fields["category"].choices = friendly_category_names

        friendly_seasons_names = [
            (s.id, s.get_friendly_name()) for s in seasons
        ]
        self.fields["season"].choices = friendly_seasons_names
