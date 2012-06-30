from django import forms

class ArticleForm(forms.Form):
    title = forms.CharField(max_length=120)
    content = forms.CharField()
    tags = forms.CharField()
    
    def clean_tags(self):
        tgs = self.cleaned_data['tags']
        try:
            tags = tgs.split(',')
        except:
            raise forms.ValidationError("Tags...error!")
        return tags