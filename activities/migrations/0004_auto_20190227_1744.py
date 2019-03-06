# Generated by Django 2.1.7 on 2019-02-27 17:44

from django.conf import settings
from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('activities', '0003_activity_is_active'),
    ]

    operations = [
        migrations.AlterField(
            model_name='activity',
            name='creator',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='activities_creator', to=settings.AUTH_USER_MODEL, verbose_name='创建者'),
        ),
        migrations.AlterField(
            model_name='activity',
            name='title',
            field=models.CharField(max_length=100, verbose_name='活动标题'),
        ),
    ]
