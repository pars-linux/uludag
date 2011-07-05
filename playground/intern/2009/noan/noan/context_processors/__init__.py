from noan.repository.models import Distribution

def distros(request):
    distros = Distribution.objects.all()
    return {
        'distros': distros,
    }
