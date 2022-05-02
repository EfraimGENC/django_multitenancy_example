import uuid
from django.db import models
from django.db.models import F
from django.utils.translation import gettext_lazy as _


class BaseModel(models.Model):
    uuid = models.UUIDField(
        _("UUID"),
        unique=True,
        default=uuid.uuid4,
        editable=False,
    )

    updated_date = models.DateTimeField(
        _("Update Date"),
        auto_now=True,
        editable=False
    )

    created_date = models.DateTimeField(
        _("Create Date"),
        auto_now_add=True,
        editable=False
    )

    # Managers
    objects = models.Manager()

    class Meta:
        abstract = True
        ordering = (F('created_date').desc(), F('id').desc())
        get_latest_by = (F('created_date').desc(), F('id').desc())

    @classmethod
    def get_ordering_options(cls):
        return [
                   ('latest', _('Latest'), (F('created_date').desc(), F('id').desc())),
                   ('earliest', _('Earliest'), (F('created_date').asc(), F('id').asc())),
               ] + getattr(cls, 'ORDERING_OPTIONS', [])

    @classmethod
    def get_ordering_queries(cls):
        queries = {}
        for choice in cls.get_ordering_options():
            queries[choice[0]] = choice[2]
        return queries

    @classmethod
    def get_ordering_choices(cls):
        choices = []
        for choice in cls.get_ordering_options():
            choices.append((choice[0], choice[1]))
        return choices
