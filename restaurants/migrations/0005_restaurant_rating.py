# Generated by Django 4.2.7 on 2023-11-25 17:28

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('restaurants', '0004_menuitem_is_popular'),
    ]

    operations = [
        migrations.AddField(
            model_name='restaurant',
            name='rating',
            field=models.FloatField(default=0.0),
        ),
    ]
