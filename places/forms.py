from django.forms import ModelForm, HiddenInput, ValidationError
from django.utils.translation import ugettext_lazy as _
from django import forms

from places.models import Place, Media, Review

class PlaceCreationForm(ModelForm):
    class Meta:
        model = Place
        fields = (
            'name',
            'coordinates',
            'category',
            'has_wifi',
            'telephone',
            'description',
        )

        labels = {
            'name' : '',
            'category' : _('Category'),
            'has_wifi' : _('Has Wifi'),
            'telephone' : '',
            'description' : ''
        }

        widgets = {
            'coordinates' : HiddenInput,
            'category' : forms.Select(attrs={'class' : 'form-control'}),
            'has_wifi' : forms.CheckboxInput(attrs={'class' : 'form-control'}),
            'name' : forms.TextInput(attrs = {
                                              'class' : 'form-control',
                                              'placeholder' : _('Place Name')
                                             }
                                     ),

            'telephone' : forms.TextInput(attrs = {
                                              'class' : 'form-control',
                                              'placeholder' : _('Telephone')
                                             }
                                     ),

            'description' : forms.Textarea(attrs = {
                                              'class' : 'form-control',
                                              'placeholder' : _('Enter a description')
                                             }
                                     )
        }

    def clean_coordinates(self):
        coords = self.cleaned_data['coordinates']

        try:
            lat, lng = coords.split(',')
            lat = float(lat)
            lng = float(lng)

            if (
                lat < -90 or lat > 90 or
                lng < -180 or lng > 180
            ):
                raise ValidationError(_('Please enter an available coordinate.'))
        except ValueError:
            raise ValidationError('Enter coordinates with click on the map where the place is shown.')
        return coords

class MediaCreationForm(ModelForm):
	class Meta:
		model = Media
		fields = ('image', )

class ReviewCreationForm(ModelForm):
    class Meta:
        model = Review
        fields = ('comment', 'vote', )
