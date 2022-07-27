from sqlalchemy import func
from model import Artist, Venue, Show


def artist_from_form(request, artist=None):
    if artist is None:
        artist = Artist()
    artist.name = request.form.get('name')
    artist.city = request.form.get('city')
    artist.state = request.form.get('state')
    artist.phone = request.form.get('phone')
    artist.genres = ';'.join(request.form.getlist('genres'))
    artist.facebook_link = request.form.get('facebook_link')
    artist.image_link = request.form.get('image_link')
    artist.website = request.form.get('website_link')
    if request.form.get('seeking_venue') == 'y':
        artist.seeking_venue = True
    else:
        artist.seeking_venue = False
    artist.seeking_description = request.form.get('seeking_description')

    return artist


def populate_artist_form(form, artist):
    form.name.data = artist.name
    form.city.data = artist.city
    form.state.data = artist.state
    form.phone.data = artist.phone
    form.genres.data = artist.genres.split(';')
    form.facebook_link.data = artist.facebook_link
    form.image_link.data = artist.image_link
    form.website_link.data = artist.website
    if artist.seeking_venue:
        form.seeking_venue.checked = True
    else:
        form.seeking_venue.checked = False
    form.seeking_description.data = artist.seeking_description

    return form


def collect_all_artist():
    artist = Artist.query.all()
    data = []
    for art in artist:
        val = {
            "id": art.id,
            "name": art.name,
        }
        data.append(val)
    return data


def search_artist_by_string(string, function, now):
    if string is None or len(string) < 1:
        data = {"count": 0, "data": []}
        return data
    artist = Artist.query.filter(func.lower(Artist.name).contains(string.lower()))
    val = [{
            "id": art.id,
            "name": art.name,
            "num_upcoming_shows": len(function(art.id, now)[1])
        }
        for art in artist]
    data = {
        "count": artist.count(),
        "data": val
    }

    return data