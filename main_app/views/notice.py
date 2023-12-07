from typing import Any
from django import http
from django.views.generic import TemplateView, ListView, DetailView
from django.contrib.auth.mixins import LoginRequiredMixin
from django.http import HttpResponseRedirect
from django.urls import reverse
from django.shortcuts import redirect
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
    template_name = "main_app/notice/user-notice-list.html"

    def get_context_data(self, **kwargs):
        context =  super().get_context_data(**kwargs)

        context["objects"] = UserNotice.objects.filter(user=self.request.user).order_by("-datetime")

        return context
    

class UserNoticeDetailView(LoginRequiredMixin, DetailView):
    template_name = "main_app/notice/user-notice-detail.html"
    model = UserNotice
    context_object_name = "object"

    def get(self, request, *args, **kwargs):
        obj = UserNotice.objects.get(id=self.kwargs['pk'])

        obj.is_check = True
        obj.save()

        if obj.url:
            return redirect(obj.url)
        else:
            return super().get(request, *args, **kwargs)
        
    def get_context_data(self, **kwargs):
        context =  super().get_context_data(**kwargs)

        context["menu"] = UserNotice.objects.filter(user=self.request.user).order_by("-datetime")

        return context
        
    
