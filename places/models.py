from django.db import models
from django.conf import settings
from django.utils.encoding import smart_text

class Category(models.Model):
    name = models.CharField(max_length=50)
    icon = models.CharField(max_length=20)
    color = models.CharField(max_length=7)

    def __str__(self):
        return smart_text(self.name)

'''class PlaceManager(models.Manager): #<-- heryerde wifi True olanları getir. Hem adminde panelinde hem sayfalarda
    def set_wifi_true(self):
        return self.get.queryset().update(has_wifi = True)'''


class Place(models.Model):
    user = models.ForeignKey(settings.AUTH_USER_MODEL, related_name='added_places')
    name = models.CharField(max_length=255)
    is_active = models.BooleanField(default=False)
    coordinates = models.CharField(max_length=255, null=True, blank=False)#'null' database için nullable, 'blank' formda validation için not required
    category = models.ForeignKey(Category)
    has_wifi = models.BooleanField(default=False)
    telephone = models.CharField(max_length=255, blank=True, null=True)
    description = models.TextField(blank=True, null=True)
    likes = models.ManyToManyField(settings.AUTH_USER_MODEL, blank=True, related_name='liked_places')
    #objects = PlaceManager() #<-- PlaceManager'ı Place modeline ekledik

    '''class Meta:
        verbose_name = "Yer" <-- Admin kısmında Place yerine Yer şeklinde çıkması için
        verbose_name_plural = "Yerler" <-- Admin kısmında Yers şeklinde çıkmaması için'''

    def __str__(self):
        return smart_text(self.name)

    @models.permalink
    def get_absolute_url(self): #<-- get_absolute_url metodu linkleri hard_coded yazmamak için kullanıldı böylece urls.py'dan url'imizi degiştirdigimizde tek tek html sayfalarından degiştirmek zorunda kalmayacagız.
        return ('place_detail', (self.id,))

    #Seçilen yerin toplam yorum sayısını getir
    def review_count(self): #<-- admin.py içerisinde kullanabiliyoruz list_display ile admin panelde görüntüleniyor
        return self.review_set.count()

    #Seçilen yerin active yorumlarını getir
    def active_reviews(self):
        return self.review_set.filter(is_active = True)

    #Seçilen yerin active resimlerini getir
    def place_pictures(self):
        return self.media_set.filter(is_active = True)

    #Giriş yapmış olan kullanıcının Review'ları active mi getir
    def user_place_review(self):
        return self.review_set.filter(is_active = True, user__username = self.user)

    #Seçilen place için yorum yapan kullanıcıları çek ve bir listeye username'lerini at
    def commenters(self):
        commented_users = list()
        for review in self.review_set.all():
                commented_users.append(review.user.username)
        return commented_users

class Review(models.Model):
    user = models.ForeignKey(settings.AUTH_USER_MODEL)
    place = models.ForeignKey(Place)
    comment = models.TextField()
    vote = models.IntegerField(
        default = 3,
        choices = (
                (1, 'Bad'),
                (2, 'Not Bad'),
                (3, 'Meh'),
                (4, 'Fine'),
                (5, 'Rocks'),
        )
    )
    is_active = models.BooleanField(default=False)

    def __str__(self):
        return smart_text(self.comment)

class Media(models.Model):
    user = models.ForeignKey(settings.AUTH_USER_MODEL)
    place = models.ForeignKey(Place)
    image = models.ImageField(upload_to="uploads") #image için 'pillow' yüklemek gerekli (pip install pillow)
    is_active = models.BooleanField(default=False)

    def __str__(self):
        return smart_text(self.image.url)
