from secrets import choice
from string import digits
from datetime import timedelta

from django.shortcuts import redirect, get_object_or_404
from django.contrib.auth.mixins import LoginRequiredMixin
from django.core.mail import send_mail
from django.template.loader import render_to_string
from django.views import generic
from django.utils import timezone
from django.conf import settings

from .forms import NewTransferForm, ConfirmTransferForm
from .models import Transfer, TransferToConfirm


class CreateView(LoginRequiredMixin, generic.FormView):
    form_class = NewTransferForm
    template_name = "transfers/new.html"

    def form_valid(self, form):
        transfer = form.save(commit=False)
        transfer.user = self.request.user
        transfer.auth_code = CreateView.random_code()
        transfer.save()

        msg_html = render_to_string("transfers/email.html", {"transfer": transfer})

        send_mail(
            subject="Transfer Authorisation",
            message=msg_html,
            from_email=None,
            recipient_list=[self.request.user.email],
            html_message=msg_html,
        )

        return redirect("transfers:confirm", transfer.id)

    @staticmethod
    def random_code():
        return "".join(choice(digits) for _ in range(6))


class ConfirmView(LoginRequiredMixin, generic.FormView):
    form_class = ConfirmTransferForm
    template_name = "transfers/confirm.html"

    def get_form_kwargs(self):
        kwargs = super(ConfirmView, self).get_form_kwargs()
        kwargs["confirm_id"] = self.kwargs["confirm_id"]
        return kwargs

    def get_context_data(self, **kwargs):
        context = super(ConfirmView, self).get_context_data(**kwargs)
        context["transfer"] = self.get_toconfirm_or_404()
        return context

    def form_valid(self, _):
        confirmed = self.get_toconfirm_or_404()
        transfer = Transfer.objects.create(
            title=confirmed.title,
            recipient=confirmed.recipient,
            date=confirmed.date,
            amount=confirmed.amount,
            iban=confirmed.iban,
            user=confirmed.user,
        )
        transfer.save()
        confirmed.delete()
        return redirect("transfers:details", transfer.id)

    def get_toconfirm_or_404(self):
        return get_object_or_404(
            TransferToConfirm,
            pk=self.kwargs["confirm_id"],
            user=self.request.user,
            created__gte=timezone.now()
            - timedelta(seconds=settings.TRANSFER_CONFIRM_TIME),
        )


class RejectView(LoginRequiredMixin, generic.TemplateView):
    template_name = "transfers/reject.html"

    def post(self, _, reject_id):
        transfer = get_object_or_404(
            TransferToConfirm, pk=reject_id, user=self.request.user
        )
        transfer.delete()
        return self.render_to_response({"transfer": transfer})


class DetailView(LoginRequiredMixin, generic.DetailView):
    model = Transfer
    template_name = "transfers/details.html"

    def get_queryset(self):
        return Transfer.objects.filter(user=self.request.user)


class ListView(LoginRequiredMixin, generic.ListView):
    model = Transfer
    template_name = "transfers/list.html"

    def get_queryset(self):
        return Transfer.objects.filter(user=self.request.user)
