# Generated by Django 5.0.6 on 2024-06-27 12:05

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('mainApp', '0004_delete_review'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='modelparameter',
            name='updated_at',
        ),
        migrations.AddField(
            model_name='modelparameter',
            name='original_filename',
            field=models.CharField(blank=True, max_length=255, null=True),
        ),
    ]
