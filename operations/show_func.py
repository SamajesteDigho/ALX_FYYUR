from model import Artist, Venue, Show


def show_from_form(request, date_format):
    show = Show()
    artist = Artist.query.get(request.form.get('artist_id'))
    venue = Venue.query.get(request.form.get('venue_id'))
    if artist and venue:
        show.artist_id = artist.id
        show.venue_id = venue.id
        show.start_date = date_format(request.form.get('start_time'), 'full')
    else:
        show = None

    return show


def collect_past_upcoming_show_by_artist(artist_id, now):
    shows = Show.query.filter_by(artist_id=artist_id).filter(Show.start_date < now)
    pastshow = []
    for s in shows:
        val = {
            "venue_id": s.venue.id,
            "venue_name": s.venue.name,
            "venue_image_link": s.venue.image_link,
            "start_time": str(s.start_date)
        }
        pastshow.append(val)
    shows = Show.query.filter_by(artist_id=artist_id).filter(Show.start_date > now)
    upcomingshow = []
    for s in shows:
        val = {
            "venue_id": s.venue.id,
            "venue_name": s.venue.name,
            "venue_image_link": s.venue.image_link,
            "start_time": str(s.start_date)
        }
        upcomingshow.append(val)
    return pastshow, upcomingshow


def collect_past_upcoming_show_by_venue(venue_id, now):
    shows = Show.query.filter_by(venue_id=venue_id).filter(Show.start_date < now)
    pastshow = []
    for s in shows:
        val = {
            "artist_id": s.artist.id,
            "artist_name": s.artist.name,
            "artist_image_link": s.artist.image_link,
            "start_time": str(s.start_date)
        }
        pastshow.append(val)
    shows = Show.query.filter_by(venue_id=venue_id).filter(Show.start_date > now)
    upcomingshow = []
    for s in shows:
        val = {
            "artist_id": s.artist.id,
            "artist_name": s.artist.name,
            "artist_image_link": s.artist.image_link,
            "start_time": str(s.start_date)
        }
        upcomingshow.append(val)
    return pastshow, upcomingshow
