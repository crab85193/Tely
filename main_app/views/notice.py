from django.views.generic import TemplateView, ListView, DetailView
from django.contrib.auth.mixins import LoginRequiredMixin
from django.http import HttpResponseRedirect
from ..models.notice import Notice, UserNotice

class NoticeListView(LoginRequiredMixin, ListView):
    template_name = "main_app/notice/notice-list.html"
    model = Notice
    context_object_name = "objects"
    ordering = "-datetime"

class NoticeDetailView(LoginRequiredMixin, DetailView):
    template_name = "main_app/notice/notice-detail.html"
    model = Notice
    context_object_name = "object"

    def get_context_data(self, **kwargs):
        context =  super().get_context_data(**kwargs)

        context["menu"] = Notice.objects.all().order_by("-datetime")

        return context

class UserNoticeListView(LoginRequiredMixin, TemplateView):
    pass

class UserNoticeDetailView(LoginRequiredMixin, TemplateView):
    pass