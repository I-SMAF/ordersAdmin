from django.contrib import admin
from django.core.handlers.wsgi import WSGIRequest
from django.db.models import QuerySet
from django.http import HttpResponseRedirect, HttpResponse
from django.shortcuts import render

from apps.main.admin.forms import ChangeStatusForm
from apps.main.models.models import Element, Order, StatusStory, Source, CheckingOrder, ComplianceOrder, LoadingOrder, \
    ReturnOrder, Status, City


class StatusStoryInline(admin.TabularInline):
    model = StatusStory
    can_delete = False
    extra = 0
    show_change_link = False
    fields = ('status', 'order_comment',)
    readonly_fields = fields

    def has_add_permission(self, request: WSGIRequest, obj: StatusStory | None = None) -> bool:
        return False

    def has_delete_permission(self, request: WSGIRequest, obj: StatusStory | None = None) -> bool:
        return False

    def has_change_permissionn(self, request: WSGIRequest, obj: StatusStory | None = None) -> bool:
        return False


class ElementViewInline(admin.TabularInline):
    model = Element
    can_delete = True
    extra = 0
    show_change_link = False
    fields = ('amount', 'name',)
    readonly_fields = ('amount', 'name',)

    def has_add_permission(self, request: WSGIRequest, obj: StatusStory) -> bool:
        return False

    def has_delete_permission(self, request: WSGIRequest, obj: Order | None = None) -> bool:
        return False

    def has_change_permissionn(self, request: WSGIRequest, obj: Order | None = None) -> bool:
        return False


class ElementInline(admin.TabularInline):
    model = Element
    can_delete = False
    extra = 0
    show_change_link = False
    fields = ('amount', 'name',)


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
    ordering = ('number',)
    list_filter = ('city',)
    fieldsets: list[tuple[str, object]] = [
        (
            'Внешние данные',
            {
                'fields':
                    (
                        'source',
                        'number',
                        'price',
                        'customers_name',
                        'customers_phone',
                        'city',

                    )
            },
        ),
        (
            'Внутренние данные', {
                'fields':
                    (
                        'status',
                        'date',
                        'delivery_price',
                        'delivery_position',
                        'order_comment',
                    ),
            },
        ),
    ]
    list_display = ('number', 'city', 'date', 'status')
    list_display_links = ('number', 'city', 'date', 'status')
    inlines = (ElementInline, StatusStoryInline)


@admin.register(CheckingOrder)
class CheckingOrderAdmin(admin.ModelAdmin):
    list_filter = ('city',)
    ordering = ('number',)
    fieldsets: list[tuple[str, object]] = [
        (
            'Внешние данные',
            {
                'fields':
                    (
                        'status',
                        'source',
                        'number',
                        'price',
                        'customers_name',
                        'customers_phone',
                        'city',

                    )
            },
        ),
        (
            'Внутренние данные', {
                'fields':
                    (
                        'date',
                        'delivery_price',
                        'order_comment',
                    ),
            },
        ),
    ]
    readonly_fields = ('status',
                       'source',
                       'number',
                       'price',
                       'customers_name',
                       'customers_phone',
                       'city',
                       'date',
                       'delivery_price',
                       'order_comment',
                       )
    list_display = ('number', 'city', 'date', 'status')
    list_display_links = ('number', 'city', 'date', 'status')
    inlines = (ElementViewInline, StatusStoryInline)
    actions = ('change_status', 'return_order')

    def has_add_permission(self, request: WSGIRequest) -> bool:
        return False

    def has_delete_permission(self, request: WSGIRequest, obj: Order | None = None) -> bool:
        return False

    @admin.action(description='вернуть заказ(ы)')
    def return_order(
            modeladmin,
            request: WSGIRequest,
            queryset: QuerySet[Order]
    ) -> HttpResponseRedirect | HttpResponse:
        forms = []

        print(request.POST)

        if 'apply' in request.POST:
            count = 0
            for element in zip(request.POST.getlist('message'), request.POST.getlist('element')):
                oreder = Order.objects.get(pk=element[-1])
                print(oreder.__dict__)
                oreder.status = Status.RETURN
                oreder.save()
                status_story = StatusStory(status=Status.RETURN, order=oreder, order_comment=element[0])
                status_story.save()
                count += 1
            modeladmin.message_user(request, f"Статус {Status.RETURN.name} применена к {count} товарам.")
            return HttpResponseRedirect(request.get_full_path())

        if not forms:
            print(request.POST)
            for element in request.POST.getlist('_selected_action'):
                forms.append([ChangeStatusForm(initial={'_selected_action': element}), element])

        return render(request, 'change_status.html',
                      {'items': queryset, 'forms': forms, 'title': u'Изменения статусов', 'action': 'return_order'})

    def get_queryset(self, request: WSGIRequest) -> QuerySet[Order]:
        qs = self.model._default_manager.get_queryset().filter(status=Status.CHECKING)
        ordering = self.get_ordering(request)
        if ordering:
            qs = qs.order_by(*ordering)
        return qs

    @admin.action(description='Передать заказ(ы) на проверку логистического соответствия')
    def change_status(
            modeladmin,
            request: WSGIRequest,
            queryset: QuerySet[Order]
    ) -> HttpResponseRedirect | HttpResponse:
        forms = []

        print(request.POST)

        if 'apply' in request.POST:
            count = 0
            for element in zip(request.POST.getlist('message'), request.POST.getlist('element')):
                print(request.POST.__dict__)
                oreder = Order.objects.get(pk=element[-1])
                print(oreder.__dict__)
                oreder.status = Status.COMPLIANCE
                oreder.save()
                status_story = StatusStory(status=Status.COMPLIANCE, order=oreder, order_comment=element[0])
                status_story.save()
                count += 1
            modeladmin.message_user(request, f"Статус {Status.CHECKING.name} применена к {count} товарам.")
            return HttpResponseRedirect(request.get_full_path())

        if not forms:
            print(request.POST)
            for element in request.POST.getlist('_selected_action'):
                forms.append([ChangeStatusForm(initial={'_selected_action': element}), element])

        return render(request, 'change_status.html',
                      {'items': queryset, 'forms': forms, 'title': u'Изменения статусов', 'action': 'change_status'})


@admin.register(ComplianceOrder)
class ComplianceOrderAdmin(admin.ModelAdmin):
    list_filter = ('city',)
    ordering = ('number',)
    fieldsets: list[tuple[str, object]] = [
        (
            'Внешние данные',
            {
                'fields':
                    (
                        'status',
                        'source',
                        'number',
                        'price',
                        'customers_name',
                        'customers_phone',
                        'city',

                    )
            },
        ),
        (
            'Внутренние данные', {
                'fields':
                    (
                        'date',
                        'delivery_price',
                        'delivery_position',
                        'order_comment',
                    ),
            },
        ),
    ]
    readonly_fields = ('status',
                       'source',
                       'number',
                       'price',
                       'customers_name',
                       'customers_phone',
                       'city',
                       'date',
                       'delivery_price',
                       'order_comment',
                       )
    list_display = ('number', 'city', 'date', 'status')
    list_display_links = ('number', 'city', 'date', 'status')
    inlines = (ElementViewInline, StatusStoryInline)
    actions = ('change_status', 'return_order')

    def has_add_permission(self, request: WSGIRequest) -> bool:
        return False

    def has_delete_permission(self, request: WSGIRequest, obj: Order | None = None) -> bool:
        return False

    @admin.action(description='вернуть заказ(ы)')
    def return_order(
            modeladmin,
            request: WSGIRequest,
            queryset: QuerySet[Order]
    ) -> HttpResponseRedirect | HttpResponse:
        forms = []

        print(request.POST)

        if 'apply' in request.POST:
            count = 0
            for element in zip(request.POST.getlist('message'), request.POST.getlist('element')):
                oreder = Order.objects.get(pk=element[-1])
                print(oreder.__dict__)
                oreder.status = Status.RETURN
                oreder.save()
                status_story = StatusStory(status=Status.RETURN, order=oreder, order_comment=element[0])
                status_story.save()
                count += 1
            modeladmin.message_user(request, f"Статус {Status.RETURN.name} применена к {count} товарам.")
            return HttpResponseRedirect(request.get_full_path())

        if not forms:
            print(request.POST)
            for element in request.POST.getlist('_selected_action'):
                forms.append([ChangeStatusForm(initial={'_selected_action': element}), element])

        return render(request, 'change_status.html',
                      {'items': queryset, 'forms': forms, 'title': u'Изменения статусов', 'action': 'return_order'})

    def get_queryset(self, request: WSGIRequest) -> QuerySet[Order]:
        qs = self.model._default_manager.get_queryset().filter(status=Status.COMPLIANCE)
        ordering = self.get_ordering(request)
        if ordering:
            qs = qs.order_by(*ordering)
        return qs

    @admin.action(description='Передать заказ(ы) на погрузку')
    def change_status(
            modeladmin,
            request: WSGIRequest,
            queryset: QuerySet[Order]
    ) -> HttpResponseRedirect | HttpResponse:
        forms = []

        print(request.POST)

        if 'apply' in request.POST:
            count = 0
            for element in zip(request.POST.getlist('message'), request.POST.getlist('element')):
                oreder = Order.objects.get(pk=element[-1])
                print(oreder.__dict__)
                oreder.status = Status.LOADING
                oreder.save()
                status_story = StatusStory(status=Status.LOADING, order=oreder, order_comment=element[0])
                status_story.save()
                count += 1
            modeladmin.message_user(request, f"Статус {Status.LOADING.name} применена к {count} товарам.")
            return HttpResponseRedirect(request.get_full_path())

        if not forms:
            print(request.POST)
            for element in request.POST.getlist('_selected_action'):
                forms.append([ChangeStatusForm(initial={'_selected_action': element}), element])

        return render(request, 'change_status.html',
                      {'items': queryset, 'forms': forms, 'title': u'Изменения статусов', 'action': 'change_status'})


@admin.register(LoadingOrder)
class LoadingOrderAdmin(admin.ModelAdmin):
    list_filter = ('city',)
    ordering = ('number',)
    fieldsets: list[tuple[str, object]] = [
        (
            'Внешние данные',
            {
                'fields':
                    (
                        'status',
                        'source',
                        'number',
                        'price',
                        'customers_name',
                        'customers_phone',
                        'city',

                    )
            },
        ),
        (
            'Внутренние данные', {
                'fields':
                    (
                        'date',
                        'delivery_price',
                        'delivery_position',
                        'order_comment',
                    ),
            },
        ),
    ]
    readonly_fields = ('status',
                       'source',
                       'number',
                       'price',
                       'customers_name',
                       'customers_phone',
                       'city',
                       'date',
                       'delivery_price',
                       'order_comment',
                       )
    list_display = ('number', 'delivery_position', 'city', 'date', 'status')
    list_display_links = ('number', 'city', 'date', 'status')
    inlines = (ElementViewInline, StatusStoryInline)
    actions = ('return_order',)

    def has_add_permission(self, request: WSGIRequest) -> bool:
        return False

    def has_delete_permission(self, request: WSGIRequest, obj: Order | None = None) -> bool:
        return False

    @admin.action(description='вернуть заказ(ы)')
    def return_order(
            modeladmin,
            request: WSGIRequest,
            queryset: QuerySet[Order]
    ) -> HttpResponseRedirect | HttpResponse:
        forms = []

        print(request.POST)

        if 'apply' in request.POST:
            count = 0
            for element in zip(request.POST.getlist('message'), request.POST.getlist('element')):
                oreder = Order.objects.get(pk=element[-1])
                print(oreder.__dict__)
                oreder.status = Status.RETURN
                oreder.save()
                status_story = StatusStory(status=Status.RETURN, order=oreder, order_comment=element[0])
                status_story.save()
                count += 1
            modeladmin.message_user(request, f"Статус {Status.RETURN.name} применена к {count} товарам.")
            return HttpResponseRedirect(request.get_full_path())

        if not forms:
            print(request.POST)
            for element in request.POST.getlist('_selected_action'):
                forms.append([ChangeStatusForm(initial={'_selected_action': element}), element])

        return render(request, 'change_status.html',
                      {'items': queryset, 'forms': forms, 'title': u'Изменения статусов', 'action': 'return_order'})

    def get_queryset(self, request: WSGIRequest) -> QuerySet[Order]:
        qs = self.model._default_manager.get_queryset().filter(status=Status.LOADING)
        ordering = self.get_ordering(request)
        if ordering:
            qs = qs.order_by(*ordering)
        return qs


@admin.register(ReturnOrder)
class ReturnOrderAdmin(admin.ModelAdmin):
    list_filter = ('city',)
    ordering = ('number',)
    fieldsets: list[tuple[str, object]] = [
        (
            'Внешние данные',
            {
                'fields':
                    (
                        'status',
                        'source',
                        'number',
                        'price',
                        'customers_name',
                        'customers_phone',
                        'city',

                    )
            },
        ),
        (
            'Внутренние данные', {
                'fields':
                    (
                        'date',
                        'delivery_price',
                        'delivery_position',
                        'order_comment',
                    ),
            },
        ),
    ]
    readonly_fields = ('status',
                       'source',
                       'number',
                       'price',
                       'customers_name',
                       'customers_phone',
                       'city',
                       'date',
                       'delivery_price',
                       'delivery_position',
                       'order_comment',
                       )
    list_display = ('number', 'city', 'date', 'status')
    list_display_links = ('number', 'city', 'date', 'status')
    inlines = (ElementViewInline, StatusStoryInline)

    def has_add_permission(self, request: WSGIRequest) -> bool:
        return False

    def get_queryset(self, request: WSGIRequest) -> QuerySet[Order]:
        qs = self.model._default_manager.get_queryset().filter(status=Status.RETURN)
        ordering = self.get_ordering(request)
        if ordering:
            qs = qs.order_by(*ordering)
        return qs
