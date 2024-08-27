# Generated by Django 5.0.4 on 2024-08-09 11:19

import django.db.models.deletion
from django.db import migrations, models


class Migration(migrations.Migration):

    initial = True

    dependencies = [
    ]

    operations = [
        migrations.CreateModel(
            name='Vegetable',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(max_length=100)),
                ('description', models.TextField()),
                ('price', models.DecimalField(decimal_places=2, max_digits=10)),
                ('stock', models.IntegerField()),
                ('date_add', models.DateTimeField(auto_now_add=True)),
            ],
        ),
        migrations.CreateModel(
            name='Command',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('quantity', models.IntegerField()),
                ('name_client', models.CharField(max_length=100)),
                ('adrress_client', models.CharField(max_length=200)),
                ('date_command', models.DateTimeField(auto_now_add=True)),
                ('statut', models.CharField(default='En cours', max_length=50)),
                ('Vegetable', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='vegetable_shop.vegetable')),
            ],
        ),
    ]
