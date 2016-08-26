from django.contrib import admin

from places.models import (
    Place, Category, Review, Media
)

class MediaInline(admin.TabularInline):#<-- admin panel listelemesinde TabularInline yanyana gösterir, StackedInline altalta gösterir
    model = Media
    extra = 0#<-- extra yeni resimler girilecek yerler gösterilmesin sadece girilenler gösterilsin

class ReviewInline(admin.TabularInline):
    model = Review
    extra = 0

class PlaceAdmin(admin.ModelAdmin): #<-- admin panelde model'in oldugu kısma ulaşmak için Model_adıAdmin kullanılır
    list_display = ('name', 'user', 'category', 'has_wifi', 'review_count', 'is_active') #<-- admin panelde listede gösterilmesini istedigimiz yerler
    list_editable = ('category', 'has_wifi', 'is_active') #<-- admin panelde direk listeden editlenecek yerler
    actions = ('set_wifi_true', ) #<-- admin panelde yapılacak Eylemlere bir yenisini ekledik, !!!tuple olarak algılaması için muhakkak sona virgül koymalıyız, yoksa string olarak algılar parantezlerin bir etkisi yoktur!!!!
    inlines = [
        MediaInline, #<--Admin panelde Places sayfasından direk resim ekleyebilmek için yazdık (class'ı yukarda tanımlı)
        ReviewInline, #<--Admin panelde Places sayfasından direk rewiew ekleyebilmek için yazdık (class'ı yukarda tanımlı)
    ]

    def set_wifi_true(self, request, queryset):#<-- admin panelde 'set_wifi_true' ismi ile yapılacak işlemin fonksiyonu
        queryset.update(has_wifi = True)
    set_wifi_true.short_description = 'Mahmut' #<-- admin panelde gösterilecek Eylemler kısmında 'Set wifi true' yerine Mahmut yazmasını sagladık!

admin.site.register(Place, PlaceAdmin)
admin.site.register(Review)
admin.site.register(Category)
admin.site.register(Media)
