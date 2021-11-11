from django.contrib import admin
from django.core.exceptions import ValidationError
from django.forms import BaseInlineFormSet

from .models import Tag, Scope, Article


class ScopeInlineFormSet(BaseInlineFormSet):

    def clean(self):
        count = False
        for form in self.forms:
            if form.cleaned_data.get('is_main'):
                if count == True:
                    raise ValidationError('Основным может быть только один раздел')
                else:
                    count = True
        if count == False:
            raise ValidationError('Укажите основной раздел')
        return super().clean()


class ScopeInline(admin.TabularInline):
    model = Scope
    formset = ScopeInlineFormSet


@admin.register(Tag)
class TagAdmin(admin.ModelAdmin):
    list_display = ('id', 'name')
    list_display_links = ('id', 'name')


@admin.register(Article)
class ArticleAdmin(admin.ModelAdmin):
    list_display = ('id', 'title', 'published_at')
    list_display_links = ('id', 'title')
    inlines = (ScopeInline, )
