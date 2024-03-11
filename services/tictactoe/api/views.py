from    django.shortcuts    import render, redirect
from    django.http         import Http404

def play( request ):
        return render(request, "index.html", {})
        