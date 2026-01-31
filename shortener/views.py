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

    # Check if we have result in session
    if 'short_url' in request.session:
        context['short_url'] = request.session.pop('short_url')
        context['qr_code'] = request.session.pop('qr_code', None)

    if request.method == 'POST':
        original_url = request.POST.get('original_url')
        short_code = generate_short_code()

        # Store in cache
        cache.set(short_code, original_url, timeout=None)

        # Build short URL - Force HTTPS
        if request.is_secure() or 'onrender.com' in request.get_host():
            scheme = 'https'
        else:
            scheme = 'http'
        
        host = request.get_host()
        short_url = f"{scheme}://{host}/{short_code}/"

        # Generate QR Code
        qr = qrcode.QRCode(
            version=2,
            error_correction=qrcode.constants.ERROR_CORRECT_H,
            box_size=12,
            border=4,
        )
        qr.add_data(short_url)
        qr.make(fit=True)

        qr_image = qr.make_image(fill_color="#000000", back_color="#FFFFFF")
        
        buffer = BytesIO()
        qr_image.save(buffer, format='PNG')
        buffer.seek(0)
        qr_base64 = base64.b64encode(buffer.getvalue()).decode('utf-8')

        # Store in session temporarily
        request.session['short_url'] = short_url
        request.session['qr_code'] = qr_base64

        # Redirect to same page (PRG pattern)
        return redirect('home')

    return render(request, 'shortener/home.html', context)

def redirect_url(request, shorter_url):
    original_url = cache.get(shorter_url)
    
    if original_url:
        return redirect(original_url)
    else:
        raise Http404("URL not found or expired")