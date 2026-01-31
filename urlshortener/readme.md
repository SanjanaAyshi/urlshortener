# 🔗 URL Shortener

A simple URL shortener built with Django featuring a retro Windows 98 UI design and QR code generation.

![Python](https://img.shields.io/badge/Python-3.10+-blue.svg)
![Django](https://img.shields.io/badge/Django-4.2-green.svg)
![License](https://img.shields.io/badge/License-MIT-yellow.svg)

## 🌐 Live Demo

[https://urlshortener-dwty.onrender.com/](https://urlshortener-dwty.onrender.com/)

## ✨ Features

- 🔗 **URL Shortening** - Convert long URLs into short, shareable links
- 📱 **QR Code Generation** - Automatic QR code for each shortened URL
- 🖥️ **Retro UI** - Windows 98 inspired design
- ⚡ **Fast** - Uses in-memory cache for quick access
- 🌍 **Free Hosting** - Deployed on Render

## 🛠️ Tech Stack

- **Backend:** Django 4.2
- **Frontend:** HTML, CSS (Windows 98 theme)
- **QR Code:** qrcode library with Pillow
- **Storage:** Django Cache (In-Memory)
- **Hosting:** Render

## 🚀 How It Works

1. User enters a long URL
2. System generates random 6-character code (e.g., "aB3xK9")
3. URL is stored in cache: aB3xK9 → original URL
4. QR code is generated with the short URL
5. User gets short link + QR code

### When someone visits the short URL:

1. System looks up the code in cache
2. Finds the original URL
3. Redirects user to original URL

## 📁 Project Structure

urlshortener/
├── shortener/
│ ├── templates/shortener/
│ │ ├── base.html
│ │ └── home.html
│ ├── views.py
│ └── urls.py
├── urlshortener/
│ ├── settings.py
│ ├── urls.py
│ └── wsgi.py
├── requirements.txt
├── build.sh
└── README.md

## 🏃 Run Locally

### Prerequisites

- Python 3.10+

### Installation

1. Clone the repository

2. Create virtual environment
   python -m venv venv
3. Activate virtual environment
   venv\Scripts\activate
   Windows:
4. Install dependencies
   pip install -r requirements.txt

5. Run the server
   python manage.py runserver

6. Open browser: http://127.0.0.1:8000/

## 📦 Dependencies

| Package    | Purpose            |
| ---------- | ------------------ |
| Django     | Web framework      |
| qrcode     | QR code generation |
| Pillow     | Image processing   |
| gunicorn   | Production server  |
| whitenoise | Static files       |

## 🌐 Deployment (Render)

**Build Command:**
./build.sh

**Start Command:**
gunicorn urlshortener.wsgi:application

## 👩‍💻 Author

**Sanjana**

- Portfolio: [https://protfolio-sanjana.vercel.app/](https://protfolio-sanjana.vercel.app/)
- GitHub: [@SanjanaAyshi](https://github.com/SanjanaAyshi)

## 📄 License

This project is open source under the MIT License.

---

Made with Django
