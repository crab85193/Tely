from ..template.admin import AdminTemplateView

class TablesData(AdminTemplateView):
    template_name = 'main_app/dev/tables-data.html'

class TablesGeneral(AdminTemplateView):
    template_name = 'main_app/dev/tables-general.html'
