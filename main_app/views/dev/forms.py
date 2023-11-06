from ..template.admin import AdminTemplateView

class FormsEditors(AdminTemplateView):
    template_name = 'main_app/dev/forms-editors.html'

class FormsElements(AdminTemplateView):
    template_name = 'main_app/dev/forms-elements.html'

class FormsLayouts(AdminTemplateView):
    template_name = 'main_app/dev/forms-layouts.html'

class FormsValidation(AdminTemplateView):
    template_name = 'main_app/dev/forms-validation.html'
