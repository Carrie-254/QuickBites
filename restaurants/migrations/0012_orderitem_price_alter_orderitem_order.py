# Generated by Django 4.2.7 on 2023-11-28 15:43

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('restaurants', '0011_remove_order_name'),
    ]

    operations = [
        migrations.AddField(
            model_name='orderitem',
            name='price',
            field=models.DecimalField(decimal_places=2, default=0.0, max_digits=8),
        ),
        migrations.AlterField(
            model_name='orderitem',
            name='order',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='order_items', to='restaurants.order'),
        ),
    ]