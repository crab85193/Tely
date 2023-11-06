from ..template.admin import AdminTemplateView

class ChartsApexChartsView(AdminTemplateView):
    template_name = 'main_app/dev/charts-apexcharts.html'

class ChartsChartjsView(AdminTemplateView):
    template_name = 'main_app/dev/charts-chartjs.html'

class ChartsEchartsView(AdminTemplateView):
    template_name = 'main_app/dev/charts-echarts.html'
