from django.shortcuts import render, render_to_response


def handler404(request):
    return render(request, '404.html', status=404)


def referral(request):
    return render_to_response('referral.html')
