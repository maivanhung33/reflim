# Generated by Django 3.0.5 on 2020-06-24 06:24

from django.db import migrations, models
import uuid


class Migration(migrations.Migration):

    dependencies = [
        ('post', '0012_auto_20200624_1048'),
    ]

    operations = [
        migrations.AddField(
            model_name='usercommentpost',
            name='parentId',
            field=models.UUIDField(blank=True, default=uuid.uuid4, editable=False, null=True),
        ),
    ]
