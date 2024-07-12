from .models import Team

def team(request):
    team = Team.objects.filter(created_by=request.user)[0]
    return {'team': team}