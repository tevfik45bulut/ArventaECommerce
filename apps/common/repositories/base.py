from django.db import models


class BaseRepository:

    model: models.Model = None

    @classmethod
    def all(cls):
        return cls.model.objects.all()

    @classmethod
    def active(cls):
        return cls.model.objects.filter(is_active=True)

    @classmethod
    def get(cls, **kwargs):
        return cls.model.objects.get(**kwargs)

    @classmethod
    def filter(cls, **kwargs):
        return cls.model.objects.filter(**kwargs)

    @classmethod
    def create(cls, **kwargs):
        return cls.model.objects.create(**kwargs)

    @classmethod
    def update(cls, instance, **kwargs):
        for key, value in kwargs.items():
            setattr(instance, key, value)

        instance.save()

        return instance

    @classmethod
    def delete(cls, instance):
        instance.delete()