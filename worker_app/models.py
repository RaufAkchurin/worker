from django.db import models


class Worker(models.Model):
    name = models.CharField(max_length=10, verbose_name='Имя')
    surname = models.CharField(max_length=10, verbose_name='Фамилия')
    password = models.IntegerField(verbose_name='Пароль')
    telegram_id = models.CharField(max_length=50, unique=True, verbose_name='Телеграм')

    class Meta:
        verbose_name = 'Рабочий'
        verbose_name_plural = 'Рабочие'

    def __str__(self):
        return f"{self.surname} {self.name}"


class Measurement(models.Model):
    name = models.CharField(max_length=10, verbose_name='Название')

    class Meta:
        verbose_name = 'Ед.изм.'
        verbose_name_plural = 'Ед.изм.'

    def __str__(self):
        return self.name


class Object(models.Model):
    name = models.CharField(max_length=255, verbose_name='Название')

    class Meta:
        verbose_name = 'Объект'
        verbose_name_plural = 'Объекты'

    def __str__(self):
        return self.name


class Category(models.Model):
    name = models.CharField(max_length=255, verbose_name='Название')
    object = models.ForeignKey(Object, on_delete=models.CASCADE, verbose_name='Объект')

    class Meta:
        verbose_name = 'Категория'
        verbose_name_plural = 'Категории'

    def __str__(self):
        return f"{self.object} - {self.name}"


class WorkType(models.Model):
    category = models.ForeignKey(Category, on_delete=models.CASCADE, verbose_name='Категория')
    name = models.CharField(max_length=255, verbose_name='Название')

    price_for_worker = models.IntegerField(verbose_name='Цена для рабочих')
    price_for_customer = models.IntegerField(verbose_name='Цена для заказчика')
    total_scope = models.IntegerField(verbose_name='Общий объём')
    measurement_type = models.ForeignKey(Measurement, on_delete=models.CASCADE, verbose_name='Ед.изм.')

    class Meta:
        verbose_name = 'Тип работ'
        verbose_name_plural = 'Типы работ'

    def __str__(self):
        return self.name


class Shift(models.Model):
    worker = models.ForeignKey(Worker, on_delete=models.CASCADE, verbose_name='Рабочий')
    date = models.DateField(verbose_name='Дата')
    work_type = models.ForeignKey(WorkType, on_delete=models.CASCADE, verbose_name='Тип работ')
    value = models.IntegerField(verbose_name='Выполненный объём')

    class Meta:
        verbose_name = 'Смена'
        verbose_name_plural = 'Смены'

    def __str__(self):
        return f"{self.worker.name} -- {self.work_type} -- {self.date}"