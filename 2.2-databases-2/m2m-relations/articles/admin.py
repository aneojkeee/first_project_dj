from django.contrib import admin
from django.core.exceptions import ValidationError
from django.forms import BaseInlineFormSet
from .models import Article, Theme, ArticleTheme


class ArticleThemeInlineFormset(BaseInlineFormSet):
    def clean(self):
        if len(self.forms) == 0:
            raise ValidationError('Не определены рубрики')

        count_main = 0
        for form in self.forms:
            if form.cleaned_data['is_main']:
                count_main += 1
            if count_main > 1:
                raise ValidationError('Главная рубрика отмечена более одного раза!')
        return super().clean()

class ArticleThemeInline(admin.TabularInline):
    model = ArticleTheme
    formset = ArticleThemeInlineFormset


@admin.register(Article)
class ArticleAdmin(admin.ModelAdmin):
    inlines = [ArticleThemeInline]


@admin.register(Theme)
class ThemeAdmin(admin.ModelAdmin):
    pass