from django.conf.urls import url
from django.utils.safestring import mark_safe
from django.urls import reverse
from django import forms
from django.shortcuts import render, HttpResponse, redirect
from django.db.models.fields.related import ManyToManyField, ForeignKey, OneToOneField
from stark.utils import page
from django.db.models import Q
import copy


class DisplayList:

    def __init__(self, config_obj, request):
        self.config_obj = config_obj
        self.request = request
        self.start = 0
        self.end = 10

    def display_header(self):
        head_list = []
        for field_or_func in self.config_obj.get_new_display_list():
            if callable(field_or_func):
                head_list.append("操作")
            else:
                try:
                    head_list.append(self.config_obj.model._meta.get_field(field_or_func).verbose_name)
                except Exception as e:
                    # "__str__"的情况下取model的class名称的大写
                    head_list.append(self.config_obj.model._meta.model_name.upper())
        return head_list

    def display_page(self):
        # page_num, all_data_amount, request, per_page_data = 10, page_show_tags = 11
        page_num = self.request.GET.get("page", 1)
        all_data_amount = self.config_obj.model.objects.filter(self.config_obj.search_q).filter(
            self.config_obj.filter_q).distinct().count()

        mypage = page.MyPage(page_num, all_data_amount, self.request, per_page_data=self.config_obj.per_page_data,
                             page_show_tags=self.config_obj.page_show_tags)

        self.start = mypage.start
        self.end = mypage.end
        page_tag_html = mypage.ret_html

        return page_tag_html

    def display_body(self):
        data_list = []

        for obj in self.config_obj.model.objects.filter(self.config_obj.search_q).filter(
                self.config_obj.filter_q).distinct()[self.start:self.end]:
            temp = []
            for field_or_func in self.config_obj.get_new_display_list():
                val = ""
                if callable(field_or_func):
                    val = field_or_func(self.config_obj, obj)
                else:
                    try:
                        # 通过对象的_mete取判断每个字段的对象 class
                        field_obj = obj._meta.get_field(field_or_func)
                        if isinstance(field_obj, ManyToManyField):
                            val = " | ".join(
                                [str(temp_data_obj) for temp_data_obj in getattr(obj, field_or_func).all()])
                        else:
                            # 通过反射获取对象的值
                            val = getattr(obj, field_or_func)
                            if field_or_func in self.config_obj.display_list_links:
                                val = mark_safe(
                                    "<a href='{}'>{}</a>".format(self.config_obj.get_change_url(obj.pk), val))
                    except Exception as e:
                        # "__str__"的情况
                        val = getattr(obj, field_or_func)
                temp.append(val)
            data_list.append(temp)
        return data_list


class ModelStark:
    display_list = ['__str__']
    display_list_links = []
    search_fields = []
    model_form_class = ""
    actions = []
    filter_list = []

    def __init__(self, model):
        self.model = model
        self.per_page_data = 5  # 控制分页每页显示的数量
        self.page_show_tags = 11  # 显示多少页码标签
        # print(dir(self.model._meta))
        # for i in dir(self.model._meta):
        #     print(i," === ",getattr(self.model._meta,i))
        self.model_name = self.model._meta.model_name
        self.app_label = self.model._meta.app_label
        self.search_q = ""
        self.filter_q = ""

    def patch_delete(self, request, queryset):
        queryset.delete()

    patch_delete.desc = "数据清除"

    def get_new_actions(self):
        temp = []
        temp.extend(self.actions)
        temp.append(self.patch_delete)

        new_actions = []
        for func in temp:
            new_actions.append({
                "text": func.desc,
                "name": func.__name__
            })
        return new_actions

    def get_list_url(self):
        url = '%s_%s_list' % (self.app_label, self.model_name)
        _url = reverse(url)
        return _url

    def get_add_url(self):
        url = '%s_%s_add' % (self.app_label, self.model_name)
        _url = reverse(url)
        return _url

    def get_change_url(self, id):
        url = '%s_%s_change' % (self.app_label, self.model_name)
        _url = reverse(url, args=(id,))
        return _url

    def get_change_or_delete_ret_list_url(self, id):
        total_page_num, more = divmod(self.model.objects.filter(id__lte=id).count(), self.per_page_data)
        if more:
            total_page_num += 1

        url = '%s_%s_list' % (self.app_label, self.model_name)
        _url = reverse(url) + "?page=" + str(total_page_num)

        return _url

    def get_delete_url(self, id):
        url = '%s_%s_delete' % (self.app_label, self.model_name)
        _url = reverse(url, args=(id,))
        return _url

    def get_last_page_url(self):
        total_page_num, more = divmod(self.model.objects.count(), self.per_page_data)
        if more:
            total_page_num += 1

        url = '%s_%s_list' % (self.app_label, self.model_name)
        _url = reverse(url) + "?page=" + str(total_page_num)

        return _url

    def add_data(self, obj=None, is_header=False):
        return "操作" if is_header else mark_safe("<a href='%s'>添加</a>" % self.get_add_url())

    def delete_data(self, obj=None, is_header=False):
        return "操作" if is_header else mark_safe("<a href='%s'>删除</a>" % self.get_delete_url(obj.pk))

    def edit_data(self, obj=None, is_header=False):
        return "操作" if is_header else mark_safe("<a href='%s'>编辑</a>" % self.get_change_url(obj.pk))

    def check_box(self, obj=None, is_header=False):
        return "选择" if is_header else mark_safe("<input name='pk' type='checkbox' value='%s'>" % obj.pk)

    def get_new_display_list(self):
        temp = []
        temp.insert(0, ModelStark.check_box)
        temp.extend(self.display_list)
        temp.extend([ModelStark.delete_data, ModelStark.edit_data])
        if self.display_list_links:
            temp.remove(ModelStark.edit_data)
        return temp

    def get_filter_data_list(self):
        filter_data_list = []
        data = ''

        if len(self.filter_list):
            for field in self.filter_list:
                field_obj = self.model._meta.get_field(field)
                if isinstance(field_obj, ForeignKey) or isinstance(field_obj, ManyToManyField) \
                        or isinstance(field_obj, OneToOneField):
                    data = field_obj.related_model.objects.all()
                else:
                    data = self.model.objects.all().values_list(field)
                filter_data_list.append({field: data})

        return filter_data_list

    def get_filter_data_html(self, request):
        filter_data_html_dic = {}
        filter_data_list = self.get_filter_data_list()

        params = copy.deepcopy(request.GET)
        # params[k.name] = item[0]
        # params.urlencode()

        no_exist_fields = []

        for data_dict in filter_data_list:
            for k, v in data_dict.items():

                k = self.model._meta.get_field(k)

                for no_exist_field in no_exist_fields:
                    params.pop(no_exist_field, "")

                if isinstance(k, ForeignKey) or isinstance(k, OneToOneField):
                    if k.name + "_id" not in params:
                        no_exist_fields.append(k.name + "_id")
                elif type(v[0]) == tuple or isinstance(k, ManyToManyField):
                    if k.name not in params:
                        no_exist_fields.append(k.name)

                a_label_html_list = [
                    mark_safe("<p style='margin:0px;'><a href='?{}'>All</a></p>".format(params.urlencode()))]

                for item in v:
                    a_label_html = ""
                    # 第一次进来，没有的字段会被添加
                    if type(item) == tuple:
                        params[k.name] = item[0]
                        a_label_html = mark_safe("<a href='?{0}'>{1}</a>".format(params.urlencode(), item[0]))
                    elif isinstance(k, ForeignKey) or isinstance(k, OneToOneField):
                        params[k.name + "_id"] = item.id
                        a_label_html = mark_safe("<a href='?{0}'>{1}</a>".format(params.urlencode(), item))
                    elif isinstance(k, ManyToManyField):
                        params[k.name] = item.id
                        a_label_html = mark_safe("<a href='?{0}'>{1}</a>".format(params.urlencode(), item))

                    a_label_html_list.append(a_label_html)

                filter_data_html_dic[k.verbose_name] = a_label_html_list

        return filter_data_html_dic

    def get_search_kvp(self, search_value, kvp_dic):

        self.search_q = Q()
        self.search_q.connector = "OR"

        self.filter_q = Q()

        if search_value:
            for search_field in self.search_fields:
                self.search_q.children.append((search_field + "__icontains", search_value))

        if len(kvp_dic):
            for k, v in kvp_dic.items():
                self.filter_q.children.append((k, v))

    def get_kvp_dic(self, request):

        params = copy.deepcopy(request.GET)
        print("params ============>", params)

        kvp_dic = {}

        for param in params:
            print(param)
            value = request.GET.get(param)
            kvp_dic[param] = value

        return kvp_dic

    def list_view(self, request):

        # 数据过滤
        if request.method == 'GET':
            kvp_dic = self.get_kvp_dic(request)
            search_value = request.GET.get("search_value", "")

            kvp_dic.pop("search_value", "")
            kvp_dic.pop("page", "")

            self.get_search_kvp(search_value, kvp_dic)
        elif request.method == 'POST':  # 自定义批量操作方法 和 默认批量操作方法
            action_func = request.POST.get("path_operate")
            pk_list = request.POST.getlist("pk")
            try:
                action_func = getattr(self, action_func)
                queryset = self.model.objects.filter(pk__in=pk_list)
                action_func(request, queryset)
            except Exception as e:
                pass  # ------------

        display_list = DisplayList(self, request)
        page_tag_html = display_list.display_page()
        head_list = display_list.display_header()
        data_list = display_list.display_body()
        new_actions = self.get_new_actions()

        add_link_tag = ModelStark.add_data(self)
        filter_data_html_dic = self.get_filter_data_html(request)

        return render(request, "list_view.html",
                      {"add_link_tag": add_link_tag,
                       "page_tag_html": page_tag_html,
                       "head_list": head_list,
                       "data_list": data_list,
                       "filter_data_html_dic": filter_data_html_dic,
                       "actions": new_actions,
                       "search": self.search_fields})

    def get_model_form_class(self, ):
        """获取modelform"""
        if self.model_form_class:
            return self.model_form_class
        else:
            # from django.forms import widgets as wdg
            class ModelFormClass(forms.ModelForm):
                class Meta:
                    model = self.model
                    fields = "__all__"

            return ModelFormClass

    def add_view(self, request):
        ModelFormClass = self.get_model_form_class()

        if request.method == 'GET':
            model_from = ModelFormClass()
        elif request.method == 'POST':
            model_from = ModelFormClass(request.POST)
            if model_from.is_valid():
                model_from.save()
                return redirect(self.get_last_page_url())
        return render(request, 'add_view.html', {"from": model_from, "index_url": self.get_list_url()})

    def change_view(self, request, id):
        ModelFormClass = self.get_model_form_class()
        obj = self.model.objects.filter(id=id).first()

        if request.method == 'GET':
            model_from = ModelFormClass(instance=obj)
        elif request.method == 'POST':
            model_from = ModelFormClass(request.POST, instance=obj)
            if model_from.is_valid():
                model_from.save()
                return redirect(self.get_change_or_delete_ret_list_url(id))

        return render(request, 'change_view.html',
                      {"from": model_from, "index_url": self.get_change_or_delete_ret_list_url(id)})


    def delete_view(self, request, id):
        ModelFormClass = self.get_model_form_class()
        obj = self.model.objects.filter(id=id).first()

        if request.method == 'GET':
            model_from = ModelFormClass(instance=obj)
            return render(request, 'delete_view.html',
                          {"from": model_from, "index_url": self.get_change_or_delete_ret_list_url(id)})
        elif request.method == 'POST':
            self.model.objects.filter(pk=id).delete()
            return redirect(self.get_change_or_delete_ret_list_url(id))

    def get_urls(self):
        temp = []
        temp.append(url(r'^$', self.list_view, name='%s_%s_list' % (self.app_label, self.model_name)))
        temp.append(url(r'^add/$', self.add_view, name='%s_%s_add' % (self.app_label, self.model_name)))
        temp.append(url(r'^(\d+)/change/$', self.change_view, name='%s_%s_change' % (self.app_label, self.model_name)))
        temp.append(url(r'^(\d+)/delete/$', self.delete_view, name='%s_%s_delete' % (self.app_label, self.model_name)))
        return temp

    @property
    def urls(self):
        return self.get_urls(), None, None


class AdminSite:

    def __init__(self):
        self._registry = {}

    def register(self, model, config_class=None):
        """
        注册一张数据表
        :param model:  model的表的class
        :param config_class:  自定义样式类
        :return:
        """
        if config_class is None:
            config_class = ModelStark
        self._registry[model] = config_class(model)

    def get_urls(self):
        temp = []
        for model, config_obj in self._registry.items():
            model_name = model._meta.model_name
            app_label = model._meta.app_label
            temp.append(url(r"^%s/%s/" % (app_label, model_name), config_obj.urls))
        return temp

    @property
    def urls(self):
        return self.get_urls(), None, None


site = AdminSite()
