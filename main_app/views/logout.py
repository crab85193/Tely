from django.contrib.auth.views import LogoutView

class Logout(LogoutView):
    template_name = 'main_app/login/logout.html'