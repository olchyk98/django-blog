def base(request):
    return {
        'inAuth': bool(request.session.get('uauth', False))
    }