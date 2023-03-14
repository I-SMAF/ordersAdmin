from django.db import models


class Source(models.Model):
    """
    Модель Источника Заказа
    """

    class Meta:
        verbose_name = 'Источник заказа'
        verbose_name_plural = 'Источники заказов'

    name = models.CharField(
        verbose_name='Название',
        max_length=256
    )

    def __str__(self) -> str:
        return f'{self.name}'

    def __repr__(self) -> str:
        return self.__str__()


class City(models.Model):
    """
    Модель Источника Заказа
    """

    class Meta:
        verbose_name = 'Город'
        verbose_name_plural = 'Города'

    name = models.CharField(
        verbose_name='Город',
        max_length=256
    )

    def __str__(self) -> str:
        return f'{self.name}'

    def __repr__(self) -> str:
        return self.__str__()


class Status(models.TextChoices):
    """
    TextChoices статусы
    """

    CHECKING = 'checking', 'Проверка наличия (склад)'
    COMPLIANCE = 'compliance', 'Проверка логистического соответствия'
    LOADING = 'loading', 'Погрузка'
    RETURN = 'return', 'Возврат'
    SENT = 'sent', 'Отправлено'


class Departure(models.Model):
    class Meta:
        verbose_name = 'Отправлено (Выезд)'
        verbose_name_plural = 'Отправлено (Выезды)'
        ordering = ['date']

    invoice_cost = models.PositiveIntegerField(
        verbose_name='Стоимость по накладной',
        default=0,
        null=True,
        blank=True
    )
    date = models.DateField(
        verbose_name='Дата выезда',
        null=True,
        blank=True
    )
    direction = models.CharField(
        verbose_name='Направление выезда',
        max_length=256,
        null=True,
        blank=True
    )


class Order(models.Model):
    """
    Модель заказа
    """

    class Meta:
        verbose_name = 'Заказ'
        verbose_name_plural = 'Заказы'
        ordering = ['id']

    status = models.CharField(
        verbose_name='Статус заказа',
        max_length=256,
        choices=Status.choices,
        default=Status.CHECKING
    )
    is_complaint = models.BooleanField(
        verbose_name='Рекламация',
        default=False
    )
    number = models.CharField(
        verbose_name='Номер заказа',
        max_length=256
    )
    source = models.ForeignKey(
        to=Source,
        verbose_name='Источник заказа',
        on_delete=models.DO_NOTHING,
        related_name='orders'
    )
    address = models.CharField(
        verbose_name='Адрес заказа',
        max_length=256,
        null=True
    )
    city = models.ForeignKey(
        to=City,
        verbose_name='Город',
        on_delete=models.DO_NOTHING,
        related_name='orders'
    )
    customers_name = models.CharField(
        verbose_name='Имя заказчика',
        max_length=256
    )
    customers_phone = models.CharField(
        verbose_name='Номер телефона заказчика',
        max_length=256
    )
    date = models.DateField(
        verbose_name='Конечная дата заказа',
    )
    date_from = models.TimeField(
        verbose_name='Время заказа от',
        null=True,
        blank=True,
    )
    date_to = models.TimeField(
        verbose_name='Время заказа до',
        null=True,
        blank=True,
    )
    delivery_price = models.PositiveIntegerField(
        verbose_name='Цена доставки',
        default=0,
        null=True,
        blank=True
    )
    delivery_position = models.SmallIntegerField(
        verbose_name='Позиция погрузки',
        default=0,
        null=True,
        blank=True
    )
    order_comment = models.TextField(
        verbose_name='Комментарий заказа',
        null=True,
        blank=True
    )
    logic_slots = models.PositiveIntegerField(
        verbose_name='Кол-во логистических мест',
        null=True,
        blank=True
    )
    departure = models.ForeignKey(
        to=Departure,
        on_delete=models.CASCADE,
        verbose_name='Выезд',
        null=True,
        blank=True,
        related_name='orders'
    )

    def __str__(self) -> str:
        return f'{self.number}'

    def __repr__(self) -> str:
        return self.__str__()


class WorkOrder(Order):
    """
    Proxy Модель заказа
    """

    class Meta:
        proxy = True
        verbose_name = 'Заказ в работе'
        verbose_name_plural = f'Заказы в работе'


class CheckingOrder(Order):
    """
    Proxy Модель заказа
    """

    class Meta:
        proxy = True
        verbose_name = 'Заказ проверка наличия (склад)'
        verbose_name_plural = f'Проверка наличия (склад)'


class ComplianceOrder(Order):
    """
    Proxy Модель заказа
    """

    class Meta:
        proxy = True
        verbose_name = 'Заказ проверка логистического соответствия'
        verbose_name_plural = f'Проверка логистического соответствия'


class LoadingOrder(Order):
    """
    Proxy Модель заказа
    """

    class Meta:
        proxy = True
        verbose_name = 'Заказ погрузка'
        verbose_name_plural = f'Погрузка'


class ReturnOrder(Order):
    """
    Proxy Модель заказа
    """

    class Meta:
        proxy = True
        verbose_name = 'Заказ возврат'
        verbose_name_plural = f'Возврат'


class SentOrder(Order):
    """
    Proxy Модель заказа
    """

    class Meta:
        proxy = True
        verbose_name = 'Заказ отправлено'
        verbose_name_plural = f'Отправлено (Заказы)'


class Element(models.Model):
    """
    Модель товара
    """

    class Meta:
        verbose_name = 'Товар'
        verbose_name_plural = 'Товары'

    amount = models.PositiveSmallIntegerField(
        verbose_name='Количество',
        default=1
    )
    name = models.CharField(
        verbose_name='Название',
        max_length=256
    )
    order = models.ForeignKey(
        to=Order,
        verbose_name='Заказ',
        on_delete=models.CASCADE,
        related_name='elements'
    )
    weight = models.FloatField(
        verbose_name='Вес (кг)',
        default=0.0
    )
    price = models.FloatField(
        verbose_name='Цена',
        default=0.0
    )

    def __str__(self) -> str:
        return f'{self.name}: {self.amount}'

    def __repr__(self) -> str:
        return self.__str__()


class StatusStory(models.Model):
    """
    Модель история статусов
    """

    class Meta:
        verbose_name = 'История статуса'
        verbose_name_plural = 'История статусов'

    status = models.CharField(
        verbose_name='Статус заказа',
        max_length=256,
        choices=Status.choices
    )
    order_comment = models.TextField(
        verbose_name='Комментарий',
        null=True,
        blank=True
    )
    order = models.ForeignKey(
        to=Order,
        verbose_name='Заказ',
        on_delete=models.CASCADE,
        related_name='status_story'
    )

    def __str__(self) -> str:
        return f'{self.status}: {self.order}'

    def __repr__(self) -> str:
        return self.__str__()
