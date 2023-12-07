from django.db import models

# TODO перепроверить автодата нигде не будет ли перезаписывать нчиего?


class Worker(models.Model):
    name = models.CharField(max_length=10, verbose_name='Имя')
    surname = models.CharField(max_length=10, verbose_name='Фамилия')
    telegram_id = models.IntegerField(unique=True, verbose_name='Телеграм_id', blank=True, null=True)

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


class Travel(models.Model):
    object = models.ForeignKey(Object, on_delete=models.CASCADE, verbose_name='Объект')
    worker = models.ForeignKey(Worker, on_delete=models.CASCADE, verbose_name='Рабочий')
    rate = models.IntegerField(verbose_name='Сумма в день', default=700)

    date_start = models.DateField(verbose_name='Начало командировки')
    date_finish = models.DateField(verbose_name='Окончание командировки', blank=True, null=True)

    class Meta:
        verbose_name = 'Командировка'
        verbose_name_plural = 'Командировки'

    def __str__(self):
        return f"{self.object}  --  {self.worker}  --  {self.date_start}"


class TravelBenefits(models.Model):
    travel = models.ForeignKey(Travel, on_delete=models.CASCADE, verbose_name='Командировка')
    paid_for_travel = models.IntegerField(verbose_name='Выплаченно за командировку')

    date = models.DateField(verbose_name='Дата выплаты')

    class Meta:
        verbose_name = 'Командировочная выплата'
        verbose_name_plural = 'Командировочные выплаты'

    def __str__(self):
        return f"Выплата за командировку №{self.pk}"
