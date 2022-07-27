from model import Artist, Venue, Show
from sqlalchemy import func


def collect_venue_organise_by_city(funct, now):
    cities = Venue.query.with_entities(Venue.city, Venue.state).distinct(Venue.city).all()
    data = []
    for city, state in cities:
        res = Venue.query.filter_by(city=city)
        venues = [{
            'id': v.id,
            'name': v.name,
            'num_upcoming_shows': len(funct(v.id, now)[1])
            }
            for v in res]
        val = {
            "city": city,
            "state": state,
            "venues": venues
        }
        data.append(val)
    return data


def search_venue_by_string(string, function, now):
    if string is None or len(string) < 1:
        data = {"count": 0, "data": []}
        return data
    venue = Venue.query.filter(func.lower(Venue.name).contains(string.lower()))
    val = [{
            "id": v.id,
            "name": v.name,
            "num_upcoming_shows": len(function(v.id, now)[1])
        }
        for v in venue]
    data = {
        "count": venue.count(),
        "data": val
    }
    return data


def venue_from_form(request, venue=None):
    if venue is None:
        venue = Venue()
    venue.name = request.form.get('name')
    venue.city = request.form.get('city')
    venue.state = request.form.get('state')
    venue.address = request.form.get('address')
    venue.phone = request.form.get('phone')
    venue.genres = ';'.join(request.form.getlist('genres'))
    venue.facebook_link = request.form.get('facebook_link')
    venue.image_link = request.form.get('image_link')
    venue.website = request.form.get('website_link')
    if request.form.get('seeking_talent') == 'y':
        venue.seeking_talent = True
    else:
        venue.seeking_talent = False
    venue.seeking_description = request.form.get('seeking_description')

    return venue


def populate_artist_form(form, venue):
    form.name.data = venue.name
    form.city.data = venue.city
    form.state.data = venue.state
    form.address.data = venue.address
    form.phone.data = venue.phone
    form.genres.data = venue.genres.split(';')
    form.facebook_link.data = venue.facebook_link
    form.image_link.data = venue.image_link
    form.website_link.data = venue.website
    if venue.seeking_talent:
        form.seeking_talent.checked = True
    else:
        form.seeking_talent.checked = False
    form.seeking_description.data = venue.seeking_description

    return form