from django.contrib import admin
from .models import (
    KepalaDesa, VisiMisi, LayananCepat, JamLayanan, LokasiKantor,
    Kontak, Gallery, GalleryImage, News, Document, Event, ContactMessage, SejarahDesa
)

# ================= Model CKEditor5 =================
@admin.register(KepalaDesa)
class KepalaDesaAdmin(admin.ModelAdmin):
    fields = ('nama', 'foto', 'sambutan')

@admin.register(VisiMisi)
class VisiMisiAdmin(admin.ModelAdmin):
    fields = ('visi', 'misi')

# ================== Sejarah Desa=============
@admin.register(SejarahDesa)
class SejarahDesaAdmin(admin.ModelAdmin):
    list_display = ('judul', 'tanggal_dibuat', 'tanggal_update')
    search_fields = ('judul',)


@admin.register(ContactMessage)
class ContactMessageAdmin(admin.ModelAdmin):
    fields = ('nama', 'email', 'telepon', 'bagian', 'subjek', 'pesan', 'created_at')
    readonly_fields = ('created_at',)

# ================= Model News =================
@admin.register(News)
class NewsAdmin(admin.ModelAdmin):
    list_display = ('title', 'author', 'category', 'date', 'is_important')
    list_filter = ('category', 'is_important')
    search_fields = ('title', 'excerpt', 'content')
    prepopulated_fields = {'slug': ('title',)}
    fields = ('title', 'excerpt', 'content', 'author', 'category', 'image', 'is_important', 'slug', 'source_url')

# ================= Model Gallery =================
class GalleryImageInline(admin.TabularInline):
    model = GalleryImage
    extra = 1

@admin.register(Gallery)
class GalleryAdmin(admin.ModelAdmin):
    list_display = ('title', 'category', 'date', 'views')
    search_fields = ('title', 'description')
    inlines = [GalleryImageInline]

# ================= Model standar =================
@admin.register(LayananCepat)
class LayananCepatAdmin(admin.ModelAdmin):
    list_display = ('nama', 'url')

@admin.register(JamLayanan)
class JamLayananAdmin(admin.ModelAdmin):
    list_display = ('hari1', 'hari2')

@admin.register(LokasiKantor)
class LokasiKantorAdmin(admin.ModelAdmin):
    list_display = ('alamat',)

@admin.register(Kontak)
class KontakAdmin(admin.ModelAdmin):
    list_display = ('telepon', 'email')

@admin.register(Document)
class DocumentAdmin(admin.ModelAdmin):
    list_display = ('title', 'date', 'file_type', 'size', 'file')

@admin.register(Event)
class EventAdmin(admin.ModelAdmin):
    list_display = ('title', 'date', 'time', 'location')

#layanan/service/pengajuan 
from .models import Service, ServiceRequest

@admin.register(Service)
class ServiceAdmin(admin.ModelAdmin):
    list_display = ("name", "category", "fee", "processing_time")
    search_fields = ("name", "category")

@admin.register(ServiceRequest)
class ServiceRequestAdmin(admin.ModelAdmin):
    list_display = ("nama", "nik", "service", "status", "tanggal")
    list_filter = ("status", "service")
    search_fields = ("nama", "nik", "alamat")
