from django.contrib import admin
from django.contrib import messages

# from utils import send_mail

from .models import (
    EmailList,
    EmailContent,
    Email,
    EmailCategory,
    InjectedEmailContent,
)


class EmailAdmin(admin.ModelAdmin):
    list_display = ('get_subject', 'created_date', 'is_sent')
    ordering = ['created_date']
    exclude = ['is_sent', 'created_date']
    actions = ['send_mail']

    def get_subject(self, obj):
        return obj.content.subject

    def send_mail(self, request, queryset):
        responses = []
        for mail in queryset.all():
            if not mail.is_sent:
                resp = mail.send()
                responses.append(resp)

        if len(set(responses)) == 1 and responses[0] == 200:
            messages.success(request, "Email(s) sent!")
        else:
            messages.warning(request, "Something might have gone wrong.")


class EmailListAdmin(admin.ModelAdmin):
    list_display = ('first_name', 'last_name', 'email')
    ordering = ['first_name']
    exclude = ['created_date']


class EmailContentAdmin(admin.ModelAdmin):
    list_display = ('subject', 'is_html', 'created_date')
    ordering = ['created_date']
    exclude = ['created_date']


class InjectedEmailContentAdmin(admin.ModelAdmin):
    list_display = ('subject', 'created_date')
    ordering = ['created_date']
    exclude = ['created_date']
    readonly_fields = ['subject', 'body', 'created_date']

    def has_add_permission(self, request, obj=None):
        return False

    def has_delete_permission(self, request, obj=None):
        return False

# Register your models here.
admin.site.register(EmailList, EmailListAdmin)
admin.site.register(EmailContent, EmailContentAdmin)
admin.site.register(Email, EmailAdmin)
admin.site.register(EmailCategory)
admin.site.register(InjectedEmailContent, InjectedEmailContentAdmin)

admin.site.site_header = "Email Manager"
admin.site.site_title = "Email Manager"

