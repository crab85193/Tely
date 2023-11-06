from ..template.admin import AdminTemplateView

class Dashboard(AdminTemplateView):
    template_name = 'main_app/dev/index.html'

class PagesBlank(AdminTemplateView):
    template_name = 'main_app/dev/pages-blank.html'

class PagesContact(AdminTemplateView):
    template_name = 'main_app/dev/pages-contact.html'

class PagesError404(AdminTemplateView):
    template_name = 'main_app/dev/pages-error-404.html'

class PagesFAQ(AdminTemplateView):
    template_name = 'main_app/dev/pages-faq.html'

class PagesLogin(AdminTemplateView):
    template_name = 'main_app/dev/pages-login.html'

class PagesRegister(AdminTemplateView):
    template_name = 'main_app/dev/pages-register.html'

class UsersProfile(AdminTemplateView):
    template_name = 'main_app/dev/users-profile.html'
