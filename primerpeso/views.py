import urllib
from django.shortcuts import render, redirect
from formtools.wizard.views import CookieWizardView
from django.views.generic.detail import DetailView
from django.utils.translation import ugettext as _
from django.core.urlresolvers import reverse
from django.shortcuts import render_to_response
from django.shortcuts import get_object_or_404
from . import models, forms


def about(request):
    return render(request, "primerpeso/about.jade", {'title': _('About')})


def home(request):
    return render(request, "primerpeso/home.jade", {'title': _('Home')})


class SearchFormView(CookieWizardView):
    template_name = "primerpeso/search_form.html"

    def done(self, form_list, **kwargs):
        combined = {}
        for form in form_list:
            combined.update(form.cleaned_data)
        search = models.OpportunitySearch(**combined)
        search.save()
        url = reverse('search-results', args=[search.pk, ])
        return redirect(url)


def search_results(request, pk):
    try:
        search = models.OpportunitySearch.objects.get(pk=pk)
    except models.OpportunitySearch.DoesNotExist:
        return redirect(reverse('search-form'))
    else:
        segmented_opps = list(search.segment_search().items())
        return render_to_response("primerpeso/search_results.html", {
            'title': _('Questionnaire Results'),  # Preguntas
            'segmented_opps': segmented_opps,
        })


class OpportunityDetailView(DetailView):
    model = models.Opportunity
