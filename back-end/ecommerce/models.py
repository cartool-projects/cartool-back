import re

from ckeditor.fields import RichTextField
from django.db import models
from django.utils.translation import gettext_lazy as _
from versatileimagefield.fields import VersatileImageField

from ecommerce.choices import ProductStatus, OrderStatus, PaymentMethod

from user.models import User


class Product(models.Model):
    name = models.CharField(_("სახელი"), max_length=255)
    description = RichTextField(_("აღწერა"))
    price = models.DecimalField(_("ფასი"), max_digits=10, decimal_places=2)
    created_at = models.DateTimeField(_("შექმნის თარიღი"), auto_now_add=True)
    category = models.ForeignKey("Category",
                                 verbose_name=_("კატეგორია"),
                                 related_name="products",
                                 on_delete=models.CASCADE,
                                 null=True, blank=True)
    in_stock = models.PositiveIntegerField(_("მარაგში დარჩენილი რაოდენობა"), default=0)
    status = models.IntegerField(_("სტატუსი"),
                                 choices=ProductStatus.choices,
                                 default=ProductStatus.AVAILABLE)
    discount = models.ForeignKey("Discount",
                                 verbose_name=_("ფასდაკლება"),
                                 related_name="products",
                                 on_delete=models.CASCADE,
                                 null=True, blank=True)
    free_delivery = models.BooleanField(_("უფასო მიწოდება"), default=False)
    slug = models.SlugField(_("სლაგი"), max_length=255, unique=True)
    views = models.PositiveIntegerField(_("ნახვები"), default=0)
    popular = models.BooleanField(_("პოპულარული"), default=False)

    class Meta:
        verbose_name = _("პროდუქტი")
        verbose_name_plural = _("პროდუქტები")

    def __str__(self):
        return f'{self.name}-{self.id}'

    def increase_views(self):
        self.views += 1
        self.save(update_fields=['views'])

    def save(self, *args, **kwargs):
        if not self.slug:
            slug = re.sub(r'[-\s]+', '-', self.name.lower())
            self.slug = slug[:255]
        super().save(*args, **kwargs)


class ProductImage(models.Model):
    product = models.ForeignKey(Product,
                                verbose_name=_("პროდუქტი"),
                                related_name="product_image",
                                on_delete=models.CASCADE)
    image = VersatileImageField(_("სურათი"),
                                upload_to="ecommerce/product_images/",
                                blank=True, null=True)
    color = models.CharField(_("ფერი"), max_length=255, blank=True, null=True)

    class Meta:
        verbose_name = _("პროდუქტის სურათი")
        verbose_name_plural = _("პროდუქტის სურათები")

    def __str__(self):
        return self.product.name


class Discount(models.Model):
    is_active = models.BooleanField(_("აქტიურია"), default=False)
    discount = models.DecimalField(_("ფასდაკლება"), max_digits=10, decimal_places=2)
    start_date = models.DateTimeField(_("დაწყების თარიღი"))
    end_date = models.DateTimeField(_("დასრულების თარიღი"))

    class Meta:
        verbose_name = _("ფასდაკლება")
        verbose_name_plural = _("ფასდაკლებები")

    def __str__(self):
        return f"{self.discount}%"


class Category(models.Model):
    name = models.CharField(_("სახელი"), max_length=255, db_index=True)
    slug = models.SlugField(_("სლაგი"), max_length=255,
                            unique=True, blank=True, null=True)
    parent = models.ForeignKey("self", on_delete=models.CASCADE,
                               verbose_name=_("მშობელი კატეგორია"),
                               related_name="children", blank=True, null=True)

    class Meta:
        verbose_name = _("კატეგორია")
        verbose_name_plural = _("კატეგორიები")

    def save(self, *args, **kwargs):
        if not self.slug:
            slug = re.sub(r'[-\s]+', '-', self.name.lower())
            self.slug = slug[:255]
        super().save(*args, **kwargs)

    def get_parents(self):
        parents = []
        parent = self.parent
        while parent:
            parents.append(parent)
            parent = parent.parent
        # for string representation, not category objects
        parents_names = [parent.slug for parent in parents]
        return parents_names[::-1]

    def get_path(self):
        parents = self.get_parents()
        parents.append(self.slug)
        return '/'.join(parents)

    def __str__(self):
        return self.name


class ProductSpecs(models.Model):
    product = models.ForeignKey(Product,
                                verbose_name=_("პროდუქტი"),
                                related_name="product_specs",
                                on_delete=models.CASCADE)
    spec_name = models.CharField(_("სპეციფიკაციის სახელი"), max_length=255)
    spec_value = models.CharField(_("სპეციფიკაციის მნიშვნელობა"), max_length=255)
    order = models.PositiveIntegerField(default=0, editable=False, db_index=True)

    class Meta:
        verbose_name = _("სპეციფიკაცია")
        verbose_name_plural = _("სპეციფიკაციები")

    def __str__(self):
        return f"{self.spec_name}: {self.spec_value}"


class Order(models.Model):
    customer = models.ForeignKey(User,
                                 verbose_name=_("მომხმარებელი"),
                                 related_name="orders",
                                 on_delete=models.CASCADE)
    product = models.ForeignKey(Product,
                                verbose_name=_("პროდუქტი"),
                                related_name="orders",
                                on_delete=models.CASCADE)
    quantity = models.PositiveIntegerField(_("რაოდენობა"))
    total_price = models.DecimalField(_("ჯამური ფასი"),
                                      max_digits=10, decimal_places=2)
    order_date = models.DateTimeField(_("შეკვეთის თარიღი"))
    status = models.IntegerField(_("სტატუსი"),
                                 choices=OrderStatus.choices,
                                 default=OrderStatus.PROCESSING)

    class Meta:
        verbose_name = _("შეკვეთა")
        verbose_name_plural = _("შეკვეთები")

    def __str__(self):
        return f"{self.customer.username} - {self.product.name} - {self.quantity} - {self.total_price} - {self.order_date} - {self.status}"


class Payment(models.Model):
    order = models.ForeignKey(Order,
                              verbose_name=_("შეკვეთა"),
                              related_name="payments",
                              on_delete=models.CASCADE)
    amount = models.DecimalField(_("თანხა"),
                                 max_digits=10, decimal_places=2)
    payment_method = models.IntegerField(_("გადახდის მეთოდი"),
                                         choices=PaymentMethod.choices,
                                         default=PaymentMethod.CREDIT_CARD)
    date = models.DateTimeField(_("თარიღი"))

    class Meta:
        verbose_name = _("გადახდა")
        verbose_name_plural = _("გადახდები")

    def __str__(self):
        return f"{self.order} - {self.amount} - {self.payment_method} - {self.date}"


class Cart(models.Model):
    customer = models.ForeignKey(User,
                                 verbose_name=_("მომხმარებელი"),
                                 related_name="carts",
                                 on_delete=models.CASCADE)
    product = models.ForeignKey(Product,
                                verbose_name=_("პროდუქტი"),
                                related_name="carts",
                                on_delete=models.CASCADE)
    quantity = models.PositiveIntegerField(_("რაოდენობა"), default=1)
    total_price = models.DecimalField(_("ჯამური ფასი"), default=0,
                                      max_digits=10, decimal_places=2)
    order = models.PositiveIntegerField(default=0, editable=False, db_index=True)

    class Meta:
        verbose_name = _("კალათა")
        verbose_name_plural = _("კალათები")

    def __str__(self):
        return f"{self.customer.username} - {self.product.name} - {self.quantity} - {self.total_price}"
