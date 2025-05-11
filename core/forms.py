from django import forms
from .models import Review

class ReviewForm(forms.ModelForm):
    RATING_CHOICES = (
        (1, '1 - Poor'),
        (2, '2 - Fair'),
        (3, '3 - Good'),
        (4, '4 - Very Good'),
        (5, '5 - Excellent'),
    )

    rating = forms.ChoiceField(
        choices=RATING_CHOICES,
        widget=forms.Select(attrs={
            'class': 'border p-2 rounded w-full focus:outline-none focus:ring-2 focus:ring-blue-500'
        })
    )
    comment = forms.CharField(
        required=False,
        widget=forms.Textarea(attrs={
            'class': 'border p-2 rounded w-full focus:outline-none focus:ring-2 focus:ring-blue-500',
            'rows': 4,
            'placeholder': 'আপনার মন্তব্য লিখুন (ঐচ্ছিক)'
        })
    )

    class Meta:
        model = Review
        fields = ['comment', 'rating']
        labels = {
            'comment': 'মন্তব্য',
            'rating': 'রেটিং',
        }
        help_texts = {
            'rating': '1 থেকে 5 এর মধ্যে একটি রেটিং বাছাই করুন।',
            'comment': 'আপনার অভিজ্ঞতা বা মতামত শেয়ার করুন।'
        }

    def __init__(self, *args, **kwargs):
        self.user = kwargs.pop('user', None)
        self.product = kwargs.pop('product', None)
        super().__init__(*args, **kwargs)

    def clean(self):
        cleaned_data = super().clean()
        if self.user and self.product:
            if Review.objects.filter(user=self.user, product=self.product).exists():
                raise forms.ValidationError("আপনি ইতিমধ্যে এই প্রোডাক্টে একটি রিভিউ দিয়েছেন।")
        return cleaned_data

class CartItemUpdateForm(forms.Form):
    item_id = forms.IntegerField(widget=forms.HiddenInput())
    quantity = forms.IntegerField(min_value=0, widget=forms.NumberInput(attrs={
        'class': 'border p-2 rounded w-16 focus:outline-none focus:ring-2 focus:ring-blue-500'
    }))