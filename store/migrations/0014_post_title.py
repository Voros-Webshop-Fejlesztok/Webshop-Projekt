# Generated by Django 4.2.9 on 2024-02-23 18:20

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('store', '0013_alter_post_likes'),
    ]

    operations = [
        migrations.AddField(
            model_name='post',
            name='title',
            field=models.CharField(blank=True, max_length=30, null=True),
        ),
    ]
