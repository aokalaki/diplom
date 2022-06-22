from django.contrib import admin

from housing.models import Advertisement


@admin.register(Advertisement)
class AdvertisementAdmin(admin.ModelAdmin):
    list_display = ('no', 'address', 'rooms', 'duration', 'price', 'conditions', 'date')

    @admin.display(ordering='pk', description='ID')
    def no(self, obj):
        return f'№{obj.pk:06d}'
