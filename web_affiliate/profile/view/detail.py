from django.shortcuts import render
from django.contrib.auth.decorators import login_required
from django.views.generic.base import TemplateView
from authentications.models import Profile

# Create your views here.
class UserProfile(TemplateView):
	template_name = "detail.html"

	def get(self, request, *args, **kwargs):
		context = super(UserProfile, self).get_context_data(**kwargs)
		profile = Profile.objects.get(user=self.request.user)
		context['name'] = profile.user.first_name
		context['mobile'] = profile.user.username
		context['email'] = profile.user.email

		return render(request, self.template_name, context)