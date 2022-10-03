# Generated by Django 4.1.1 on 2022-10-03 20:43

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    initial = True

    dependencies = [
    ]

    operations = [
        migrations.CreateModel(
            name='ClientIp',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('created_at', models.DateTimeField(auto_now_add=True)),
                ('updated_at', models.DateTimeField(auto_now=True)),
                ('client_ip', models.CharField(max_length=15, null=True, unique=True)),
            ],
            options={
                'db_table': 'client_ip',
            },
        ),
        migrations.CreateModel(
            name='Url',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('created_at', models.DateTimeField(auto_now_add=True)),
                ('updated_at', models.DateTimeField(auto_now=True)),
                ('original_url', models.URLField()),
                ('shortened_url_key', models.CharField(max_length=15, unique=True)),
            ],
            options={
                'db_table': 'url',
            },
        ),
        migrations.CreateModel(
            name='UrlShorteningRequest',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('created_at', models.DateTimeField(auto_now_add=True)),
                ('updated_at', models.DateTimeField(auto_now=True)),
                ('client_ip', models.ForeignKey(on_delete=django.db.models.deletion.RESTRICT, to='shortening.clientip')),
                ('url', models.ForeignKey(on_delete=django.db.models.deletion.RESTRICT, to='shortening.url')),
            ],
            options={
                'db_table': 'url_shortening_request',
            },
        ),
    ]
