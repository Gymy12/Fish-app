# Generated by Django 3.0.5 on 2024-06-17 03:32

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('fishapp', '0002_auto_20240617_0242'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='product',
            name='count',
        ),
        migrations.RemoveField(
            model_name='productattribute',
            name='count',
        ),
        migrations.DeleteModel(
            name='Count',
        ),
    ]
