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
        verbose_name = 'Результат за день'
        verbose_name_plural = 'Результаты за день'

    def __str__(self):
        return f"{self.worker.name} -- {self.work_type} -- {self.date}"


class WorkersBenefits(models.Model):
    worker = models.ForeignKey(Worker, on_delete=models.CASCADE, verbose_name='Рабочий')
    object = models.ForeignKey(Object, on_delete=models.CASCADE, verbose_name='Объект')
    paid_amount = models.IntegerField(verbose_name='Выплаченная сумма')
    date = models.DateField(verbose_name='Дата')

    class Meta:
        verbose_name = 'Выплата рабочему'
        verbose_name_plural = 'Выплаты рабочим'

    def __str__(self):
        return f"{self.date.day}.{self.date.month}.{self.date.year} -- {self.worker.name} -- {self.object} -- {self.paid_amount}"


class TravelBenefits(models.Model):
    worker = models.ForeignKey(Worker, on_delete=models.CASCADE, verbose_name='Рабочий')
    object = models.ForeignKey(Object, on_delete=models.CASCADE, verbose_name='Объект')
    period = models.CharField(max_length=7, verbose_name='За период')
    days_to_pay = models.IntegerField(verbose_name='Дней к оплате')
    rate = models.IntegerField(verbose_name='Сумма в день', default=700)
    date = models.DateField(verbose_name='Дата выплаты')

    class Meta:
        verbose_name = 'Командировочная выплата'
        verbose_name_plural = 'Командировочные выплаты'
        unique_together = ('worker', 'object', 'period')

    def __str__(self):
        return f"{self.worker.name} -- {self.object} -- {self.period} -- {self.date}"

    @staticmethod
    def generate_period_choices():
        choices = []
        for year in range(2023, 2030):  # Выберите нужный диапазон лет
            for month in range(1, 13):
                choices.append((f"{year}-{month:02d}", f"{month:02d}/{year}"))
        return choices
