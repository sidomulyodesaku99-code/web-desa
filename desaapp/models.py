from django.db import models
from django_ckeditor_5.fields import CKEditor5Field
from django.utils.text import slugify

# ================= Kepala Desa =================
class KepalaDesa(models.Model):
    nama = models.CharField(max_length=100)
    foto = models.ImageField(upload_to='kepala_desa/')
    sambutan = CKEditor5Field('Sambutan Kepala Desa', config_name='extends')

    def __str__(self):
        return self.nama

# ================= Visi & Misi =================
class VisiMisi(models.Model):
    judul = models.CharField(max_length=200, default="Visi & Misi Desa")
    visi = CKEditor5Field('Visi Desa', config_name='extends')
    misi = CKEditor5Field('Misi Desa', config_name='extends', help_text="Isi dengan list misi, pisahkan baris dengan enter")

    def __str__(self):
        return self.judul


#service layanan/ pengajuan ############################################
from django.db import models

# Model Layanan Desa
class Service(models.Model):
    CATEGORY_CHOICES = [
        ("Kependudukan", "Kependudukan"),
        ("Sosial", "Sosial"),
        ("Perizinan", "Perizinan"),
        ("Ekonomi", "Ekonomi"),
    ]

    name = models.CharField(max_length=200)
    description = models.TextField()
    requirements = models.TextField(help_text="Pisahkan dengan koma (,)")  # disimpan string lalu di-split
    processing_time = models.CharField(max_length=100)
    fee = models.CharField(max_length=100, default="Gratis")
    category = models.CharField(max_length=50, choices=CATEGORY_CHOICES)

    def get_requirements_list(self):
        return [r.strip() for r in self.requirements.split(",")]

    def __str__(self):
        return self.name


# Model Pengajuan Layanan
class ServiceRequest(models.Model):
    STATUS_CHOICES = [
        ("pending", "Menunggu"),
        ("in_progress", "Diproses"),
        ("done", "Selesai"),
        ("rejected", "Ditolak"),
    ]

    service = models.ForeignKey(Service, on_delete=models.CASCADE)
    nama = models.CharField(max_length=100)
    nik = models.CharField(max_length=20)
    alamat = models.TextField()
    tanggal = models.DateTimeField(auto_now_add=True)
    status = models.CharField(max_length=20, choices=STATUS_CHOICES, default="pending")

    def __str__(self):
        return f"{self.nama} - {self.service.name}"


    
# ================= Sejarah Desa =================
class SejarahDesa(models.Model):
    judul = models.CharField(max_length=200, default="Sejarah Desa Sidomulyo")
    isi = CKEditor5Field('Isi Sejarah Desa', config_name='extends')
    tanggal_dibuat = models.DateTimeField(auto_now_add=True)
    tanggal_update = models.DateTimeField(auto_now=True)

    class Meta:
        verbose_name = "Sejarah Desa"
        verbose_name_plural = "Sejarah Desa"

    def __str__(self):
        return self.judul


# ================= Layanan Cepat =================
class LayananCepat(models.Model):
    nama = models.CharField(max_length=100)
    url = models.URLField(blank=True)

    def __str__(self):
        return self.nama

# ================= Jam Layanan =================
class JamLayanan(models.Model):
    hari1 = models.CharField(max_length=50)
    hari2 = models.CharField(max_length=50)

    def __str__(self):
        return "Jam Layanan"

# ================= Lokasi Kantor =================
class LokasiKantor(models.Model):
    alamat = models.TextField()

    def __str__(self):
        return self.alamat[:30]
    
    

# ================= Galeri =================
# desaapp/models.py

class Gallery(models.Model):
    CATEGORY_CHOICES = [
        ('Kegiatan Warga', 'Kegiatan Warga'),
        ('Pembangunan', 'Pembangunan'),
        ('UMKM', 'UMKM'),
        ('Budaya', 'Budaya'),
        ('Alam', 'Alam'),
        ('Pariwisata', 'Pariwisata'),
    ]

    title = models.CharField(max_length=200)
    description = models.TextField()
    date = models.DateField()
    category = models.CharField(max_length=50, choices=CATEGORY_CHOICES)
    thumbnail = models.ImageField(upload_to="gallery/thumbnails/")
    # video file optional
    video_file = models.FileField(upload_to="gallery/videos/", blank=True, null=True)
    video_url = models.URLField(blank=True, null=True)
    duration = models.CharField(max_length=20, blank=True, null=True)
    views = models.PositiveIntegerField(default=0)

    def __str__(self):
        return self.title

    # method helper untuk template
    def has_photos(self):
        return self.images.exists()

    def has_video(self):
        return self.video_file or self.video_url


class GalleryImage(models.Model):
    gallery = models.ForeignKey(Gallery, related_name="images", on_delete=models.CASCADE)
    image = models.ImageField(upload_to="gallery/images/")

    def __str__(self):
        return f"Gambar {self.gallery.title}"




# ================= News / Berita =================
class News(models.Model):
    CATEGORY_CHOICES = [
        ('Pengumuman', 'Pengumuman'),
        ('Kegiatan', 'Kegiatan'),
        ('Pembangunan', 'Pembangunan'),
        ('UMKM', 'UMKM'),
        ('Kesehatan', 'Kesehatan'),
        ('Pariwisata', 'Pariwisata'),
    ]

    title = models.CharField(max_length=255)
    excerpt = CKEditor5Field('Ringkasan Berita', config_name='extends')
    content = CKEditor5Field('Isi Berita', config_name='extends')
    date = models.DateField(auto_now_add=True)
    time = models.TimeField(auto_now_add=True)
    author = models.CharField(max_length=100)
    category = models.CharField(max_length=50, choices=CATEGORY_CHOICES)
    image = models.ImageField(upload_to="news_images/", blank=True, null=True)
    is_important = models.BooleanField(default=False)
    slug = models.SlugField(unique=True, blank=True)
    source_url = models.URLField(blank=True, null=True)

    def save(self, *args, **kwargs):
        if not self.slug:
            self.slug = slugify(self.title)
        super().save(*args, **kwargs)

    def __str__(self):
        return self.title

# ================= Document =================
class Document(models.Model):
    title = models.CharField(max_length=255)
    date = models.DateField()
    file_type = models.CharField(max_length=10)
    size = models.CharField(max_length=20)
    file = models.FileField(upload_to='documents/')

    def __str__(self):
        return self.title

# ================= Event =================
class Event(models.Model):
    title = models.CharField(max_length=255)
    date = models.DateField()
    time = models.TimeField()
    location = models.CharField(max_length=255)

    def __str__(self):
        return self.title

# ================= Contact Message =================
class ContactMessage(models.Model):
    nama = models.CharField(max_length=100)
    email = models.EmailField()
    telepon = models.CharField(max_length=20, blank=True)
    bagian = models.CharField(max_length=50, blank=True)
    subjek = models.CharField(max_length=200)
    pesan = CKEditor5Field('Pesan', config_name='extends')
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"{self.nama} - {self.subjek}"

# ================= Kontak =================
class Kontak(models.Model):
    telepon = models.CharField(max_length=20)
    email = models.EmailField()

    def __str__(self):
        return f"Kontak {self.telepon}"
    
