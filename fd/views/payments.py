from django.contrib.auth.mixins import LoginRequiredMixin
from django.views.generic import DetailView, FormView, TemplateView, View
from django.core.urlresolvers import reverse_lazy, reverse

class ConfirmFormView(LoginRequiredMixin, FormView):
    """A view used to confirm customers into a subscription plan."""

#    form_class = PlanForm
    template_name = "djstripe/confirm_form.html"
    success_url = reverse_lazy("djstripe:history")
    form_valid_message = "You are now subscribed!"

    def get(self, request, *args, **kwargs):
        """Override ConfirmFormView GET to perform extra validation.
        - Returns 404 when no plan exists.
        - Redirects to djstripe:subscribe when customer is already subscribed to this plan.
        """
        plan_id = self.kwargs['plan_id']

        if not Plan.objects.filter(id=plan_id).exists():
            return HttpResponseNotFound()

        customer, _created = Customer.get_or_create(
            subscriber=djstripe_settings.subscriber_request_callback(self.request)
        )

        if (customer.subscription and str(customer.subscription.plan.id) == plan_id and
                customer.subscription.is_valid()):
            message = "You already subscribed to this plan"
            messages.info(request, message, fail_silently=True)
            return redirect("djstripe:subscribe")

        return super(ConfirmFormView, self).get(request, *args, **kwargs)

    def get_context_data(self, *args, **kwargs):
        """Return ConfirmFormView's context with plan_id."""
        context = super(ConfirmFormView, self).get_context_data(**kwargs)
        context['plan'] = Plan.objects.get(id=self.kwargs['plan_id'])
        return context

    def post(self, request, *args, **kwargs):
        """
        Handle POST requests.
        Instantiates a form instance with the passed POST variables and
        then checks for validity.
        """
        form_class = self.get_form_class()
        form = self.get_form(form_class)
        if form.is_valid():
            try:
                customer, _created = Customer.get_or_create(
                    subscriber=djstripe_settings.subscriber_request_callback(self.request)
                )
                customer.add_card(self.request.POST.get("stripe_token"))
                customer.subscribe(form.cleaned_data["plan"])
            except StripeError as exc:
                form.add_error(None, str(exc))
                return self.form_invalid(form)
            return self.form_valid(form)
        else:
            return self.form_invalid(form)
