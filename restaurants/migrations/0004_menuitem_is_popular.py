# Generated by Django 4.2.7 on 2023-11-25 09:16

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('restaurants', '0003_remove_restaurant_description'),
    ]

    operations = [
        migrations.AddField(
            model_name='menuitem',
            name='is_popular',
            field=models.BooleanField(default=False),
        ),
    ]
