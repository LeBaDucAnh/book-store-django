# Generated by Django 4.0.6 on 2022-07-21 03:30

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('myapp', '0008_alter_customer_email'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='customer',
            name='username',
        ),
        migrations.AlterField(
            model_name='customer',
            name='email',
            field=models.EmailField(max_length=254),
        ),
    ]