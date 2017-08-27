from django.contrib import admin

from .models import Invite


class InviteAdmin(admin.ModelAdmin):
    list_display = ('code', 'expired')
    raw_id_fields = ('user', )

    def save_model(self, request, obj, form, change):
        if not change:
            obj.user = request.user
        super(InviteAdmin, self).save_model(request, obj, form, change)


admin.site.register(Invite, InviteAdmin)
