import os

os.environ.setdefault("DJANGO_SETTINGS_MODULE", "custom_crm.settings")


if __name__ == '__main__':
    import django
    django.setup()

    from app01 import models

    from django.db.models import Q

    # print(models.Book._meta)
    # print(dir(models.Book._meta))
    # for i in dir(models.Book._meta):
    #     print(i," ===> ",getattr(models.Book._meta,i))

    # print(models.Publish._meta)
    # print(dir(models.Publish._meta))
    # for i in dir(models.Publish._meta):
    #     print(i, " ===> ", getattr(models.Publish._meta, i))
    #
    # print(models.Publish._meta.__str__)
    # print(dir(models.Publish._meta.__str__))


    data = models.Book.objects.all().first()
    print("data == ",dir(data))

    # for i in dir(data):
    #     print(i," ===> ",getattr(data,i))


    # val = getattr(data, 'publish')
    # print(val)
    # print(data)

    # print(type(Q))
    # print(dir(Q()))

    # for obj in models.Author.objects.all():
    #     print(obj)
    #     print(type(obj))
    #     print(dir(obj._meta))


    # def create_data():
    #     book_obj_list = [models.Book(name='test{}'.format(i),publish_id=1) for i in range(100)]
    #     models.Book.objects.bulk_create(book_obj_list)
    #
    # create_data()






























