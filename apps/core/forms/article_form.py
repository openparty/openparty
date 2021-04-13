from apps.core.models import Topic
from django.forms import ModelForm, Textarea


class ArticleForm(ModelForm):
    class Meta:
        model = Topic
        fields = ("name", "description", "content", "in_event")
        widgets = {
            "description": Textarea(attrs={"cols": 60, "rows": 5}),
            "content": Textarea(
                attrs={"cols": 60, "rows": 20, "class": "with_tinymce"}
            ),
        }
