import datetime

from django.apps import apps
from django.contrib import admin
from django.core.handlers.wsgi import WSGIRequest
from django.db.models import QuerySet
from django.http import HttpResponseRedirect, HttpResponse
from django.shortcuts import render

from apps.main.admin.forms import ChangeStatusForm, CreateDepartureForm
from apps.main.models.models import (
    Element,
    Order,
    StatusStory,
    Source,
    CheckingOrder,
    ComplianceOrder,
    LoadingOrder,
    Status,
    City,
    SentOrder,
    WorkOrder,
    Departure
)


class StatusStoryInline(admin.TabularInline):
    model = StatusStory
    can_delete = False
    extra = 0
    show_change_link = False
    fields = ('status', 'order_comment',)
    readonly_fields = fields

    def has_add_permission(self, request: WSGIRequest, obj: StatusStory or None = None) -> bool:
        return False

    def has_delete_permission(self, request: WSGIRequest, obj: StatusStory or None = None) -> bool:
        return False

    def has_change_permission(self, request: WSGIRequest, obj: StatusStory or None = None) -> bool:
        return False


class ElementInline(admin.TabularInline):
    model = Element
    can_delete = False
    extra = 0
    show_change_link = False
    fields = ('amount', 'name', 'weight', 'price')


class OrderInline(admin.TabularInline):
    model = Order
    can_delete = False
    show_change_link = False
    extra = 0
    ordering = ('date_to',)
    readonly_fields = (
        'weight',
        'timings',
        'price',
    )
    fields = (
        'number',
        'source',
        'address',
        'timings',
        'delivery_price',
        'price',
        'logic_slots',
        'weight',
    )

    def has_add_permission(self, request: WSGIRequest, obj: StatusStory) -> bool:
        return False

    def has_delete_permission(self, request: WSGIRequest, obj: Order or None = None) -> bool:
        return False

    def has_change_permission(self, request: WSGIRequest, obj: Order or None = None) -> bool:
        return False

    @admin.display(
        description="Общий вес",
    )
    def weight(self, obj: Order) -> str:
        result = str(sum(
            map(lambda element: element[0] * element[1], list(obj.elements.values_list('weight', 'amount')))
        )).replace('.', ',')
        return result if result != '0' else '0,0'

    @admin.display(
        description="Цена товаров",
    )
    def price(self, obj: Order) -> str:
        result = str(sum(
            map(lambda element: element[0] * element[1], list(obj.elements.values_list('price', 'amount')))
        )).replace('.', ',')

        return result if result != '0' else '0,0'

    @admin.display(
        description="Вилка времени",
    )
    def timings(self, obj: Order) -> str:
        if obj.date_from and obj.date_from:
            return f"{obj.date_from} - {obj.date_to}"
        return ""

    @admin.display(
        description="Что в заказе",
    )
    def elements_names(self, obj: Order) -> str:
        return ', '.join(obj.elements.values_list('name', flat=True))


class ElementViewInline(ElementInline):
    show_change_link = False
    readonly_fields = ElementInline.fields

    def has_add_permission(self, request: WSGIRequest, obj: StatusStory) -> bool:
        return False

    def has_delete_permission(self, request: WSGIRequest, obj: Order or None = None) -> bool:
        return False

    def has_change_permissionn(self, request: WSGIRequest, obj: Order or None = None) -> bool:
        return False


@admin.register(Source)
class SourceAdmin(admin.ModelAdmin):
    ordering = ('name',)
    list_display = ('name',)
    list_display_links = ('name',)


@admin.register(City)
class CityAdmin(admin.ModelAdmin):
    ordering = ('name',)
    list_display = ('name',)
    list_display_links = ('name',)


@admin.register(Order)
class OrderAdmin(admin.ModelAdmin):
    search_fields = (
        'number',
        'customers_name',
        'customers_phone',
        'city__name',
        'address',
        'elements__name',
        'source__name',
    )
    search_help_text = (
        'Поиск осуществляется по полям: Номер, Адрес, Имя заказчика, Номер телефона заказчика, Название товара, Источник, Город'
    )
    list_filter = ('city__name',)
    ordering = ('date',)
    fieldsets: list[tuple[str, object]] = [
        (
            'Внешние данные',
            {
                'fields':
                    (
                        'source',
                        'number',
                        'customers_name',
                        'customers_phone',
                        'city',
                        'address',
                    )
            },
        ),
        (
            'Внутренние данные', {
                'fields':
                    (
                        'status',
                        'date_from',
                        'date_to',
                        'date',
                        'delivery_position',
                        'weight',
                        'price',
                        'delivery_price',
                        'logic_slots',
                        'order_comment',
                    ),
            },
        ),
    ]
    list_display = ('number', 'city', 'date', 'status')
    list_display_links = ('number', 'city', 'date', 'status')
    readonly_fields = ('weight', 'status', 'price')
    inlines = (ElementInline, StatusStoryInline)

    @admin.display(
        description="Общий вес",
    )
    def weight(self, obj: Order) -> str:
        result = str(sum(
            map(lambda element: element[0] * element[1], list(obj.elements.values_list('weight', 'amount')))
        )).replace('.', ',')
        return result if result != '0' else '0,0'

    @admin.display(
        description="Цена товаров",
    )
    def price(self, obj: Order) -> str:
        result = str(sum(
            map(lambda element: element[0] * element[1], list(obj.elements.values_list('price', 'amount')))
        )).replace('.', ',')

        return result if result != '0' else '0,0'

    @admin.display(
        description="Вилка времени",
    )
    def timings(self, obj: Order) -> str:
        if obj.date_from and obj.date_from:
            return f"{obj.date_from} - {obj.date_to}"
        return ""

    @admin.display(
        description="Что в заказе",
    )
    def elements_names(self, obj: Order) -> str:
        return ', '.join(obj.elements.values_list('name', flat=True))


@admin.register(WorkOrder)
class WorkOrderAdmin(OrderAdmin):
    list_display = (
        'number',
        'customers_phone',
        'customers_name',
        'elements_names',
        'price',
        'source',
        'status',
    )
    list_display_links = list_display

    def get_queryset(self, request: WSGIRequest) -> QuerySet[Order]:
        qs = self.model._default_manager.get_queryset().exclude(status=Status.SENT)
        ordering = self.get_ordering(request)
        if ordering:
            qs = qs.order_by(*ordering)
        return qs


class StatusOrderAdmin(OrderAdmin):
    model = None
    readonly_fields = (
        'source',
        'number',
        'customers_name',
        'customers_phone',
        'city',
        'address',
        'status',
        'date_from',
        'date_to',
        'date',
        'delivery_position',
        'weight',
        'price',
        'delivery_price',
        'logic_slots',
        'order_comment',
    )
    inlines = (ElementViewInline, StatusStoryInline)
    list_display = [
        'source',
        'number',
        'elements_names',
        'address',
        'customers_phone',
        'customers_name',
        'date_from',
        'date_to',
        'price',
        'delivery_price',
        'delivery_position',
    ]
    list_display_links = list_display
    actions = ('change_status', 'return_order')

    status = None
    next_status = ('', '')

    def has_add_permission(self, request: WSGIRequest) -> bool:
        return False

    def has_delete_permission(self, request: WSGIRequest, obj: Order or None = None) -> bool:
        return False

    def get_actions(self, request):
        actions = super().get_actions(request)
        if not request.user.has_perm(
                self.model._meta.app_label + '.' + apps.get_model(
                    'auth',
                    'Permission'
                ).objects.get(
                    content_type__model=self.model._meta.model_name,
                    codename__startswith='change_'
                ).codename
        ):
            actions.pop('change_status')
            actions.pop('return_order')
        return actions

    @admin.action(description='Вернуть заказ(ы)')
    def return_order(
            modeladmin,
            request: WSGIRequest,
            queryset: QuerySet[Order]
    ) -> HttpResponseRedirect or HttpResponse:
        forms: list[list] = []

        if 'apply' in request.POST:
            count = 0
            for element in zip(request.POST.getlist('message'), request.POST.getlist('element')):
                oreder = Order.objects.get(pk=element[-1])
                print(oreder.__dict__)
                oreder.status = Status.CHECKING
                oreder.save()
                status_story = StatusStory(status=Status.RETURN, order=oreder, order_comment=element[0])
                status_story.save()
                count += 1
            modeladmin.message_user(request, f"Статус {Status.RETURN[-1]} применена к {count} товарам.")
            return HttpResponseRedirect(request.get_full_path())

        if not forms:
            print(request.POST)
            for element in request.POST.getlist('_selected_action'):
                forms.append([
                    ChangeStatusForm(
                        initial={
                            '_selected_action': element,
                        }
                    ), element, Order.objects.get(pk=element)
                ])

        return render(request, 'change_status.html',
                      {'items': queryset, 'forms': forms, 'title': u'Изменения статусов',
                       'action': 'return_order'})

    @admin.action(description=f'Сменить статус')
    def change_status(
            modeladmin,
            request: WSGIRequest,
            queryset: QuerySet[Order]
    ) -> HttpResponseRedirect or HttpResponse:
        forms = []

        print(request.POST)

        if 'apply' in request.POST:
            count = 0
            for element in zip(request.POST.getlist('message'), request.POST.getlist('element')):
                oreder = Order.objects.get(pk=element[-1])
                oreder.status = modeladmin.next_status
                oreder.save()
                status_story = StatusStory(status=modeladmin.next_status, order=oreder,
                                           order_comment=element[0])
                status_story.save()
                count += 1
            modeladmin.message_user(request, f"Статус сменён у {count} заказов.")
            return HttpResponseRedirect(request.get_full_path())

        if not forms:
            for element in request.POST.getlist('_selected_action'):
                forms.append([
                    ChangeStatusForm(
                        initial={
                            '_selected_action': element,
                        }
                    ), element, Order.objects.get(pk=element)
                ])

        return render(request, 'change_status.html',
                      {'items': queryset, 'forms': forms, 'title': u'Изменения статусов',
                       'action': 'change_status'})

    def get_queryset(self, request: WSGIRequest) -> QuerySet[Order]:
        qs = self.model._default_manager.get_queryset().filter(status=self.status)
        ordering = self.get_ordering(request)
        if ordering:
            qs = qs.order_by(*ordering)
        return qs

    class Meta:
        abstract = True


@admin.register(CheckingOrder)
class CheckingOrderAdmin(StatusOrderAdmin):
    status = Status.CHECKING
    next_status = Status.COMPLIANCE


@admin.register(ComplianceOrder)
class ComplianceOrderAdmin(StatusOrderAdmin):
    status = Status.COMPLIANCE
    next_status = Status.LOADING
    readonly_fields = (
        'source',
        'number',
        'customers_name',
        'customers_phone',
        'city',
        'address',
        'status',
        'date',
        'weight',
        'price',
        'delivery_price',
        'logic_slots',
        'order_comment',
    )


@admin.register(LoadingOrder)
class LoadingOrderAdmin(StatusOrderAdmin):
    status = Status.LOADING
    next_status = Status.SENT

    @admin.action(description=f'Сменить статус')
    def change_status(
            modeladmin,
            request: WSGIRequest,
            queryset: QuerySet[Order]
    ) -> HttpResponseRedirect or HttpResponse:
        form = None
        if 'apply' in request.POST:
            print(request.POST)
            departure = Departure.objects.create(
                direction=request.POST.getlist('direction')[0],
                invoice_cost=request.POST.getlist('invoice_cost')[0],
                date=datetime.datetime.strptime(request.POST.getlist('date')[0], '%d.%m.%Y').date(),
            )
            departure.orders.set(Order.objects.filter(pk__in=request.POST.getlist('_selected_action')))
            for order in Order.objects.filter(pk__in=request.POST.getlist('_selected_action')):
                order.status = modeladmin.next_status
                order.save()
                status_story = StatusStory(
                    status=modeladmin.next_status,
                    order=order,
                    order_comment=f"Добавлен в выезд от {departure.date}, по направлению {departure.direction}")
                status_story.save()
            result = ', '.join(
                Order.objects.filter(pk__in=request.POST.getlist('_selected_action')).values_list('number', flat=True))
            modeladmin.message_user(
                request,
                f"Заказы: ({result}) добавлены  в выезд от {departure.date}, по направлению {departure.direction}.")
            return HttpResponseRedirect(request.get_full_path())

        if not form:
            form = CreateDepartureForm(
                initial={'_selected_action': request.POST.getlist('_selected_action'), 'date': datetime.date.today(), })

        return render(request, 'create_departure.html',
                      {'items': queryset, 'form': form, 'title': u'Изменение категории'})


@admin.register(SentOrder)
class SentOrderAdminOld(StatusOrderAdmin):
    status = Status.SENT
    next_status = Status.SENT
    actions = None


@admin.register(Departure)
class SentOrderAdmin(admin.ModelAdmin):
    search_fields = ('orders__number', 'orders__address', 'orders__customers_name')
    search_help_text = 'Поиск осуществляется по полям заказов: Номер, Адрес, Имя заказчика'
    list_filter = ('direction', 'orders__source')
    ordering = ('date',)
    fields = ('invoice_cost', 'date', 'direction')
    readonly_fields = fields
    list_display = ('date', 'direction', 'invoice_cost', 'price', 'delivery_price')
    list_display_links = list_display
    inlines = (OrderInline,)

    @admin.display(
        description="Цена товаров",
    )
    def price(self, obj: Departure) -> str:
        result = 0.0
        for order in obj.orders.all():
            result += sum(
                map(lambda element: element[0] * element[1], list(order.elements.values_list('price', 'amount')))
            )
        result = str(result).replace('.', ',')
        return result if result != '0' else '0,0'

    @admin.display(
        description="Цена доставки",
    )
    def delivery_price(self, obj: Departure) -> str:
        result = str(sum(obj.orders.values_list('delivery_price', flat=True))).replace('.', ',')
        return result if result != '0' else '0,0'

    def has_add_permission(self, request: WSGIRequest) -> bool:
        return False

    def has_delete_permission(self, request: WSGIRequest, obj: Departure or None = None) -> bool:
        return False
