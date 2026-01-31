from django.shortcuts import render, redirect
from django.core.cache import cache
from django.http import Http404
import qrcode
import base64
from io import BytesIO
import random
import string

def generate_short_code():
    characters = string.ascii_letters + string.digits
    short_code = ''.join(random.choice(characters) for _ in range(6))
    return short_code

def home(request):
    context = {}

    if request.method == 'POST':
        original_url = request.POST.get('original_url')
        short_code = generate_short_code()

        # Store in cache
        cache.set(short_code, original_url, timeout=None)

        # Build short URL
        short_url = request.build_absolute_uri(short_code + '/')
        
        # Force HTTPS for production
        if 'onrender.com' in request.get_host():
            short_url = short_url.replace('http://', 'https://')

        # Generate QR Code
        qr = qrcode.QRCode(
            version=1,
            error_correction=qrcode.constants.ERROR_CORRECT_L,
            box_size=10,
            border=4
        )
        qr.add_data(short_url)
        qr.make(fit=True)

        qr_image = qr.make_image(fill_color="black", back_color="white")

        buffer = BytesIO()
        qr_image.save(buffer, format='PNG')
        buffer.seek(0)
        qr_code = base64.b64encode(buffer.getvalue()).decode('utf-8')

        context['short_url'] = short_url
        context['qr_code'] = qr_code
        context['original_url'] = original_url

    return render(request, 'shortener/home.html', context)

def redirect_url(request, shorter_url):
    original_url = cache.get(shorter_url)
    
    if original_url:
        return redirect(original_url)
    else:
        raise Http404("URL not found or expired")