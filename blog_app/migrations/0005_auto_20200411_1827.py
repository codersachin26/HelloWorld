# Generated by Django 3.0.3 on 2020-04-11 12:57

from django.db import migrations, models
import django.utils.timezone


class Migration(migrations.Migration):

    dependencies = [
        ('blog_app', '0004_auto_20200411_1819'),
    ]

    operations = [
        migrations.AlterField(
            model_name='article',
            name='upload_date',
            field=models.DateTimeField(default=django.utils.timezone.now),
        ),
    ]