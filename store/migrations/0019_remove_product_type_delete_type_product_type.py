# Generated by Django 4.2.9 on 2024-01-23 18:59

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('store', '0018_remove_product_views_product_rating'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='product',
            name='type',
        ),
        migrations.DeleteModel(
            name='Type',
        ),
        migrations.AddField(
            model_name='product',
            name='type',
            field=models.CharField(default='', max_length=100),
        ),
    ]