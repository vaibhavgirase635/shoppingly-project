# Generated by Django 4.1.6 on 2023-03-07 08:49

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('app', '0003_reviewrating'),
    ]

    operations = [
        migrations.AddField(
            model_name='orderplaced',
            name='razorpay_order_id',
            field=models.CharField(blank=True, max_length=100, null=True),
        ),
        migrations.AddField(
            model_name='orderplaced',
            name='razorpay_payment_id',
            field=models.CharField(blank=True, max_length=100, null=True),
        ),
        migrations.AddField(
            model_name='orderplaced',
            name='razorpay_payment_signature',
            field=models.CharField(blank=True, max_length=100, null=True),
        ),
        migrations.AlterField(
            model_name='product',
            name='category',
            field=models.CharField(choices=[('M', 'Mobile'), ('L', 'Laptop'), ('TW', 'Top Wear'), ('BW', 'Bottom Wear'), ('A', 'Atta'), ('C', 'Chhola'), ('CO', 'Cooking Oil'), ('K', 'Kitchen'), ('R', 'Rice'), ('DP', 'Dal/Pulses'), ('N', 'Nuts'), ('P', 'Pasta & Noodles'), ('SO', 'Special Offer')], max_length=2),
        ),
    ]
