from django.shortcuts import render, redirect, get_object_or_404
from .models import URL, generate_short_url
import qrcode
import base64
from io import BytesIO

def home(request):
    context = {}

    if request.method == 'POST':
        original_url = request.POST.get('original_url')
        shorter_url = generate_short_url()

        url_object = URL.objects.create(
            original_url=original_url,
            shorter_url=shorter_url
        )

        short_url = request.build_absolute_uri(shorter_url + '/')

        # Generate QR Code
        qr = qrcode.QRCode(
            version=1,
            box_size=10,
            border=4
        )
        qr.add_data(short_url)
        qr.make(fit=True)

        # Create QR image
        qr_image = qr.make_image(fill_color="black", back_color="white")

        # Convert to base64
        buffer = BytesIO()
        qr_image.save(buffer, format='PNG')
        buffer.seek(0)
        qr_code = base64.b64encode(buffer.getvalue()).decode('utf-8')

        context['short_url'] = short_url
        context['qr_code'] = qr_code

    return render(request, 'shortener/home.html', context)

def redirect_url(request, shorter_url):
    url_object = get_object_or_404(URL, shorter_url=shorter_url)
    return redirect(url_object.original_url)