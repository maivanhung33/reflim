# Generated by Django 3.0.5 on 2020-05-05 14:58

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('post', '0001_initial'),
    ]

    operations = [
        migrations.RenameField(
            model_name='post',
            old_name='userId',
            new_name='user',
        ),
    ]
