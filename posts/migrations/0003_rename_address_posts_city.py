# Generated by Django 3.2.10 on 2023-11-17 16:12

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('posts', '0002_auto_20231113_1326'),
    ]

    operations = [
        migrations.RenameField(
            model_name='posts',
            old_name='address',
            new_name='city',
        ),
    ]
