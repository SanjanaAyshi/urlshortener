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
    
    # Check if showing result
    show_code = request.GET.get('code')
    if show_code:
        # Build the short URL
        if request.is_secure() or 'onrender.com' in request.get_host():
            scheme = 'https'
        else:
            scheme = 'http'
        
        host = request.get_host()
        short_url = f"{scheme}://{host}/{show_code}/"
        
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
        
        context['short_url'] = short_url
        context['qr_code'] = qr_base64

    if request.method == 'POST':
        original_url = request.POST.get('original_url')
        short_code = generate_short_code()

        # Store in cache
        cache.set(short_code, original_url, timeout=None)

        # Redirect with code parameter
        return redirect(f'/?code={short_code}')

    return render(request, 'shortener/home.html', context)

def redirect_url(request, shorter_url):
    original_url = cache.get(shorter_url)
    
    if original_url:
        return redirect(original_url)
    else:
        raise Http404("URL not found or expired")