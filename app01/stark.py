from django import forms
from django.forms import widgets
from django.db.models.fields.related import ForeignKey,ManyToManyField
from stark.service.sites import site
from stark.service import sites
from app01 import models


class AuthorModelForm(forms.ModelForm):
    class Meta:
        val = {"required": "该字段不能为空"}
        model = models.Author
        fields = "__all__"
        widgets = {
            'name': widgets.TextInput(attrs={'class': 'form-control', 'autocomplete': 'off'}),
            'stage_name': widgets.TextInput(attrs={'class': 'form-control', 'autocomplete': 'off'}),
            'address': widgets.TextInput(attrs={'class': 'form-control', 'autocomplete': 'off'}),
            'phone': widgets.TextInput(attrs={'class': 'form-control', 'autocomplete': 'off'}),
            'gender': widgets.TextInput(attrs={'class': 'form-control', 'autocomplete': 'off'}),
        }


class AuthorAdmin(sites.ModelStark):
    model_form_class = AuthorModelForm
    display_list = ['name', 'gender', 'phone']


site.register(models.Author, AuthorAdmin)


class BookModelForm(forms.ModelForm):
    class Meta:
        model = models.Book
        fields = "__all__"
        widgets = {
            'name': widgets.TextInput(attrs={'class': 'form-control', 'autocomplete': 'off'}),
            # 'autor':widgets.SelectMultiple(attrs={'class': 'form-control', 'autocomplete': 'off'}),
            # 'autor':widgets.CheckboxSelectMultiple(attrs={'class': 'form-control', 'autocomplete': 'off'}),
            # 'autor':widgets.ChoiceWidget(attrs={'class': 'form-control', 'autocomplete': 'off'}),
            'author':widgets.SelectMultiple(attrs={'class': 'form-control', 'autocomplete': 'off'}),
            'publish':widgets.Select(attrs={'class': 'form-control', 'autocomplete': 'off'}),
        }
        val = {"required": "该字段不能为空"}
        error_messages = {
            "name": val,
            "author": val,
            "publish": val,
        }


class BookAdmin(sites.ModelStark):
    model_form_class = BookModelForm
    display_list = ['name', 'author', 'publish']
    display_list_links = ["name","author","publish"]
    search_fields = ["name","author__name","publish__name"]  # bug author id
    filter_list = ["name","author",'publish']

    def init_publish(self,request,queryset):
        queryset.update(publish_id = 1)

    init_publish.desc = "出版社初始化"

    actions = [init_publish]


site.register(models.Book, BookAdmin)


class PublishModelForm(forms.ModelForm):
    class Meta:
        val = {"required": "该字段不能为空"}
        model = models.Publish
        fields = "__all__"
        widgets = {
            'name': widgets.TextInput(attrs={'class': 'form-control', 'autocomplete': 'off'}),
            'address': widgets.TextInput(attrs={'class': 'form-control', 'autocomplete': 'off'}),
            'phone': widgets.TextInput(attrs={'class': 'form-control', 'autocomplete': 'off'}),
            'record_date': widgets.TextInput(attrs={'class': 'form-control', 'autocomplete': 'off'}),
        }


class PublishAdmin(sites.ModelStark):
    model_form_class = PublishModelForm
    display_list = ['name', 'address', 'record_date']

    def init_date(self,request,queryset):
        queryset.update(record_date = '201808-31')

    init_date.desc = "日期初始化"

    actions = [init_date]


site.register(models.Publish, PublishAdmin)
