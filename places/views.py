from django.shortcuts import get_object_or_404
from django.http import JsonResponse
from .models import Place


def places_geojson(request):
    features = []
    for place in Place.objects.prefetch_related('images').all():
        features.append({
            "type": "Feature",
            "geometry": {
                "type": "Point",
                "coordinates": [place.lng, place.lat]
            },
            "properties": {
                "title": place.title,
                "placeId": place.id,
                "detailsUrl": f"/places/{place.id}/"
            }
        })
    
    return JsonResponse({
        "type": "FeatureCollection",
        "features": features
    })

def place_detail(request, pk):
    place = get_object_or_404(Place, pk=pk)
    
    imgs = [request.build_absolute_uri(img.image.url) for img in place.images.all()]
    
    return JsonResponse({
        "title": place.title,
        "imgs": imgs,
        "description_short": place.description_short,
        "description_long": place.description_long,
        "coordinates": {
            "lng": str(place.lng),
            "lat": str(place.lat)
        }
    })