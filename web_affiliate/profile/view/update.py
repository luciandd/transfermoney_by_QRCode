from django.shortcuts import render, redirect
from django.views.generic.base import TemplateView
from authentications.models import Profile


# Create your views here.
class UserUpdate(TemplateView):
	template_name = "update.html"

	def get(self, request, *args, **kwargs):
		context = super(UserUpdate, self).get_context_data(**kwargs)
		print("Get profile detail")
		profile = Profile.objects.get(user=self.request.user)
		context['name'] = profile.user.first_name
		context['mobile'] = profile.user.username
		context['email'] = profile.user.email
		return render(request, self.template_name, context)

	def post(self, request, *args, **kwargs):
		profile = Profile.objects.get(user=self.request.user)
		profile.user.first_name = request.POST.get('name')
		profile.user.username = request.POST.get('mobile')
		profile.user.email = request.POST.get('email')

		profile.user.save()
		return redirect("profile:detail")
