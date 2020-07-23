from django.conf import settings
from django.contrib import messages
from django.shortcuts import redirect
from django.urls import reverse
from django.utils import safestring
from django.utils.translation import gettext as _


class ItouCurrentOrganizationMiddleware:
    """
    Store the ID of the current prescriber organization or employer structure in session.
    https://docs.djangoproject.com/en/dev/topics/http/middleware/#writing-your-own-middleware
    """

    def __init__(self, get_response):
        self.get_response = get_response

    def __call__(self, request):

        # Before the view is called.

        user = request.user

        if user.is_authenticated:

            # Note that the case of a siae user without any siae attached actually happens
            # during the siae invitation process, thus we have filter out this edge case here.
            if user.is_siae_staff and user.siae_set.exists():
                current_siae_pk = request.session.get(settings.ITOU_SESSION_CURRENT_SIAE_KEY)
                if not user.siae_set(manager="active").filter(pk=current_siae_pk).exists():
                    first_active_siae = user.siae_set(manager="active").first()
                    if first_active_siae:
                        request.session[settings.ITOU_SESSION_CURRENT_SIAE_KEY] = first_active_siae.pk
                    elif request.path != reverse("account_logout"):
                        # SIAE user has no active SIAE and thus must not be able to login.
                        message = (
                            "Nous sommes désolés, votre compte n'est "
                            "malheureusement plus actif car la ou les "
                            "structures associées ne sont plus "
                            "conventionnées. Nous espérons cependant "
                            "avoir l'occasion de vous accueillir de "
                            "nouveau sur la Plateforme."
                        )
                        message = safestring.mark_safe(message)
                        messages.warning(request, _(message))
                        return redirect("account_logout")

            elif user.is_prescriber and user.prescriberorganization_set.exists():
                request.session[
                    settings.ITOU_SESSION_CURRENT_PRESCRIBER_ORG_KEY
                ] = user.prescriberorganization_set.first().pk

        response = self.get_response(request)

        # After the view is called.

        return response
