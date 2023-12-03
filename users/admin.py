from django.contrib import admin
from users.models import Client, User


@admin.register(Client)
class ClientAdmin(admin.ModelAdmin):
    list_display = ('email', 'full_name', 'comment')
    search_fields = ('email', 'full_name', 'comment')


admin.site.register(User)
