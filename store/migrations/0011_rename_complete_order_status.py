# Generated by Django 4.2.10 on 2024-03-01 19:17

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('store', '0010_alter_order_delivery_alter_order_pay'),
    ]

    operations = [
        migrations.RenameField(
            model_name='order',
            old_name='complete',
            new_name='status',
        ),
    ]
