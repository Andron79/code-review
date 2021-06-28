from .models import UserProfile
from .forms import TransferForm

from django.views.generic.edit import FormView


class TransferView(FormView):
    form_class = TransferForm
    template_name = 'index.html'

    def post(self, request, *args, **kwargs):
        ctx = self.get_context_data(**kwargs)
        form = TransferForm(request.POST or None)
        if form.is_valid():
            ctx['op_result'] = UserProfile.transfer_money(**form.cleaned_data)
        return self.render_to_response(ctx)
