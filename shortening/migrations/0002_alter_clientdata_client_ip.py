# Generated by Django 4.1.2 on 2022-10-04 13:28

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('shortening', '0001_initial'),
    ]

    operations = [
        migrations.AlterField(
            model_name='clientdata',
            name='client_ip',
            field=models.GenericIPAddressField(null=True, unique=True),
        ),
    ]