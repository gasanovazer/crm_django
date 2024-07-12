from django.contrib import messages
from django.contrib.auth.decorators import login_required
from django.shortcuts import redirect, render, get_object_or_404

from team.models import Team


from .forms import AddClientForm, AddCommentForm, AddFileForm
from .models import Client

@login_required
def clients_list(request):
    clients = Client.objects.filter(created_by=request.user)

    return render(request, 'client/clients_list.html', {
        'clients':clients
    })


@login_required
def clients_add_file(request, pk):
    client = get_object_or_404(Client, created_by=request.user, pk=pk)
    team = Team.objects.filter(created_by=request.user)[0]

    if request.method == 'POST':
        form = AddFileForm(request.POST, request.FILES)

        if form.is_valid():
            file = form.save(commit=False)
            file.team = team 
            file.client_id = pk
            file.created_by = request.user
            form.save()
        return redirect("clients:detail", pk=pk)
    return redirect("clients:detail", pk=pk)

@login_required
def clients_detail(request, pk):
    client = get_object_or_404(Client, created_by=request.user, pk=pk)

    if request.method == 'POST':
        form = AddCommentForm(request.POST)
        team = Team.objects.filter(created_by=request.user)[0]

        if form.is_valid():
            comment = form.save(commit=False)
            comment.team = team
            comment.created_by = request.user
            comment.client = client
            comment.save()

            return redirect('clients:detail', pk=pk)
    else:
        form = AddCommentForm()

    return render(request, 'client/clients_detail.html', {
        'client': client,
        'form': form,
        'fileform': AddFileForm()
    })

@login_required
def clients_add(request):
    if request.method == 'POST':
        form = AddClientForm(request.POST)

        if form.is_valid():
            team = Team.objects.filter(created_by=request.user)[0]
            
            client = form.save(commit=False)
            client.created_by = request.user
            client.team = team
            client.save()
            messages.success(request, "The client was created.")

            return redirect('clients:list')
    else:
        form = AddClientForm()

    return render(request, 'client/clients_add.html', {
        'form': form
    })

@login_required
def clients_edit(request, pk):
    client = get_object_or_404(Client, created_by=request.user, pk=pk)

    if request.method == 'POST':
        form = AddClientForm(request.POST, instance=client)

        if form.is_valid():
            form.save()
            messages.success(request, "The changes was saved.")

            return redirect('clients:list')
    else:
        form = AddClientForm(instance=client)
    
    return render(request, "client/clients_edit.html", {
        'form': form
    })

@login_required
def clients_delete(request, pk):
    client = get_object_or_404(Client, created_by=request.user, pk=pk)
    client.delete()

    messages.success(request, "The client was deleted.")

    return redirect('clients:list')