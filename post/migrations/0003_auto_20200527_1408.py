# Generated by Django 3.0.5 on 2020-05-27 07:08

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('post', '0002_auto_20200527_1357'),
    ]

    operations = [
        migrations.AlterField(
            model_name='post',
            name='name_film',
            field=models.CharField(max_length=255),
        ),
        migrations.AlterField(
            model_name='post',
            name='title',
            field=models.CharField(blank=True, max_length=255, null=True),
        ),
    ]
