import json
from django.shortcuts import render, get_object_or_404, redirect
from django.contrib import messages
from django.http import HttpResponse
from django.contrib.auth.decorators import login_required

from places.models import Place, Review
from places.forms import PlaceCreationForm, MediaCreationForm, ReviewCreationForm

def index(request):
    return render(
        request,
        'index.html',
        {
            'places': Place.objects.filter(is_active = True),
        }
    )


def detail(request, id):
	return render(
        request,
        'place.html',
        {
            'place': get_object_or_404(Place,  id = id, is_active = True),
        }
    )

@login_required(login_url='login') #<-- authenticated user degilse login sayfasına yönlendiriyor
def new_place(request):
    form = PlaceCreationForm()

    if request.method == 'POST':
        form = PlaceCreationForm(request.POST)
        if form.is_valid():
            form.instance.user = request.user #<-- ekleyen user'ı kaydetmek için
            form.save()
            messages.info(
                request,
                'Tebrikler. Yer bildiriminiz başarıyla alındı. '
                'Editör onayından geçtikten sonra yayınlanacaktır.'
            )
            return redirect('/')
    return render(
        request,
        'new_place.html',
        {
            'form': form,
        }
    )

@login_required(login_url='login')
def new_media(request, place_id):
    place = get_object_or_404(Place, id=place_id)
    form = MediaCreationForm()

    if request.method == 'POST':
        form = MediaCreationForm(request.POST, request.FILES)
        if form.is_valid():
            form.instance.place = place
            form.instance.user = request.user
            form.save()
            messages.info(
                request,
                'Tebrikler. Fotografınız başarıyla alındı. '
                'Editör onayından geçtikten sonra yayınlanacaktır.'
            )
            return redirect(place.get_absolute_url())

    return render(
        request,
        'new_media.html',
        {
            'place': place,#<-- place objesini gönderdik
            'form': form,#<-- formu gönderdik
        }
    )

@login_required(login_url='login')
def new_review(request, place_id):
    place = get_object_or_404(Place, id=place_id)
    form = ReviewCreationForm()

    if request.method == 'POST':
        form = ReviewCreationForm(request.POST)
        if form.is_valid():
            form.instance.place = place
            form.instance.user = request.user
            form.save()
            messages.info(
                request,
                'Tebrikler. Yorumunuz başarıyla alındı. '
                'Editör onayından geçtikten sonra yayınlanacaktır.'
            )
            return redirect(place.get_absolute_url())

    return render(
        request,
        'new_review.html',
        {
            'place': place,#<-- place objesini gönderdik
            'form': form,#<-- formu gönderdik
        }
    )

@login_required(login_url='login')
def update_review(request, review_id, place_id):
    review = get_object_or_404(Review, id = review_id, place = place_id,  user = request.user)
    place = get_object_or_404(Place, id = place_id)
    form = ReviewCreationForm(initial = {'comment' : review.comment, 'vote' : review.vote }) #<-- form'u oluştururken o name'li inputları gerekli degişkenler ile doldurduk.

    if request.method == 'POST':
        form = ReviewCreationForm(request.POST)
        if form.is_valid():
            ''' yeni bir form instance etmedigimiz için bu kısma ihtiyacımız yok.
            form.instance.review = review
            form.instance.place = place
            form.instance.user = request.user'''
            review = Review.objects.get(pk = review_id)#<-- üzerinde degişiklik yapmak istedigimiz objeyi çekiyoruz
            form = ReviewCreationForm(request.POST, instance = review)#<-- objeyi forma instance ediyoruz
            review.is_active = False #<-- o review'ın is_active kısmını tekrar false yapıyoruz ki bizim onayımızdan geçmek zorunda kalsın (editleyince belki küfür vs. girmiş olabilir)
            form.save()
            messages.info(
                request,
                'Tebrikler. Yorumunuz başarıyla degiştirildi. '
                'Editör onayından geçtikten sonra yayınlanacaktır.'
            )
            return redirect(place.get_absolute_url())

    return render(
        request,
        'new_review.html',
        {
            'place': place,#<-- place objesini gönderdik
            'review' : review, #<-- review objesini gönderdik
            'form': form,#<-- formu gönderdik
        }
    )

@login_required(login_url='login')
def like_place(request, place_id):
    place = get_object_or_404(Place, id = place_id)

    if request.method == 'POST':
        if request.user in place.likes.all():
            place.likes.remove(request.user)
            action = 'unlike'
        else:
            place.likes.add(request.user)
            action = 'like'

        if request.is_ajax():
            return HttpResponse(
                json.dumps({
                    'count' : place.likes.count(),
                    'action': action
                    })
                )

    else:
        return HttpResponse(status_code = 403)

    return redirect(place.get_absolute_url())
