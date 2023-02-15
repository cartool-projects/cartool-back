from django.utils.translation import gettext_lazy as _
from django.db import models


class ProductStatus(models.IntegerChoices):
    AVAILABLE = 0, _('ხელმისაწვდომი')
    OUT_OF_STOCK = 1, _('მარაგში არ არის')
    COMING_SOON = 2, _('Coming Soon')
    DISCOUNT = 3, _('ფასდაკლება')


class OrderStatus(models.IntegerChoices):
    PROCESSING = 0, _('პროცესშია')
    DELIVERED = 1, _('მიღებულია')


class PaymentMethod(models.IntegerChoices):
    CASH_ON_DELIVERY = 0, _('ნაღდი ფული')
    CREDIT_CARD = 1, _('ბარათით')
    OTHERS = 2, _('სხვა')