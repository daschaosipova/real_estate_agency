from django.contrib import admin
from .models import Flat, Complaint, Owner


class FlatAdmin(admin.ModelAdmin):
    search_fields = ('owner','town', 'address',)
    readonly_fields = ('created_at',)
    list_display = [
        'town',
        'address',
        'price',
        'get_owners_names', 
        'get_owners_phones',
        'new_building',
        'construction_year',
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
