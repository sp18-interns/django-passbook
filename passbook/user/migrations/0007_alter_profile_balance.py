# Generated by Django 4.0.5 on 2022-07-27 07:48

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('user', '0006_alter_transaction_closing_balance_and_more'),
    ]

    operations = [
        migrations.AlterField(
            model_name='profile',
            name='balance',
            field=models.IntegerField(default=0),
        ),
    ]
