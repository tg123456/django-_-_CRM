import os

if __name__ == '__main__':
    os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'day68_orm.settings')
    import django
    django.setup()
    from app01 import models

# 查找所有书名里包含金老板的书
#     ret = models.Book.objects.filter(author__name='alex')
#     print(ret)

# 查找“沙河出版社”出版的所有书籍
# ret = models.Book.objects.filter(publisher__address='北京')
# print(ret)
#
# ret = models.Book.objects.filter(author__name='alex')
# print(ret)
# ret = models.Book.objects.get(id=4)
# data = ret.author_set.all()
# print(data)


# 查找每个出版社的书名以及出的书籍数量
# ret = models.Book.objects.all().order_by('publisher__id').values()
# for i in ret:
#     count = models.Book.objects.filter()
#     print(i['title'],i['publisher_id'])


# 查找每个作者写的价格最高的书籍价格
# ret = models.Author.objects.annotate(max_price = Max('books__price')).values()
# for i in ret:
#     print(i)

# ret = models.Publisher.objects.annotate(Count('book')).values()
# for i in ret:
#     print(i)

# 查找每个作者的姓名以及出的书籍数量
# ret = models.Author.objects.annotate(count = Count('books')).values('name','count')
# for i in ret:
#     print(i)

# 查找书名是“跟金老板学开车”的书的出版社
# ret = models.Publisher.objects.filter(book__title='僻邪剑谱').values()
# for i in ret:
#     print(i)

# 查找书名是“跟金老板学开车”的书的出版社所在的城市
# ret = models.Publisher.objects.filter(book__title='僻邪剑谱').values('address','book__title')
# print(ret)

# 查找书名是“跟金老板学开车”的书的出版社的名称
# ret = models.Publisher.objects.filter(book__title='僻邪剑谱').values('name','book__title')
# print(ret)

from django.db.models import F,Q
# # 查找书名是“跟金老板学开车”的书的出版社出版的其他书籍的名字和价格
# ret = models.Book.objects.filter(publisher__book__title='僻邪剑谱').exclude(title='僻邪剑谱').values('title','price')
# for i in ret:
#     print(i)

# 查找书名是“跟金老板学开车”的书的所有作者
# ret = models.Author.objects.filter(books__title='僻邪剑谱').values()
# print(ret)

# ret = models.Book.objects.filter(author__name='alex').values()
# print(ret)

# 查找书名是“跟金老板学开车”的书的作者的年龄
# book = models.Book.objects.get(title='葵花宝典(第一版)')
# ret = book.author_set.all().values('name','age')
# print(ret)

# 查找书名是“跟金老板学开车”的书的作者的手机号码
# ret = models.Book.objects.get(title='葵花宝典(第一版)').author_set.all().values('name','phone')
# print(ret)

# 查找书名是“跟金老板学开车”的书的作者们的姓名以及出版的所有书籍名称和价钱
# authors = models.Author.objects.filter(books__title='僻邪剑谱').values()
# for author in authors:
#     # print(author['id'])
#     ret = models.Book.objects.filter(author__id=author['id']).values('title','price')
#     for item in ret:
#         print(author['name'],item)

# ret = models.Book.objects.filter(
#     author__books=models.Book.objects.filter(title='南方')).values('title')
# for item in ret:
#     print(item)
# print("=======================")
# ret = models.Book.objects.filter(author__name='alex')
# ret =models.Book.objects.filter(title='南方').values()
# ret =  models.Author.objects.filter(books__title='南方')
# ret = models.Book.objects.filter(author__name='alex')
# for item in ret:
#     print(item)


from django.db.models import F,Q
# ret = models.Book.objects.filter(id='1')
# ret.price = F(ret.price) + 10
# ret.save()
# ret = models.Book.objects.get(id=1)
# print(ret.publisher)
# print(ret.publisher)

# ret = models.Book.objects.select_related().get(id=1)
# print(ret.publisher)
# print(ret.publisher)

# ret = models.Book.objects.filter(memo__isnull=True)
# print(ret)

# ret = models.Book.objects.values("title").annotate(Count("id")).order_by()
# print(ret)

# ret = models.Book.objects.annotate(num_authors=Count('authors')).aggregate(Avg('num_authors'))

# ret = models.Author.objects.annotate(num_authors=Count('books')).aggregate(Avg('num_authors'))
# print(ret)

ret = models.Publisher.objects.annotate(num_books=Count('book', distinct=True)).filter(book__price=33)
print(ret)

# a, b = models.Publisher.objects.filter(book__rating__gt=3.0).annotate(num_books=Count('book'))






