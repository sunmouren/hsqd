# Generated by Django 2.1.7 on 2019-02-26 23:51

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('activities', '0001_initial'),
    ]

    operations = [
        migrations.AddField(
            model_name='activity',
            name='start_time',
            field=models.CharField(blank=True, max_length=50, null=True, verbose_name='开始时间'),
        ),
        migrations.AlterField(
            model_name='activity',
            name='add_time',
            field=models.DateTimeField(auto_now_add=True, verbose_name='时间'),
        ),
    ]
