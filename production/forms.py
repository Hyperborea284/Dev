from django import forms

class ContactForm(forms.Form):
    full_name = forms.CharField()
    email = forms.EmailField()
    content = forms.CharField(widget=forms.Textarea)

    def cleaned_email(self, *args, **kwargs):
        tile = self.cleaned_data.get('title')
        if email.endswith(".edu"):
            raise forms.ValidationError("This is not a valid email. Please don't use .edu")

        qs = BlogPost.objects.filter(title__iexact=title)
        if qs.exists():
             forms.ValidationError("This title has already been used.")


        return title
