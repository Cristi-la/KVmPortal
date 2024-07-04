from django.shortcuts import render
from django.contrib.auth.models import User


def test(request):
    user = User.objects.all()

    return render(
        request,
        'test.html',
        {'user': user}
    )
