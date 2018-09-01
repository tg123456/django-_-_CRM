
from django.db import models
import django
# print(django.__version__)

class Person(models.Model):
    name = models.CharField(max_length=32,verbose_name="姓名")
    display_name = models.CharField(max_length=32)
    phone = models.CharField(max_length=32)
    email = models.EmailField()
    password = models.CharField(max_length=32)

    def __str__(self):
        return self.name

class Publish(models.Model):
    name = models.CharField(max_length=50,null=False,verbose_name='名称')
    address = models.CharField(max_length=255,verbose_name='地址')
    phone = models.CharField(max_length=20,verbose_name='电话')
    record_date = models.CharField(max_length=20,verbose_name='日期')

    def __str__(self):
        return self.name

    class Meta:
        verbose_name = '出版社'
        verbose_name_plural = verbose_name

class Author(models.Model):
    name = models.CharField(max_length=50,null=False,verbose_name="姓名")
    stage_name = models.CharField(max_length=50,verbose_name='别名')
    address = models.CharField(max_length=255,verbose_name='地址')
    phone = models.CharField(max_length=20,verbose_name='电话')
    gender = models.CharField(max_length=2,default="男",verbose_name='性别')

    def __str__(self):
        return self.name

class Book(models.Model):
    name = models.CharField(max_length=32,null=False,unique=True,verbose_name="书名")
    author = models.ManyToManyField(Author,verbose_name="作者")
    publish = models.ForeignKey(to="Publish",on_delete=models.SET_DEFAULT,default=9999,verbose_name='出版社')

    def __str__(self):
        return self.name

    class Meta:
        verbose_name = "书籍"
        verbose_name_plural = verbose_name





