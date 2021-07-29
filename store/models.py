from django.conf import settings
from django.db import models

# Create your models here.
from django.db.models import ForeignKey
from django.urls import reverse
from django.utils.translation import gettext_lazy as _
from mptt.fields import TreeForeignKey
from mptt.models import MPTTModel


class Category(MPTTModel):
    name = models.CharField(
        max_length=255,
        unique=True,
        verbose_name=_('Category name'),
        help_text=_('Required and unique')
    )
    slug = models.SlugField(max_length=255, verbose_name=_('Category Url name'), unique=True)
    parent = TreeForeignKey('self', on_delete=models.CASCADE, related_name='children', null=True, blank=True)
    is_active = models.BooleanField(default=True)
    class MPPTMeta:
        order_insertion_by = ['name']

    class Meta:
        verbose_name = _('Category')
        verbose_name_plural = _('Categories')

    def __str__(self):
        return self.name

    def get_absolute_url(self):
        return reverse('store:category_list', args=[self.slug])


class ProductType(models.Model):
    name = models.CharField(verbose_name=_('Product Name'), max_length=255, unique=True, )
    is_active = models.BooleanField(default=True)

    class Meta:
        verbose_name = _('Product Type')
        verbose_name_plural = _('Product Types')

    def __str__(self):
        return self.name


class ProductSpecification(models.Model):
    name = models.CharField(
        verbose_name=_('Name')
        , help_text=_('Required'),
        max_length=255)
    product_type = ForeignKey(ProductType, on_delete=models.RESTRICT)

    class Meta:
        verbose_name = _('Product Specification')
        verbose_name_plural = _('Product Specifications')

    def __str__(self):
        return self.name


# class ProductManager(models.Manager):
#     def get_queryset(self):
#         return super(ProductManager, self).get_queryset().filter(is_active=True)


class Product(models.Model):
    title = models.CharField(max_length=255, help_text=_('Required'), verbose_name=_('title'))
    category = models.ForeignKey(Category, on_delete=models.RESTRICT)
    description = models.TextField(help_text=_('Not Required'), verbose_name=_('Description'), blank=True)
    slug = models.SlugField(max_length=255)
    price = models.DecimalField(max_digits=5, decimal_places=2, help_text=_('max 999.99'),
                                error_messages={'name': {'max_length': _('The price must be max 999.99')}})
    discount_price = models.DecimalField(max_digits=5, decimal_places=2, help_text=_('max 999.99'),
                                         error_messages={'name': {'max_length': _('The price must be max 999.99')}})
    created_at = models.DateTimeField(_('Created at'), auto_now=True, editable=False)
    updated_at = models.DateTimeField(_('Updated at'), auto_now=True, )
    user_wishlist=models.ManyToManyField(settings.AUTH_USER_MODEL,blank=True,related_name='user_wishlist')

    class Meta:
        verbose_name_plural = _('Products')
        verbose_name = _('Product')
        ordering = ('-created_at',)

    def get_absolute_url(self):
        return reverse('store:product_detail', args=[self.slug])

    def __str__(self):
        return self.title


class ProductSpecificationValue(models.Model):
    product = models.ForeignKey(Product, on_delete=models.CASCADE)
    specification = models.ForeignKey(ProductSpecification, on_delete=models.RESTRICT)
    value = models.CharField(max_length=255, help_text=_('Max length is 255'), verbose_name=_('Value'))


class ProductImage(models.Model):
    product = models.ForeignKey(Product, on_delete=models.CASCADE)
    image = models.ImageField(
        verbose_name=_('Image'),
        default='images/default.png',
        upload_to='images/',
        help_text=_('Upload an image')
    )
    alt_text = models.TextField(verbose_name=_('Alternative text'),
                                help_text=_('Please add alternative text'),
                                blank=True,
                                null=True
                                )
    created_at = models.DateTimeField(auto_now=True, editable=False)
    updated_at = models.DateTimeField(auto_now=True, )
    is_feature = models.BooleanField(default=False)

    class Meta:
        verbose_name_plural = _('Product Images')
        verbose_name = _('Product Image')
