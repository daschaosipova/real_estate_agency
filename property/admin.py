from django.contrib import admin
from .models import Flat, Complaint, Owner


class OwnerInline(admin.TabularInline):
    model = Owner.flats.through
    raw_id_fields = ['owner']
    extra = 1

class FlatAdmin(admin.ModelAdmin):
    search_fields = ('flat_owners__owner','town', 'address',)
    readonly_fields = ('created_at',)
    inlines = [OwnerInline]
    list_display = [
        'address',
        'price',
        'new_building',
        'construction_year',
        'town',
        'get_owners_names', 
        'get_owners_phones',
    ]
    list_editable = ['new_building']
    list_filter = ['new_building', 'has_balcony', 'rooms_number']
    raw_id_fields = ['liked_by']

    def get_queryset(self, request):
        queryset = super().get_queryset(request)
        return queryset.prefetch_related('flat_owners')

    @admin.display(description='ФИО владельцев')
    def get_owners_names(self, obj):
        owners = obj.flat_owners.all()
        return ", ".join([owner.owner for owner in owners]) or "Нет владельца"

    @admin.display(description='Номера владельцев')
    def get_owners_phones(self, obj):
        owners = obj.flat_owners.all()
        phones = []
        for owner in owners:
            phone = str(owner.owner_pure_phone) if owner.owner_pure_phone else owner.owners_phonenumber
            phones.append(phone)
        return ", ".join(phones) or "—"

class ComplaintAdmin(admin.ModelAdmin):
    raw_id_fields = ['user', 'flat']

class OwnerAdmin(admin.ModelAdmin):
    raw_id_fields = ['flats']
    list_display = ['owner', 'owner_pure_phone']

admin.site.register(Flat, FlatAdmin)
admin.site.register(Complaint, ComplaintAdmin)
admin.site.register(Owner, OwnerAdmin)
