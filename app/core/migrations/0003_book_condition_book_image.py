# Generated by Django 4.2.5 on 2023-09-29 14:08

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('core', '0002_book'),
    ]

    operations = [
        migrations.AddField(
            model_name='book',
            name='condition',
            field=models.CharField(max_length=255, null=True),
        ),
        migrations.AddField(
            model_name='book',
            name='image',
            field=models.CharField(max_length=255, null=True),
        ),
    ]
