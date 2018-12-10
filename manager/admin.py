from django.contrib import admin
from django.contrib import messages

from celery.result import AsyncResult

from .models import EmailList, EmailContent, Email, EmailCategory, InjectedEmailContent


class EmailAdmin(admin.ModelAdmin):
    list_display = ("get_subject", "created_date", "is_sent", "is_scheduled")
    ordering = ("created_date",)
    exclude = ("is_sent", "created_date")
    actions = ("send_mail",)

    def get_subject(self, obj):
        return obj.content.subject

    def send_mail(self, request, queryset):
        for mail in queryset.all():
            if not mail.is_sent:
                resp = mail.send()
                self.notify_message(request, AsyncResult(resp[1]))
            else:
                messages.warning(request, "Email already sent.")
                return

    def notify_message(self, request, state):
        if state.state == "FAILURE":
            messages.error(request, "Failed sending email(s).")
        if state.state == "SUCCESS":
            messages.success(request, "Email(s) was sent!")
        if state.state == "STARTED":
            messages.info(request, "Email(s) sent!")
        if state.state == "PENDING":
            messages.warning(request, "Email(s) are queued.")

    def save_model(self, request, obj, form, change):
        super(EmailAdmin, self).save_model(request, obj, form, change)

        if obj.is_scheduled and not obj.is_sent:
            obj.send()


class EmailListAdmin(admin.ModelAdmin):
    list_display = ("first_name", "last_name", "email")
    ordering = ("first_name",)
    exclude = ("created_date",)


class EmailContentAdmin(admin.ModelAdmin):
    list_display = ("subject", "is_html", "created_date")
    ordering = ("created_date",)
    exclude = ("created_date",)


class InjectedEmailContentAdmin(admin.ModelAdmin):
    list_display = ("subject", "created_date")
    ordering = ("created_date",)
    exclude = ("created_date",)
    readonly_fields = ("subject", "body", "created_date")

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
