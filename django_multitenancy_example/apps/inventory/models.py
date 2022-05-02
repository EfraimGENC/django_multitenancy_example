from django.db import models
from django.utils.translation import gettext_lazy as _
from django_multitenancy_example.core.models import BaseModel


class Location(BaseModel):
    name = models.CharField(_('name'), max_length=255)

    class Meta(BaseModel.Meta):
        verbose_name = _('location')
        verbose_name_plural = _('locations')

    def __str__(self):
        return self.name


class Category(BaseModel):
    name = models.CharField(_('name'), max_length=255)

    class Meta(BaseModel.Meta):
        verbose_name = _('category')
        verbose_name_plural = _('categories')

    def __str__(self):
        return self.name


class Tag(BaseModel):
    name = models.CharField(_('name'), max_length=255)

    class Meta(BaseModel.Meta):
        verbose_name = _('tag')
        verbose_name_plural = _('tags')

    def __str__(self):
        return self.name


class Brand(BaseModel):
    name = models.CharField(_('name'), max_length=255)

    class Meta(BaseModel.Meta):
        verbose_name = _('brand')
        verbose_name_plural = _('brands')

    def __str__(self):
        return self.name


class Model(BaseModel):
    brand = models.ForeignKey(
        'inventory.Brand',
        on_delete=models.CASCADE,
        related_name='models',
        verbose_name=_('brand')
    )

    name = models.CharField(_('name'), max_length=255)

    class Meta(BaseModel.Meta):
        verbose_name = _('model')
        verbose_name_plural = _('models')

    def __str__(self):
        return self.name


class Document(BaseModel):
    inventory = models.ForeignKey(
        'inventory.Inventory',
        on_delete=models.CASCADE,
        related_name='documents',
        verbose_name=_('inventory'),
    )

    title = models.CharField(_('title'), max_length=255)
    # file = models.FileField(_('file'), upload_to='documents')

    class Meta(BaseModel.Meta):
        verbose_name = _('document')
        verbose_name_plural = _('documents')

    def __str__(self):
        return self.title


class Image(BaseModel):
    inventory = models.ForeignKey(
        'inventory.Inventory',
        on_delete=models.CASCADE,
        related_name='images',
        verbose_name=_('inventory')
    )

    title = models.CharField(_('title'), max_length=255)
    # image =

    class Meta(BaseModel.Meta):
        verbose_name = _('image')
        verbose_name_plural = _('images')

    def __str__(self):
        return self.title


class Inventory(BaseModel):
    location = models.ForeignKey(
        'inventory.Location',
        on_delete=models.PROTECT,
        related_name='inventories',
        verbose_name=_('location'),
    )

    name = models.CharField(
        _('name'),
        max_length=255
    )

    description = models.TextField(
        _('description'),
        null=True,
        blank=True
    )

    amount = models.DecimalField(
        _('amount'),
        max_digits=10,
        decimal_places=2,
        null=True,
        blank=True
    )

    quantity = models.IntegerField(_('quantity'))

    category = models.ForeignKey(
        'inventory.Category',
        on_delete=models.SET_NULL,
        related_name='inventories',
        verbose_name=_('category'),
        null=True,
        blank=True
    )

    tag = models.ForeignKey(
        'inventory.Tag',
        on_delete=models.SET_NULL,
        related_name='inventories',
        verbose_name=_('label'),
        null=True,
        blank=True
    )

    brand = models.ForeignKey(
        'inventory.Brand',
        on_delete=models.SET_NULL,
        related_name='inventories',
        verbose_name=_('brand'),
        null=True,
        blank=True
    )

    model = models.ForeignKey(
        'inventory.Model',
        on_delete=models.SET_NULL,
        related_name='inventories',
        verbose_name=_('model'),
        null=True,
        blank=True
    )

    serial = models.CharField(
        _('serial number'),
        max_length=255,
        null=True,
        blank=True
    )

    acquisitioned_at = models.DateField(
        _('date of acquisition'),
        null=True,
        blank=True
    )

    warranty_start = models.DateField(
        _('warranty start'),
        null=True,
        blank=True
    )

    warranty_end = models.DateField(
        _('warranty finnish'),
        null=True,
        blank=True
    )

    class Meta(BaseModel.Meta):
        verbose_name = _('inventory')
        verbose_name_plural = _('inventories')

    def __str__(self):
        return f"{self.name} [{self.location}]"
