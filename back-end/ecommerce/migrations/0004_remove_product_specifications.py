# Generated by Django 4.1.5 on 2023-02-15 13:41

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('ecommerce', '0003_remove_product_image_alter_cart_quantity_and_more'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='product',
            name='specifications',
        ),
    ]
