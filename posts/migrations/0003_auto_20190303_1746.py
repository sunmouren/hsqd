# Generated by Django 2.1.7 on 2019-03-03 17:46

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('posts', '0002_comment'),
    ]

    operations = [
        migrations.RenameField(
            model_name='comment',
            old_name='video',
            new_name='post',
        ),
    ]
