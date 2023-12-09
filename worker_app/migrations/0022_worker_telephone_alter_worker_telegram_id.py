# Generated by Django 4.2.7 on 2023-12-09 14:52

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('worker_app', '0021_alter_worker_telegram_id'),
    ]

    operations = [
        migrations.AddField(
            model_name='worker',
            name='telephone',
            field=models.IntegerField(default=123, verbose_name='Телефон'),
            preserve_default=False,
        ),
        migrations.AlterField(
            model_name='worker',
            name='telegram_id',
            field=models.IntegerField(blank=True, null=True, unique=True, verbose_name='Телеграм_айди'),
        ),
    ]
