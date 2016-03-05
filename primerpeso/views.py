from django.shortcuts import render
from formtools.wizard.views import CookieWizardView
from django.utils.translation import ugettext as _
from django.shortcuts import render_to_response
from . import models


def about(request):
    return render(request, "primerpeso/about.jade", {'title': 'About'})


class SearchFormView(CookieWizardView):
    template_name="primerpeso/search_form.html"
    def done(self, form_list, **kwargs):
        combined = {}
        for form in form_list:
            combined.update(form.cleaned_data)
        search = models.OpportunitySearch(**combined)
        search.save()
        query = search.search()
        return render_to_response("primerpeso/search_results.html", {
            'title': _('Questionnaire Results'), # Preguntas
        })
