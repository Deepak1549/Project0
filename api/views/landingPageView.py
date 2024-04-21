from django.views.generic import TemplateView
from django.shortcuts import render

class LandingPageView(TemplateView):
    template_name = "landing_page.html"
    def get(self, request):
        return render(request, self.template_name)