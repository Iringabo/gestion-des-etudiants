# Generated by Django 5.0 on 2024-02-15 10:31

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('app', '0006_note_slug'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='note',
            name='slug',
        ),
    ]
