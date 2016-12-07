from django.contrib.auth.decorators import login_required
from django.forms import Textarea
from django.views.generic import DetailView
from django.views.generic import ListView, CreateView, UpdateView, TemplateView, DeleteView
from django.utils.decorators import method_decorator
from django.shortcuts import get_object_or_404, render, redirect
from django.core.urlresolvers import reverse, reverse_lazy
from django.http import HttpResponseRedirect

from .forms import NewsItemForm, EventForm
from datetime import datetime

from .models import NewsItem, Event


@method_decorator(login_required(login_url='login'), name='dispatch')
class PrivacyPolicyView(TemplateView):
    template_name = 'myFirstApp/privacy-policy.html'

    def get_context_data(self, **kwargs):
        context = super(PrivacyPolicyView, self).get_context_data(**kwargs)
        return context

""" Crear un CRUD para el model NewsItem con vistas basadas en funciones. Todas las URLs de estas vistas empezarán con el prefijo /v1/ """


def get_list_news_items(request):
    news_item = NewsItem.objects.all()
    return render(request, 'myFirstApp/news_item_list.html', {'news_items': news_item})


def get_news_item_detail(request, pk):
    news_item = get_object_or_404(NewsItem, pk=pk)
    return render(request, 'myFirstApp/news_item_detail.html', {'news_item': news_item})


def new_news_item(request):
    if request.method == "POST":
        form = NewsItemForm(request.POST)
        if form.is_valid():
            news_item = form.save(commit=False)
            news_item.publish_date = datetime.now()
            news_item.save()
            return redirect('news_item_detail', pk=news_item.pk)

    else:
        form = NewsItemForm()

    return render(request, 'myFirstApp/news_item_edit.html', {'form': form})


def news_item_edit(request, pk):
    news_item = get_object_or_404(NewsItem, pk=pk)
    if request.method == "POST":
        form = NewsItemForm(request.POST, instance=news_item)
        if form.is_valid():
            form.save()
            return redirect('news_item_detail', pk=news_item.pk)
    else:
        form = NewsItemForm(instance=news_item)
    return render(request, 'myFirstApp/news_item_edit.html', {'form': form})


def news_item_delete(request, pk):
    news_item = get_object_or_404(NewsItem, pk=pk)
    news_item.delete()
    return redirect('news_item_list')

""" Crear un CRUD para el model NewsItem con vistas basadas en clases. Todas las URLs de estas vistas empezarán con el prefijo /v1/ """


class EventList(ListView):
    model = Event
    template_name = 'myFirstApp/events_list.html'
    context_object_name = 'events'


class EventDetail(DetailView):
    model = Event
    template_name = 'myFirstApp/event_detail.html'
    context_object_name = 'event'


class EventCreate(CreateView):
    model = Event
    form_class = EventForm
    template_name = 'myFirstApp/event_edit.html'
    success_url = reverse_lazy('event_list')


class EventUpdate(UpdateView):
    model = Event
    template_name = 'myFirstApp/event_edit.html'
    fields = '__all__'
    success_url = reverse_lazy('event_list')


class EventDelete(DeleteView):
    model = Event
    success_url = reverse_lazy('event_list')

    def get(self, *args, **kwargs):
        return self.post(*args, **kwargs)


class AllNews(ListView):
    model = NewsItem
    template_name = 'myFirstApp/all_list.html'
    context_object_name = 'news_items'

    def get_context_data(self, **kwargs):
        context = super(AllNews, self).get_context_data(**kwargs)
        context['events'] = Event.objects.all()
        return context
