# Generated by Django 4.2.5 on 2023-10-19 13:06

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('user_profile', '0001_initial'),
        ('posts', '0053_delete_subscription'),
    ]

    operations = [
        migrations.AlterField(
            model_name='posts',
            name='user_profile',
            field=models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.CASCADE, related_name='user_posts', to='user_profile.userprofile'),
        ),
        migrations.DeleteModel(
            name='UserProfile',
        ),
    ]