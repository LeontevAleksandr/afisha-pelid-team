import requests
from django.core.management.base import BaseCommand
from django.core.files.base import ContentFile
from places.models import Place, Image


class Command(BaseCommand):
    help = 'Load place from JSON'

    def add_arguments(self, parser):
        parser.add_argument('json_url', type=str)

    def handle(self, *args, **options):
        response = requests.get(options['json_url'])
        data = response.json()
        
        place = Place.objects.create(
            title=data['title'],
            description_short=data.get('description_short', ''),
            description_long=data.get('description_long', ''),
            lng=data['coordinates']['lng'],
            lat=data['coordinates']['lat']
        )
        
        for position, img_url in enumerate(data.get('imgs', [])):
            img_response = requests.get(img_url)
            img_name = img_url.split('/')[-1]
            
            image = Image.objects.create(place=place, position=position)
            image.image.save(img_name, ContentFile(img_response.content), save=True)
        
        self.stdout.write(f'Loaded: {place.title}')