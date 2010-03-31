from apps.core.models import Topic
from django.forms import ModelForm, Textarea


class ArticleForm(ModelForm):
    class Meta:
        model   = Topic
        fields  = ('name', 'description', 'content')
        widgets = {
                    'description': Textarea(attrs={'cols': 55, 'rows': 5}),
                    'content': Textarea(attrs={'cols': 55, 'rows': 20})
        }