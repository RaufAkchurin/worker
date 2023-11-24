# Generated by Django 4.2.7 on 2023-11-16 15:02

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('worker_app', '0007_remove_worktype_object'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='shift',
            name='object',
        ),
        migrations.AlterField(
            model_name='worker',
            name='telegram_id',
            field=models.CharField(max_length=50, unique=True),
        ),
        migrations.AlterField(
            model_name='worktype',
            name='measurement_type',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='worker_app.measurement'),
        ),
    ]