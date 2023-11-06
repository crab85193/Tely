from django.http import HttpResponseRedirect, Http404
from django.urls import reverse
from django.contrib.auth.mixins import LoginRequiredMixin
from django.views.generic import TemplateView, ListView, CreateView, DetailView, UpdateView, DeleteView

class AdminTemplateView(LoginRequiredMixin, TemplateView):
    def get(self, request):
        if not self.request.user.is_superuser:
            # return HttpResponseRedirect(reverse('main_app:forbidden')) 
            return Http404      
        return super().get(request)


class AdminListView(LoginRequiredMixin, ListView):
    def get(self, request):
        if not self.request.user.is_superuser:
            # return HttpResponseRedirect(reverse('main_app:forbidden')) 
            return Http404 
        return super().get(request)


class AdminCreateView(LoginRequiredMixin, CreateView):
    def get(self, request):
        if not self.request.user.is_superuser:
            # return HttpResponseRedirect(reverse('main_app:forbidden')) 
            return Http404 
        return super().get(request)


class AdminDetailView(LoginRequiredMixin, DetailView):
    def get(self, request, pk):
        if not self.request.user.is_superuser:
            # return HttpResponseRedirect(reverse('main_app:forbidden')) 
            return Http404 
        return super().get(request, pk)


class AdminUpdateView(LoginRequiredMixin, UpdateView):
    def get(self, request, pk):
        if not self.request.user.is_superuser:
            # return HttpResponseRedirect(reverse('main_app:forbidden')) 
            return Http404 
        return super().get(request, pk)
    

class AdminDeleteView(LoginRequiredMixin, DeleteView):
    def get(self, request, pk):
        if not self.request.user.is_superuser:
            # return HttpResponseRedirect(reverse('main_app:forbidden')) 
            return Http404 
        return super().get(request, pk)
    