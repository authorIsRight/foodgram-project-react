# Generated by Django 2.2.16 on 2022-12-03 14:03

import colorfield.fields
from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('recipes', '0001_initial'),
    ]

    operations = [
        migrations.AlterField(
            model_name='tag',
            name='color',
            field=colorfield.fields.ColorField(blank=True, default='#FFFFE0', image_field=None, max_length=7, null=True, samples=None, unique=True, verbose_name='Цвет в HEX'),
        ),
    ]
