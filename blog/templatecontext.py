from .models import Author

def base(request):
    inAuth = False

    if(request.session.get('uauth', False)):
        inAuth = Author.objects.get(login = request.session['uauth']['login'])
    # end

    return {
        'inAuth': inAuth,
    }
# end