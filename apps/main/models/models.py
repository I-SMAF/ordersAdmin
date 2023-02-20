from django.db import models


class Source(models.Model):
    """
    Модель источника заказа
    """

    class Meta:
        verbose_name = 'источник заказа'
        verbose_name_plural = 'источники заказов'

    name = models.CharField(
        verbose_name='название',
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

    CHECKING = 'checking', 'проверка наличия (склад)'
    COMPLIANCE = 'compliance', 'проверка логистического соответствия'
    LOADING = 'loading', 'погрузка'
    RETURN = 'return', 'возврат'


class Order(models.Model):
    """
    Модель заказа
    """

    class Meta:
        verbose_name = 'заказ'
        verbose_name_plural = 'заказы'

    status = models.CharField(
        verbose_name='статус заказа',
        max_length=256,
        choices=Status.choices,
        default=Status.CHECKING
    )
    number = models.CharField(
        verbose_name='номер заказа',
        max_length=256
    )
    source = models.ForeignKey(
        to=Source,
        verbose_name='источник заказа',
        on_delete=models.DO_NOTHING,
        related_name='orders'
    )
    price = models.PositiveIntegerField(  # null_by_design
        verbose_name='цена',
        default=0,
        null=True,
        blank=True
    )
    customers_name = models.CharField(
        verbose_name='имя заказчика',
        max_length=256
    )
    customers_phone = models.CharField(
        verbose_name='номер телефона заказчика',
        max_length=256
    )
    address = models.CharField(
        verbose_name='адрес заказа',
        max_length=256
    )

    date = models.DateField(
        verbose_name='конечная дата заказа',
    )
    delivery_price = models.PositiveIntegerField(  # null_by_design
        verbose_name='цена доставки',
        default=0,
        null=True,
        blank=True
    )
    delivery_position = models.SmallIntegerField(  # null_by_design
        verbose_name='позиция погрузки',
        default=0,
        null=True,
        blank=True
    )
    order_comment = models.TextField(  # null_by_design
        verbose_name='комментарий заказа',
        null=True,
        blank=True
    )

    def __str__(self) -> str:
        return f'{self.number}'

    def __repr__(self) -> str:
        return self.__str__()


class CheckingOrder(Order):
    """
    Proxy Модель заказа
    """

    class Meta:
        proxy = True
        verbose_name = 'заказ'
        verbose_name_plural = f'заказы - проверка наличия (склад)'


class ComplianceOrder(Order):
    """
    Proxy Модель заказа
    """

    class Meta:
        proxy = True
        verbose_name = 'заказ'
        verbose_name_plural = f'заказы - проверка логистического соответствия'


class LoadingOrder(Order):
    """
    Proxy Модель заказа
    """

    class Meta:
        proxy = True
        verbose_name = 'заказ'
        verbose_name_plural = f'заказы - погрузка'


class ReturnOrder(Order):
    """
    Proxy Модель заказа
    """

    class Meta:
        proxy = True
        verbose_name = 'заказ'
        verbose_name_plural = f'заказы - возврат'


class Element(models.Model):
    """
    Модель товара
    """

    class Meta:
        verbose_name = 'товар'
        verbose_name_plural = 'товары'

    amount = models.PositiveSmallIntegerField(
        verbose_name='количество',
        default=0
    )
    name = models.CharField(
        verbose_name='название',
        max_length=256
    )
    order = models.ForeignKey(
        to=Order,
        verbose_name='заказ',
        on_delete=models.CASCADE,
        related_name='elements'
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
        verbose_name = 'история статуса'
        verbose_name_plural = 'история статусов'

    status = models.CharField(
        verbose_name='статус заказа',
        max_length=256,
        choices=Status.choices
    )
    order_comment = models.TextField(
        verbose_name='комментарий',
        null=True,
        blank=True
    )
    order = models.ForeignKey(
        to=Order,
        verbose_name='заказ',
        on_delete=models.CASCADE,
        related_name='status_story'
    )

    def __str__(self) -> str:
        return f'{self.status}: {self.order}'

    def __repr__(self) -> str:
        return self.__str__()
