# Generated by Django 3.0.5 on 2020-05-21 03:20

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('post', '0005_userlikepost'),
    ]

    operations = [
        migrations.AddField(
            model_name='userlikepost',
            name='status',
            field=models.IntegerField(blank=True, null=True),
        ),
    ]
