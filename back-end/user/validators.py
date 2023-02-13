from django.core.exceptions import ValidationError
from django.utils.translation import gettext_lazy as _
import re


def validate_phone_number(value):
    reg = re.compile('^[5][0-9]{8}$')
    if not reg.match(value.replace(" ", "")):
        raise ValidationError(_('ტელეფონის ნომერი არავალიდურია(5** *** ***)'))


def validate_email(value):
    reg = re.compile('^[a-zA-Z0-9_.+-]+@[a-zA-Z0-9-]+\.[a-zA-Z0-9-.]+$')
    if not reg.match(value):
        raise ValidationError(_('მეილი არავალიდურია'))


def validate_first_name(value):
    reg = re.compile('^[^0-9]+$')
    if not reg.match(value):
        raise ValidationError(_('სახელი არავალიდურია'))

def validate_last_name(value):
    reg = re.compile('^[^0-9]+$')
    if not reg.match(value):
        raise ValidationError(_('გვარი არავალიდურია'))
