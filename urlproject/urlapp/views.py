from rest_framework import status
from django.shortcuts import get_object_or_404, redirect
from django.utils import timezone
from django.http import HttpResponseNotFound
import random, string

from .models import *

from rest_framework.views import APIView
from rest_framework.response import Response

def generate_shortcode(length=6):
    return ''.join(random.choices(string.ascii_letters + string.digits, k=length))


class ShortURLCreateView(APIView):
    def post(self, request):
        url=request.data.get('url')
        validity= request.data.get('validity', 30)
        shortcode =request.data.get('shortcode')
        if not url:
            return Response({"error": "URL is required."}, status=status.HTTP_400_BAD_REQUEST)
        if shortcode:
            if Url.objects.filter(short_code=shortcode).exists():
                return Response({"error": "Shortcode already exists."}, status=status.HTTP_400_BAD_REQUEST)
        else:
            while True:
                shortcode = generate_shortcode()
                if not Url.objects.filter(short_code=shortcode).exists():
                    break
        shorturl=Url.objects.create(url=url,short_code=shortcode,validity=validity)
        expiry=shorturl.create_time + timezone.timedelta(minutes=int(validity))
        return Response({
            "shortLink": f"http://localhost:8000/r/{shorturl.short_code}/",
            "expiry": expiry.isoformat()
        }, status=status.HTTP_201_CREATED)


class ShortURLStatsView(APIView):
    def get(self, request, shortcode):
        shorturl =get_object_or_404(Url, short_code=shortcode)
        expiry_time =shorturl.create_time + timezone.timedelta(minutes=shorturl.validity)
        click_details=Detail.objects.filter(short=shorturl).values('click_time', 'referrer', 'location')

        return Response({
            "original_url":shorturl.url,
            "created_at":shorturl.create_time,
            "validity_minutes":shorturl.validity,
            "expiry_time":expiry_time,
            "click_count":shorturl.clicks,
            "clicks":list(click_details)
        })


def redirect_view(request, shortcode):
    shorturl=Url.objects.filter(short_code=shortcode).first()
    if not shorturl:
        return HttpResponseNotFound('Shortcode not found.')

    expiry_time=shorturl.create_time + timezone.timedelta(minutes=shorturl.validity)
    if timezone.now() > expiry_time:
        return HttpResponseNotFound('Shortcode expired.')
    shorturl.clicks += 1
    shorturl.save()

    Detail.objects.create(short=shorturl,referrer=request.META.get('HTTP_REFERER', ''),location="Unknown")

    return redirect(shorturl.url)
