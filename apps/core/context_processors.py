from .models import Logo


def logos(request):
    """Context processor pour rendre les logos disponibles dans tous les templates"""
    logo_principal = Logo.objects.filter(type_logo='principal', actif=True).first()
    logo_footer = Logo.objects.filter(type_logo='footer', actif=True).first()
    logo_favicon = Logo.objects.filter(type_logo='favicon', actif=True).first()
    
    return {
        'logo_principal': logo_principal,
        'logo_footer': logo_footer,
        'logo_favicon': logo_favicon,
    }



