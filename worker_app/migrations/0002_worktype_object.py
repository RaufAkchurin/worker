# Generated by Django 4.2.7 on 2023-11-16 13:41

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('worker_app', '0001_initial'),
    ]

    operations = [
        migrations.AddField(
            model_name='worktype',
            name='object',
            field=models.ForeignKey(default=1, on_delete=django.db.models.deletion.CASCADE, to='worker_app.object'),
            preserve_default=False,
        ),
    ]
