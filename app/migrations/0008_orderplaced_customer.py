# Generated by Django 4.1.6 on 2023-03-13 13:49

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('app', '0007_remove_orderplaced_customer'),
    ]

    operations = [
        migrations.AddField(
            model_name='orderplaced',
            name='customer',
            field=models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.CASCADE, to='app.customer'),
        ),
    ]
