# desaapp/views.py
from django.shortcuts import render, get_object_or_404, redirect
from django.contrib import messages
from django.core.mail import send_mail
from django.conf import settings
from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.models import User
from django.contrib.auth.decorators import login_required

from .models import (
    KepalaDesa, VisiMisi, LayananCepat, JamLayanan,
    LokasiKantor, Kontak, News, Document, Event,
    Gallery, SejarahDesa, Service, ServiceRequest
)
from .forms import ContactForm, ServiceRequestForm

# ========================================================
#                   HALAMAN UMUM / PUBLIK
# ========================================================

# -------------------- Home --------------------
def home(request):
    context = {
        'kepala_desa': KepalaDesa.objects.first(),
        'visi_misi': VisiMisi.objects.first(),
        'layanan_cepat': LayananCepat.objects.all(),
        'jam_layanan': JamLayanan.objects.first(),
        'lokasi': LokasiKantor.objects.all(),
        'kontak': Kontak.objects.first(),
    }
    return render(request, 'desaapp/home.html', context)


# -------------------- Profil Desa --------------------
@login_required(login_url='login_user')
def profile(request):
    age_groups = [
        {"group": "0-17 tahun", "count": 1045},
        {"group": "18-60 tahun", "count": 2156},
        {"group": "60+ tahun", "count": 255},
    ]
    total_population = sum(a['count'] for a in age_groups)
    for a in age_groups:
        a['percentage'] = round((a['count'] / total_population) * 100, 2)

    statistics = [
        {"label": "Jumlah Penduduk", "value": f"{total_population:,}"},
        {"label": "Kepala Keluarga", "value": "1,700"},
        {"label": "Laki-laki", "value": "1,391"},
        {"label": "Perempuan", "value": "1,287"},
    ]

    officials = [
        {"name": "Ashari Setiawan S.Pd.I", "position": "Kepala Desa", "period": "2024-2027"},
        {"name": "Agus Wirawan", "position": "Sekretaris Desa", "period": "2024-2027"},
        {"name": "Sugeng Wiyono", "position": "Kaur Keuangan", "period": "2024-2027"},
        {"name": "Mariana Permata Saputri", "position": "Kaur Umum", "period": "2024-2027"},
        {"name": "Agus Setia Nugraha S.P", "position": "Kaur Perencanaan", "period": "2024-2027"},
        {"name": "I Nyoman Darya", "position": "Kasi Pemerintahan", "period": "2024-2027"},
        {"name": "Sahrul Saputra S.IP", "position": "Kasi Kesejahteraan", "period": "2024-2027"},
        {"name": "Yohana P.D Ratu", "position": "Kasi Pelayanan", "period": "2024-2027"},
    ]

    institutions = [
        {
            "name": "Lembaga Perlindungan Masyarakat (Linmas)",
            "leader": "Muhammad Amin",
            "secretary": "Sunyotoadi",
            "members": ["Rohady", "Slamet", "Andi Sutria"]
        },
        {
            "name": "Lembaga Pemberdayaan Masyarakat (LPM)",
            "leader": "Ketut Jana L",
            "secretary": "I Nyoman Lasya Putrajaya",
            "members": ["Ida Bagus Sugiana", "Riyanto", "Hamdi"]
        },
        {
            "name": "Lembaga Adat",
            "leader": "Asrori Setiawan",
            "secretary": "Putu Mangu Merta",
            "members": ["Sutrisno", "Damaskus", "Made Pasek"]
        },
    ]

    return render(request, "desaapp/profile.html", {
        "statistics": statistics,
        "age_groups": age_groups,
        "officials": officials,
        "institutions": institutions,
        "total_population": total_population,
        "sejarah": SejarahDesa.objects.first(),
        "visi_misi": VisiMisi.objects.first(),
    })


# -------------------- Berita Desa --------------------
@login_required(login_url='login_user')
def news_list(request):
    search_term = request.GET.get('q', '')
    category = request.GET.get('category', 'Semua')

    news_list = News.objects.all().order_by('-date', '-time')
    if search_term:
        news_list = news_list.filter(title__icontains=search_term) | news_list.filter(excerpt__icontains=search_term)
    if category != 'Semua':
        news_list = news_list.filter(category=category)

    context = {
        'news_list': news_list,
        'categories': ['Pengumuman', 'Kegiatan', 'Pembangunan', 'UMKM', 'Kesehatan'],
        'documents': Document.objects.all().order_by('-date')[:5],
        'events': Event.objects.all().order_by('date')[:5],
        'search_term': search_term,
        'selected_category': category,
    }
    return render(request, 'desaapp/news.html', context)


@login_required(login_url='login_user')
def news_detail(request, id):
    news_item = get_object_or_404(News, pk=id)
    return render(request, 'desaapp/news_detail.html', {'news': news_item})


# -------------------- Layanan Desa --------------------
@login_required(login_url='login_user')
def services_view(request):
    selected_category = request.GET.get("category", "Semua")
    services = Service.objects.all()
    if selected_category != "Semua":
        services = services.filter(category=selected_category)

    external_services = [
        {"name": "Dukcapil Online", "description": "Layanan kependudukan online", "url": "https://dukcapil.kemendagri.go.id"},
        {"name": "BPJS Kesehatan", "description": "Layanan jaminan kesehatan nasional", "url": "https://bpjs-kesehatan.go.id"},
    ]

    return render(request, "desaapp/services.html", {
        "services": services,
        "selected_category": selected_category,
        "external_services": external_services,
    })


@login_required(login_url='login_user')
def service_request(request, service_id):
    service = get_object_or_404(Service, id=service_id)
    if request.method == "POST":
        form = ServiceRequestForm(request.POST)
        if form.is_valid():
            req = form.save(commit=False)
            req.service = service
            req.save()
            return redirect("services")
    else:
        form = ServiceRequestForm()

    return render(request, "desaapp/service_request.html", {"service": service, "form": form})


@login_required(login_url='login_user')
def service_requests(request):
    requests = ServiceRequest.objects.all().order_by("-id")
    return render(request, "desaapp/service_requests.html", {"requests": requests})


# -------------------- Galeri Desa --------------------
@login_required(login_url='login_user')
def gallery_view(request):
    category = request.GET.get("category", "Semua")
    galleries = Gallery.objects.all().order_by("-date") if category == "Semua" else Gallery.objects.filter(category=category).order_by("-date")

    return render(request, "desaapp/gallery.html", {
        "galleries": galleries,
        "categories": ["Semua", "Kegiatan Warga", "Pembangunan", "UMKM", "Budaya", "Alam"],
        "active_category": category,
    })


@login_required(login_url='login_user')
def gallery_detail(request, pk):
    gallery = get_object_or_404(Gallery, pk=pk)
    gallery.views += 1
    gallery.save(update_fields=["views"])
    return render(request, "desaapp/gallery_detail.html", {"gallery": gallery})


# -------------------- Kontak Desa --------------------
@login_required(login_url='login_user')
def contact_view(request):
    if request.method == 'POST':
        form = ContactForm(request.POST)
        if form.is_valid():
            contact_message = form.save()
            subject = f"[Kontak Desa] {contact_message.subjek}"
            message = f"""
Nama: {contact_message.nama}
Email: {contact_message.email}
Telepon: {contact_message.telepon}
Bagian: {contact_message.bagian}

Pesan:
{contact_message.pesan}
"""
            send_mail(subject, message, settings.DEFAULT_FROM_EMAIL, ['Sidomulyodesaku950@gmail.com'], fail_silently=False)
            messages.success(request, "Pesan berhasil dikirim!")
            return redirect('contact')
        else:
            messages.error(request, "Terjadi kesalahan, silakan cek kembali form.")
    else:
        form = ContactForm()
    return render(request, 'desaapp/contact.html', {'form': form})


# ========================================================
#                   SISTEM LOGIN & ADMIN
# ========================================================
from django.contrib.auth.decorators import user_passes_test
from django.contrib.admin.views.decorators import staff_member_required

# ---------- Cek role ----------
def is_admin(user):
    return user.is_authenticated and user.is_staff

def is_user(user):
    return user.is_authenticated and not user.is_staff


# ==============================
# LOGIN USER
# ==============================
def login_user(request):
    if request.method == 'POST':
        username = request.POST['username']
        password = request.POST['password']

        user = authenticate(request, username=username, password=password)
        if user is not None:
            if not user.is_staff:
                login(request, user)
                messages.success(request, f'Selamat datang, {user.username}!')
                return redirect('home')
            else:
                messages.error(request, 'Gunakan halaman login admin!')
                return redirect('login_admin')
        else:
            messages.error(request, 'Username atau password salah!')
            return redirect('login_user')
    return render(request, 'desaapp/registrations/login_user.html')


# ==============================
# LOGIN ADMIN
# ==============================
def login_admin(request):
    if request.method == 'POST':
        username = request.POST['username']
        password = request.POST['password']

        user = authenticate(request, username=username, password=password)
        if user is not None:
            if user.is_staff:
                login(request, user)
                messages.success(request, f'Selamat datang, {user.username} (Admin)!')
                return redirect('home')
            else:
                messages.error(request, 'Akses ditolak! Anda bukan admin.')
                return redirect('login_admin')
        else:
            messages.error(request, 'Username atau password salah!')
            return redirect('login_admin')
    return render(request, 'desaapp/registrations/login_admin.html')


# ==============================
# HALAMAN ADMIN PANEL
# ==============================
@staff_member_required(login_url='login_admin')
def admin_panel(request):
    context = {
        "total_users": User.objects.count(),
        "total_news": News.objects.count(),
        "total_services": Service.objects.count(),
        "total_gallery": Gallery.objects.count(),
        "total_messages": Kontak.objects.count(),
    }
    return render(request, 'desaapp/admin_panel.html', context)


# ==============================
# LOGOUT
# ==============================
def logout_user(request):
    logout(request)
    messages.info(request, 'Anda telah logout.')
    return redirect('home')


# ==============================
# REGISTER USER
# ==============================
def register_user(request):
    if request.method == 'POST':
        username = request.POST['username']
        password = request.POST['password']
        password2 = request.POST['password2']

        if password != password2:
            messages.error(request, 'Password tidak cocok!')
            return redirect('register')

        if User.objects.filter(username=username).exists():
            messages.error(request, 'Username sudah digunakan!')
            return redirect('register')

        user = User.objects.create_user(username=username, password=password)
        user.save()
        messages.success(request, 'Registrasi berhasil! Silakan login.')
        return redirect('login_user')

    return render(request, 'desaapp/registrations/register.html')
