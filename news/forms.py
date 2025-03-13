from django import forms

from .models import Article, Category, Tag


class ArticleForm(forms.ModelForm):

    tags = forms.ModelMultipleChoiceField(
        queryset=Tag.objects.all(),
        widget=forms.CheckboxSelectMultiple,
        required=False
    )

    class Meta:
        model = Article
        fields = ['title', 'content', 'category', 'tags', 'image']
        widgets = {
            'content': forms.Textarea(attrs={'rows': 5, 'cols': 40}),
            'publication_date': forms.DateInput(attrs={'type': 'date'}),
            'image': forms.ClearableFileInput(attrs={'class': 'form-control-file'})
        }
        label = {
            'category': 'Категория',
            'tags': 'Теги'
        }


class ArticleUploadForm(forms.Form):
    json_file = forms.FileField()

    def clean_json_file(self):
        json_file = self.cleaned_data.get('json_file')
        if not json_file.name.endswith('.json'):
            raise forms.ValidationError('Файл должен быть в формате JSON.')
        return json_file

    def validate_json_data(self, data):
        errors = []
        existing_categories = Category.objects.values_list('name', flat=True)
        existing_tags = Tag.objects.values_list('name', flat=True)
        for item in data:
            fields = item['fields']
            title = fields['title']
            content = fields['content']
            category_name = fields['category']
            tags_names = fields['tags']
            if category_name not in existing_categories:
                errors.append(f"В новости '{title}' несуществующая категория '{category_name}'. Впишите одну из этих категорий в файл: {', '.join(existing_categories)}")
            for tag_name in tags_names:
                if tag_name not in existing_tags:
                    errors.append(f"В новости '{title}' несуществующий тег '{tag_name}'. Впишите один из этих тегов в файл: {', '.join(existing_tags)}")
        return errors