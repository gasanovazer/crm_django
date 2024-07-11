from django.contrib import messages
from django.contrib.auth.decorators import login_required
from django.shortcuts import get_object_or_404, redirect, render
from django.urls import reverse_lazy
from django.utils.decorators import method_decorator
from django.views.generic import DeleteView, DetailView, ListView

from .forms import AddLeadForm
from .models import Lead

from client.models import Client
from team.models import Team


class LeadListView(ListView):
    model = Lead

    @method_decorator(login_required)
    def dispatch(self, request, *args, **kwargs):
        return super().dispatch(request, *args, **kwargs)
    

    def get_queryset(self):
        queryset = super(LeadListView, self).get_queryset()
        return queryset.filter(created_by=self.request.user, converted_to_client=False)
    
class LeadDetailView(DetailView):
    model = Lead

    @method_decorator(login_required)
    def dispatch(self, request, *args, **kwargs):
        return super().dispatch(request, *args, **kwargs)
    
    def get_queryset(self):
        queryset = super(LeadDetailView, self).get_queryset()
        return queryset.filter(created_by=self.request.user, pk=self.kwargs.get('pk'))
    
class LeadDeleteView(DeleteView):
    model = Lead

    success_url = reverse_lazy('leads:list')

    @method_decorator(login_required)
    def dispatch(self, request, *args, **kwargs):
        return super().dispatch(request, *args, **kwargs)
    
    def get_queryset(self):
        queryset = super(LeadDeleteView, self).get_queryset()
        return queryset.filter(created_by=self.request.user, pk=self.kwargs.get('pk'))
    
    def get(self, request, *args, **kwargs):
        return super.post(request, *args, **kwargs)

@login_required
def leads_delete(request, pk):
    lead = get_object_or_404(Lead, created_by=request.user, pk=pk)
    lead.delete()

    messages.success(request, "The lead was deleted.")

    return redirect('leads:list')

@login_required
def leads_edit(request, pk):
    lead = get_object_or_404(Lead, created_by=request.user, pk=pk)

    if request.method == 'POST':
        form = AddLeadForm(request.POST, instance=lead)

        if form.is_valid():
            form.save()
            messages.success(request, "The changes was saved.")
            
            return redirect('leads:list')
    else:
        form = AddLeadForm(instance=lead)
    return render(request, 'lead/leads_edit.html', {
        'form': form
    })

@login_required
def add_lead(request):
    team = Team.objects.filter(created_by=request.user)[0]

    if request.method == 'POST':
        form = AddLeadForm(request.POST)

        if form.is_valid():
            team = Team.objects.filter(created_by=request.user)[0]
            lead = form.save(commit=False)
            lead.created_by = request.user
            lead.team= team
            lead.save()
            messages.success(request, "The lead was created.")

            return redirect('leads:list')
    else:
        form = AddLeadForm()

    return render(request, 'lead/add_lead.html', {
        'form': form,
        'team': team
    })

@login_required
def converted_to_client(request, pk):
    lead = get_object_or_404(Lead, created_by=request.user, pk=pk)
    team = Team.objects.first(crated_by=request.user)[0]
    
    client = Client.objects.create(
        name=lead.name,
        email=lead.email,
        description=lead.description,
        created_by = request.user,
        team = team,
    )
    lead.converted_to_client = True
    lead.save()
    messages.success(request, "The lead was converted to a client.")

    return redirect('leads:list')