# Generated by Django 3.0.5 on 2020-06-20 13:06

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('post', '0003_auto_20200527_1408'),
    ]

    operations = [
        migrations.AddField(
            model_name='post',
            name='film_type',
            field=models.IntegerField(default=1),
        ),
    ]
