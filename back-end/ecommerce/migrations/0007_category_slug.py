# Generated by Django 4.1.5 on 2023-02-24 10:24

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('ecommerce', '0006_category_parent_remove_product_category_and_more'),
    ]

    operations = [
        migrations.AddField(
            model_name='category',
            name='slug',
            field=models.SlugField(blank=True, max_length=255, null=True, unique=True, verbose_name='სლაგი'),
        ),
    ]
