from django.db import models
from django.contrib.postgres.fields import JSONField
from django.utils import timezone
from django.core import serializers

from celery.result import AsyncResult

from .utils import inject_to_content, send_mail


class EmailCategory(models.Model):
    name = models.CharField(max_length=100)
    mailing_list = models.ManyToManyField("EmailList", related_name="user")
    created_date = models.DateTimeField(auto_now_add=True)

    class Meta:
        verbose_name = "My Category"
        verbose_name_plural = "My Categories"

    def __str__(self):
        return f"{self.name}"

    def __repr__(self):
        return f"EmailCategory({self.name})"


class EmailList(models.Model):
    first_name = models.CharField(max_length=100)
    last_name = models.CharField(max_length=200)
    email = models.EmailField()
    sub_date = models.DateField(auto_now_add=True)
    is_subscribed = models.BooleanField(default=True)
    created_date = models.DateTimeField(default=timezone.now)

    class Meta:
        verbose_name = "My List"
        verbose_name_plural = "My Lists"

    def __str__(self):
        return f"{self.first_name} {self.last_name}"

    def __repr__(self):
        return f"EmailList({self.first_name}, {self.last_name}, {self.email})"


class EmailContent(models.Model):
    subject = models.CharField(max_length=300)
    body = models.TextField()
    variables = JSONField()
    is_html = models.BooleanField(default=True)
    created_date = models.DateTimeField(default=timezone.now)

    class Meta:
        verbose_name = "My Mail Content"
        verbose_name_plural = "My Mail Contents"

    def __str__(self):
        return f"{self.subject}"

    def __repr__(self):
        return f"EmailContent({self.subject})"

    def save(self, *args, **kwargs):
        super(EmailContent, self).save(*args, **kwargs)

        subject_ctx = self.variables.get("subject", {})
        body_ctx = self.variables.get("body", {})

        subject = inject_to_content(self.subject, subject_ctx)
        body = inject_to_content(self.body, body_ctx)

        injected_mail = InjectedEmailContent(subject=subject, body=body, content=self)
        injected_mail.save()


class InjectedEmailContent(models.Model):
    subject = models.CharField(max_length=200)
    body = models.TextField()
    content = models.ForeignKey(
        "EmailContent", related_name="content", null=True, on_delete=models.SET_NULL
    )
    created_date = models.DateTimeField(default=timezone.now)

    class Meta:
        verbose_name = "My Injected Email"
        verbose_name_plural = "My Injected Emails"

    def __str__(self):
        return f"{self.subject}"

    def __repr__(self):
        return f"InjectedEmailContent({self.subject}, {self.created_date})"


from .serializers import EmailContentSerializer, InjectedEmailContentSerializer


class Email(models.Model):
    content = models.ForeignKey(
        "InjectedEmailContent",
        related_name="mail_content",
        null=True,
        on_delete=models.SET_NULL,
    )
    email_list = models.ManyToManyField("EmailCategory")
    is_sent = models.BooleanField(default=False)
    created_date = models.DateTimeField(default=timezone.now)
    is_scheduled = models.BooleanField(default=False)
    send_date = models.DateTimeField(default=timezone.now)

    class Meta:
        verbose_name = "My Email"
        verbose_name_plural = "My Emails"

    def __str__(self):
        return f"{self.content.subject}"

    def __unicode__(self):
        return f"Email({self.content.subject}, {self.created_date})"

    def get_list_of_emails(self):
        categories = [cat for cat in self.email_list.all()]
        emails = []
        for cat in categories:
            for email in cat.mailing_list.all():
                emails.append(email)
        return emails

    def send(self):
        payload = InjectedEmailContentSerializer(self.content)
        emails = [e.email for e in self.get_list_of_emails()]

        if self.is_scheduled:
            task_id = send_mail.apply_async(
                args=(emails, payload.data, self.__class__.__name__, self.pk),
                eta=self.send_date,
            )
        else:
            print("HERE")
            task_id = send_mail.delay(
                emails, payload.data, self.__class__.__name__, self.pk
            )
        return (task_id.status, task_id.id)
