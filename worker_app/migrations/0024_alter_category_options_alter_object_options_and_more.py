# Generated by Django 4.2.7 on 2024-03-09 07:13

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('worker_app', '0023_alter_shift_unique_together'),
    ]

    operations = [
        migrations.AlterModelOptions(
            name='category',
            options={'ordering': ['id'], 'verbose_name': 'Категория', 'verbose_name_plural': 'Категории'},
        ),
        migrations.AlterModelOptions(
            name='object',
            options={'ordering': ['id'], 'verbose_name': 'Объект', 'verbose_name_plural': 'Объекты'},
        ),
        migrations.AlterModelOptions(
            name='worktype',
            options={'ordering': ['id'], 'verbose_name': 'Тип работ', 'verbose_name_plural': 'Типы работ'},
        ),
        migrations.AddField(
            model_name='worktype',
            name='created_by',
            field=models.ForeignKey(default=18, on_delete=django.db.models.deletion.CASCADE, to='worker_app.worker', verbose_name='Автор'),
        ),
        migrations.AlterField(
            model_name='worktype',
            name='price_for_customer',
            field=models.IntegerField(default=0, verbose_name='Цена для заказчика'),
        ),
        migrations.AlterField(
            model_name='worktype',
            name='price_for_worker',
            field=models.IntegerField(default=0, verbose_name='Цена для рабочих'),
        ),
        migrations.AlterField(
            model_name='worktype',
            name='total_scope',
            field=models.IntegerField(default=0, verbose_name='Общий объём'),
        ),
        migrations.AlterUniqueTogether(
            name='worktype',
            unique_together={('category', 'name')},
        ),
    ]
