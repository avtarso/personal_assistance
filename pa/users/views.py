from django.conf import settings
from django.contrib import messages
from django.contrib.auth import authenticate, get_user_model, login, logout
from django.contrib.auth.decorators import login_required
from django.contrib.auth.forms import AuthenticationForm
from django.contrib.auth.models import User
from django.contrib.auth.tokens import default_token_generator
from django.contrib.auth.views import PasswordResetView
from django.contrib.messages.views import SuccessMessageMixin
from django.contrib.sites.shortcuts import get_current_site
from django.core.mail import EmailMessage, EmailMultiAlternatives
from django.http import HttpResponse
from django.shortcuts import redirect, render
from django.template.loader import render_to_string
from django.urls import reverse_lazy
from django.utils.encoding import force_bytes, force_str
from django.utils.http import urlsafe_base64_decode, urlsafe_base64_encode
from django.views.generic import View
from django.views.generic.base import TemplateView
from django.views.generic.edit import FormView

from .forms import RegistrationForm

# from django.utils.translation import gettext_lazy as _


User = get_user_model()


def users_main(request):
    return render(request, "users/users.html")


def login_view(request):
    if request.method == "POST":
        form = AuthenticationForm(request, data=request.POST)
        if form.is_valid():
            username = form.cleaned_data.get("username")
            password = form.cleaned_data.get("password")
            user = authenticate(request, username=username, password=password)
            if user is not None:
                login(request, user)
                return redirect("users:profile")
    else:
        form = AuthenticationForm()
    return render(request, "users/login.html", {"form": form})


def register(request):
    if request.method == "POST":
        form = RegistrationForm(request.POST)
        if form.is_valid():
            user = form.save(commit=False)
            user.is_active = False
            user.save()

            # Send confirmation email
            current_site = get_current_site(request)
            mail_subject = "Activate your account"
            token = default_token_generator.make_token(user)
            uid = urlsafe_base64_encode(force_bytes(user.pk))
            message = render_to_string(
                "users/acc_active_email.html",
                {
                    "user": user,
                    "domain": current_site.domain,
                    "protocol": "https" if request.is_secure() else "http",
                    "uid": uid,
                    "token": token,
                },
            )
            email = EmailMessage(mail_subject, message, to=[user.email])
            email.send()
            return redirect("users:email_verification_sent")
    else:
        form = RegistrationForm()
    return render(request, "users/register.html", {"form": form})


@login_required
def profile(request):
    return render(request, "users/profile.html")


def logout_view(request):
    logout(request)
    return redirect("users:login")


def activate(request, uidb64, token):
    try:
        uid = force_str(urlsafe_base64_decode(uidb64))
        user = User.objects.get(pk=uid)
    except (TypeError, ValueError, OverflowError, User.DoesNotExist):
        user = None

    if user is not None and default_token_generator.check_token(user, token):
        user.is_active = True
        user.save()
        login(request, user)
        return redirect("activation_success")
    else:
        return HttpResponse("Activation link is invalid!")


def email_verification_sent(request):
    return render(request, "users/email_verification_sent.html")


def activation_success(request):
    return render(request, "users/activation_success.html")


class ResetPasswordView(SuccessMessageMixin, PasswordResetView):
    template_name = "users/password_reset.html"
    email_template_name = "users/password_reset_email.html"
    html_email_template_name = "users/password_reset_email.html"
    success_url = reverse_lazy("users:password_reset_done")
    success_message = (
        "An email with instructions to reset your password has been sent to %(email)s."
    )
    subject_template_name = "users/password_reset_subject.txt"


class EmailVerificationSentView(TemplateView):
    template_name = "users/email_verification_sent.html"


class ActivationSuccessView(TemplateView):
    template_name = "users/activation_success.html"


class ActivateAccountView(View):
    def get(self, request, uidb64, token, *args, **kwargs):
        try:
            uid = force_str(urlsafe_base64_decode(uidb64))
            user = User.objects.get(pk=uid)
        except (TypeError, ValueError, OverflowError, User.DoesNotExist):
            user = None

        if user is not None and default_token_generator.check_token(user, token):
            user.is_active = True
            user.save()
            messages.success(request, "Your account has been confirmed.")
            return redirect("users:activation_success")
        else:
            messages.warning(
                request,
                "The confirmation link was invalid, possibly because it has already been used.",
            )
            return redirect("users:email_verification_sent")


class RegisterView(FormView):
    template_name = "users/register.html"
    form_class = RegistrationForm
    success_url = reverse_lazy("users:email_verification_sent")

    def form_valid(self, form):
        user = form.save(commit=False)
        user.is_active = False
        user.save()

        current_site = self.request.get_host()
        protocol = "https" if self.request.is_secure() else "http"
        mail_subject = "Activate your account"
        token = default_token_generator.make_token(user)
        uid = urlsafe_base64_encode(force_bytes(user.pk))

        html_message = render_to_string(
            "users/acc_active_email.html",
            {
                "user": user,
                "domain": current_site,
                "uid": uid,
                "token": token,
                "protocol": protocol,
            },
        )

        email = EmailMultiAlternatives(
            subject=mail_subject,
            body="",
            from_email=settings.EMAIL_HOST_USER,
            to=[user.email],
        )

        email.attach_alternative(html_message, "text/html")
        email.send()

        return super().form_valid(form)
