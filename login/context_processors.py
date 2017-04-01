def users(request):
    if 'username' in request.session:
        return {'username': request.session['username']}
    else:
        return {}
