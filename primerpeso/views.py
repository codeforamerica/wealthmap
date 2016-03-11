import urllib
from django.shortcuts import render, redirect
from formtools.wizard.views import CookieWizardView
from django.utils.translation import ugettext as _
from django.core.urlresolvers import reverse
from django.shortcuts import render_to_response
from . import models, forms


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
        url = reverse('search-results', args=[search.pk,])
        return redirect(url)


def search_results(request, pk):
    try:
        search = models.OpportunitySearch.objects.get(pk=pk)
    except models.OpportunitySearch.DoesNotExist:
        return redirect(reverse('search-form'))
    else:
        return render_to_response("primerpeso/search_results.html", {
            'title': _('Questionnaire Results'),  # Preguntas
        })
