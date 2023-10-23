# Generated by Django 4.2.5 on 2023-10-20 12:27

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('posts', '0061_alter_posts_image_height_alter_posts_image_width'),
    ]

    operations = [
        migrations.AlterField(
            model_name='posts',
            name='image_height',
            field=models.PositiveIntegerField(default=320),
        ),
        migrations.AlterField(
            model_name='posts',
            name='image_width',
            field=models.PositiveIntegerField(default=350),
        ),
    ]
