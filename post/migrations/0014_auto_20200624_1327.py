# Generated by Django 3.0.5 on 2020-06-24 06:27

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('post', '0013_usercommentpost_parentid'),
    ]

    operations = [
        migrations.AlterField(
            model_name='usercommentpost',
            name='parentId',
            field=models.UUIDField(blank=True, editable=False, null=True),
        ),
    ]
