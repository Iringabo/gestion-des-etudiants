# Generated by Django 5.0 on 2024-02-15 10:27

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('app', '0005_userprofile_groups_userprofile_is_superuser_and_more'),
    ]

    operations = [
        migrations.AddField(
            model_name='note',
            name='slug',
            field=models.SlugField(blank=True, max_length=255, unique=True),
        ),
    ]
