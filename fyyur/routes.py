# Imports
#----------------------------------------------------------------------------#

from fyyur import app
from flask import render_template, request, flash, redirect, url_for
from fyyur import db
from fyyur.models import Artist, Venue, Show
from fyyur.forms import VenueForm, ArtistForm, ShowForm
from datetime import datetime
import sys
import logging
from logging import Formatter, FileHandler
from fyyur.filters import convertToBool, convertToList, convertToString

#----------------------------------------------------------------------------#
# Controllers.
#----------------------------------------------------------------------------#

@app.route('/')
def index():
  artists = Artist.query.order_by(Artist.id.desc()).limit(10).all()
  venues = Venue.query.order_by(Venue.id.desc()).limit(10).all()
  return render_template('pages/home.html', artists=artists, venues=venues)


#  Venues
#  ----------------------------------------------------------------

#  Retireve All Venues
#  ----------------------------------------------------------------
@app.route('/venues')
def venues():
  # TODO: replace with real venues data.
  #       num_upcoming_shows should be aggregated based on number of upcoming shows per venue.

  data = Venue.query.with_entities(Venue.city, Venue.state)\
    .group_by(Venue.city, Venue.state)\
    .order_by('state', 'city')\
    .all()

  result = []
  for d in data:
    venues = db.session.query(Venue)\
    .filter(Venue.city == d.city)\
    .filter(Venue.state == d.state)\
    .all()
    
    result.append({"city": d.city, "state": d.state, "venues": venues})
    
  return render_template('pages/venues.html', areas=result);

#  Retireve Single Venue By ID
#  ----------------------------------------------------------------
@app.route('/venues/<int:venue_id>')
def show_venue(venue_id):
      # shows the venue page with the given venue_id
  # TODO: replace with real venue data from the venues table, using venue_id
  venue = Venue.query.get(venue_id)

  # fetch all past and upcoming shows
  past_shows = []
  upcoming_shows = []
  for show in venue.shows:
    if show.start_time < datetime.today():
      past_shows.append({
        "artist_id": show.artist_id,
        "artist_name": show.artist.name,
        "artist_image_link": show.artist.image_link,
        "start_time": str(show.start_time)
      })
    else:
      upcoming_shows.append({
        "artist_id": show.artist.id,
        "artist_name": show.artist.name,
        "artist_image_link": show.artist.image_link,
        "start_time": str(show.start_time)
      })

  data = {
    "id": venue.id,
    "name": venue.name,
    "genres": convertToList(venue.genres),
    "city": venue.city,
    "state": venue.state,
    "address": venue.address,
    "phone": venue.phone,
    "facebook_link": venue.facebook_link,
    "seeking_talent": venue.seeking_talent,
    "seeking_description": venue.seeking_description,
    "image_link": venue.image_link,
    "website_link": venue.website_link,
    "past_shows": past_shows,
    "upcoming_shows": upcoming_shows,
    "past_shows_count": len(past_shows),
    "upcoming_shows_count": len(upcoming_shows),
  }
  
  return render_template('pages/show_venue.html', venue=data)

#  Search Venue
#  ----------------------------------------------------------------
@app.route('/venues/search', methods=['POST'])
def search_venues():
  # TODO: implement search on venues with partial string search. Ensure it is case-insensitive.
  # seach for Hop should return "The Musical Hop".
  # search for "Music" should return "The Musical Hop" and "Park Square Live Music & Coffee"
  search_term = request.form.get('search_term', '')
  searched_term = "%{}%".format(search_term)
  data = Venue.query.filter(Venue.name.ilike(searched_term)).all()
  response = {
    "count": len(data),
    "data": data
  }

  return render_template('pages/search_venues.html', results=response, search_term=search_term)

#  Create Venue
#  ----------------------------------------------------------------
@app.route('/venues/create', methods=['GET', 'POST'])
def create_venue():
  # TODO: insert form data as a new Venue record in the db, instead
  error = False        
  form = VenueForm()
  # form.id.data = 220
  if request.method == 'GET':
    return render_template('forms/new_venue.html', form=form)
  else:
    try:
      if form.validate_on_submit():
        data = Venue(
          name=form.name.data,
          city=form.city.data,
          state=form.state.data,
          address=form.address.data,
          phone=form.phone.data,
          genres=convertToString(form.genres.data),
          facebook_link=form.facebook_link.data,
          image_link=form.image_link.data,
          website_link=form.website_link.data,
          seeking_description=form.seeking_description.data,
          seeking_talent=convertToBool(form.seeking_talent.data)
        )
        db.session.add(data)
        db.session.commit()

      if form.errors: #If there are errors from the validations
        error = True
        for err_msg in form.errors.values():
          flash(f'An error occurred. Reason: {err_msg}', category='danger')
    except:
      error = True
      db.session.rollback()
      flash(sys.exc_info(), category='danger')
    finally:
      db.session.close()
      if error:
        return render_template('forms/new_venue.html', form=form)
      else:
        flash('Venue ' + request.form['name'] + ' was successfully listed!', category='success')
        # redirect user to the home page
        return redirect(url_for('index'))

#  Update Venue
#  ----------------------------------------------------------------
@app.route('/venues/<int:venue_id>/edit', methods=['GET', 'POST'])
def edit_venue(venue_id):
  error = False
  form = VenueForm()
  venue = Venue.query.get(venue_id)

  # check if venue exist
  if venue == None:
    flash('Venue with ID ' + str(venue_id) + ' not found', category='warning')
    return redirect(url_for("venues"))

  if request.method == 'GET':
    form.id.data = venue.id
    form.name.data = venue.name
    form.city.data = venue.city
    form.state.data = venue.state
    form.address.data = venue.address
    form.phone.data = venue.phone
    form.genres.data = venue.genres
    form.facebook_link.data = venue.facebook_link
    form.image_link.data = venue.image_link
    form.website_link.data = venue.website_link
    form.seeking_talent.data = venue.seeking_talent
    form.seeking_description.data = venue.seeking_description
  else:
    try:
      if form.validate_on_submit():
        # modify venue record
        venue.name = request.form.get("name") 
        venue.city = request.form.get("city")
        venue.state = request.form.get("state") 
        venue.address = request.form.get("address")
        venue.phone = request.form.get("phone")
        venue.genres = convertToString(request.form.getlist("genres")) 
        venue.facebook_link = request.form.get("facebook_link")
        venue.image_link = request.form.get("image_link") 
        venue.website_link = request.form.get("website_link")
        venue.seeking_talent = convertToBool(request.form.get("seeking_talent")) 
        venue.seeking_description = request.form.get("seeking_description") 
        # save to database
        db.session.commit()
        # alert user 
        flash('Venue updated successfully!', category='success')

      if form.errors:
        error = True
        for err_msg in form.errors.values():
          flash(f'An error occurred. Reason: {err_msg}', category='danger')
    except:
      error = True
      db.session.rollback()
      flash(sys.exc_info(), category='danger')
    finally:
      # db.session.close()
      if error == False:
        # redirect user to the current venue page
        return redirect(url_for('show_venue', venue_id=venue_id)) 

  # TODO: populate form with fields from venue with ID <venue_id>
  return render_template('forms/edit_venue.html', form=form, venue=venue)

# Delete Venue
# ----------------------------------------------------------------
@app.route('/venues/<venue_id>', methods=['DELETE'])
def delete_venue(venue_id):
  # TODO: Complete this endpoint for taking a venue_id, and using
  # SQLAlchemy ORM to delete a record. Handle cases where the session commit could fail.
  error = True
  try:
    venue = Venue.query.get(venue_id)
    if venue:
      name = venue.name
      db.session.delete(venue)
      db.session.commit()
      flash(f'Venue: {name} - was deleted successfully', category="success")
    else:
      error = True
      flash("Venue ID: {venue_id} not found", category="danger")
  except:
    error = True
    db.session.rollback()
    flash(sys.exc_info(), category='danger')
  finally:
    db.session.close()
    if error:
      return redirect(url_for('venues'))  

  # BONUS CHALLENGE: Implement a button to delete a Venue on a Venue Page, have it so that
  # clicking that button delete it from the db then redirect the user to the homepage
  return redirect(url_for('index'))

#  Artists
#  ----------------------------------------------------------------

#  Retrieve All Artist
#  ----------------------------------------------------------------
@app.route('/artists')
def artists():
  data = Artist.query.order_by(Artist.id.desc()).all()
  return render_template('pages/artists.html', artists=data)

#  Retrieve Single Artist By ID
#  ----------------------------------------------------------------
@app.route('/artists/<int:artist_id>/')
@app.route('/artists/<int:artist_id>')
def show_artist(artist_id):
  # shows the artist page with the given artist_id
  # TODO: replace with real artist data from the artist table, using artist_id
  artist = Artist.query.get(artist_id)

  # fetch all past and upcoming shows
  past_shows = []
  upcoming_shows = []
  for show in artist.shows:
    if show.start_time < datetime.today():
      past_shows.append({
        "venue_id": show.venue_id,
        "venue_name": show.venue.name,
        "venue_image_link": show.venue.image_link,
        "start_time": str(show.start_time)
      })
    else:
      upcoming_shows.append({
        "venue_id": show.venue.id,
        "venue_name": show.venue.name,
        "venue_image_link": show.venue.image_link,
        "start_time": str(show.start_time)
      })

  data = {
    "id": artist.id,
    "name": artist.name,
    "genres": convertToList(artist.genres),
    "city": artist.city,
    "state": artist.state,
    "phone": artist.phone,
    "facebook_link": artist.facebook_link,
    "seeking_venue": artist.seeking_venue,
    "seeking_description": artist.seeking_description,
    "image_link": artist.image_link,
    "website_link": artist.website_link,
    "past_shows": past_shows,
    "upcoming_shows": upcoming_shows,
    "past_shows_count": len(past_shows),
    "upcoming_shows_count": len(upcoming_shows),
  }
  
  return render_template('pages/show_artist.html', artist=data)

#  Search Artist
#  ----------------------------------------------------------------
@app.route('/artists/search', methods=['POST'])
def search_artists():
  # TODO: implement search on artists with partial string search. Ensure it is case-insensitive.
  # seach for "A" should return "Guns N Petals", "Matt Quevado", and "The Wild Sax Band".
  # search for "band" should return "The Wild Sax Band".
  search_term = request.form.get('search_term', '')
  searched_term = "%{}%".format(search_term)
  data = Artist.query.filter(Artist.name.ilike(searched_term)).all()
  response = {
    "count": len(data),
    "data": data
  }

  return render_template('pages/search_artists.html', results=response, search_term=search_term)

#  Create Artist
#  ----------------------------------------------------------------
@app.route('/artists/create', methods=['GET', 'POST'])
def create_artist():
  error = False        
  form = ArtistForm()
  # form.id.data = 220
  if request.method == 'GET':
    return render_template('forms/new_artist.html', form=form)
  else:
    try:
      if form.validate_on_submit():
        data = Artist(
          name=form.name.data,
          city=form.city.data,
          state=form.state.data,
          phone=form.phone.data,
          genres=convertToString(form.genres.data),
          facebook_link=form.facebook_link.data,
          image_link=form.image_link.data,
          website_link=form.website_link.data,
          seeking_description=form.seeking_description.data,
          seeking_venue=convertToBool(form.seeking_venue.data)
        )
        db.session.add(data)
        db.session.commit()

      if form.errors: #If there are errors from the validations
        error = True
        for err_msg in form.errors.values():
          flash(f'An error occurred. Reason: {err_msg}', category='danger')
    except:
      error = True
      db.session.rollback()
      flash(sys.exc_info(), category='danger')
    finally:
      db.session.close()
      if error:
        return render_template('forms/new_artist.html', form=form)
      else:
        flash('Artist ' + request.form['name'] + ' was successfully listed!', category='success')
        # redirect user to the home page
        return redirect(url_for('index'))

#  Update Artist
#  ----------------------------------------------------------------
@app.route('/artists/<int:artist_id>/edit', methods=['GET', 'POST'])
def edit_artist(artist_id):
  error = False
  form = ArtistForm()
  artist = Artist.query.get(artist_id)

  # check if artist exist
  if artist == None:
    flash('Artist with ID ' + str(artist_id) + ' not found', category='warning')
    return redirect(url_for("artists"))

  if request.method == 'GET':
    form.id.data = artist.id
    form.name.data = artist.name
    form.city.data = artist.city
    form.state.data = artist.state
    form.phone.data = artist.phone
    form.genres.data = artist.genres
    form.facebook_link.data = artist.facebook_link
    form.image_link.data = artist.image_link
    form.website_link.data = artist.website_link
    form.seeking_venue.data = artist.seeking_venue
    form.seeking_description.data = artist.seeking_description
  else:
    try:
      if form.validate_on_submit():
        # modify artist record
        artist.name = request.form.get("name") 
        artist.city = request.form.get("city")
        artist.state = request.form.get("state") 
        artist.phone = request.form.get("phone")
        artist.genres = convertToString(request.form.getlist("genres"))
        artist.facebook_link = request.form.get("facebook_link")
        artist.image_link = request.form.get("image_link") 
        artist.website_link = request.form.get("website_link")
        artist.seeking_venue = convertToBool(request.form.get("seeking_venue")) 
        artist.seeking_description = request.form.get("seeking_description") 
        # save to database
        db.session.commit()
        # alert user 
        flash('Artist updated successfully!', category='success')

      if form.errors:
        error = True
        for err_msg in form.errors.values():
          flash(f'An error occurred. Reason: {err_msg}', category='danger')
    except:
      error = True
      db.session.rollback()
      flash(sys.exc_info(), category='danger')
    finally:
      # db.session.close()
      if error == False:
        # redirect user to the current artist page
        return redirect(url_for('show_artist', artist_id=artist_id)) 

  # TODO: populate form with fields from artist with ID <artist_id>
  return render_template('forms/edit_artist.html', form=form, artist=artist)

# Delete Artist
# ----------------------------------------------------------------
@app.route('/artists/<artist_id>', methods=['DELETE'])
def delete_artist(artist_id):
  # TODO: Complete this endpoint for taking a artist_id, and using
  # SQLAlchemy ORM to delete a record. Handle cases where the session commit could fail.
  error = True
  try:
    artist = Artist.query.get(artist_id)
    if artist:
      name = artist.name
      db.session.delete(artist)
      db.session.commit()
      flash(f'Artist: {name} - was deleted successfully', category="success")
    else:
      error = True
      flash("Artist ID: {artist_id} not found", category="danger")
  except:
    error = True
    db.session.rollback()
    flash(sys.exc_info(), category='danger')
  finally:
    db.session.close()
    if error:
      return redirect(url_for('artists'))

  return redirect(url_for('index'))


#  Shows
#  ----------------------------------------------------------------

#  Retrieve All Shows
#  ----------------------------------------------------------------
@app.route('/shows')
def shows():
  # displays list of shows at /shows
  # TODO: replace with real venues data.
  data=[]
  shows = Show.query.order_by(Show.id.desc()).all()
  for show in shows:
    data.append({
      "id": show.id,
      "venue_id": show.venue_id,
      "venue_name": (show.venue).name,
      "artist_id": show.artist_id,
      "artist_name": (show.artist).name,
      "artist_image_link": (show.artist).image_link,
      "start_time": str(show.start_time)
    })

  return render_template('pages/shows.html', shows=data)

@app.route('/shows/create')
def create_shows():
  # renders form. do not touch.
  form = ShowForm()
  return render_template('forms/new_show.html', form=form)

# Create new Show
@app.route('/shows/create', methods=['POST'])
def create_show_submission():
  error = False        
  form = ShowForm()

  try:
    if form.validate_on_submit():
      data = Show(
        artist_id=int(form.artist_id.data),
        venue_id=int(form.venue_id.data),
        start_time=form.start_time.data,
      )
      db.session.add(data)
      db.session.commit()

    if form.errors: #If there are errors from the validations
      error = True
      for err_msg in form.errors.values():
        flash(f'An error occurred. Reason: {err_msg}', category='danger')
  except:
    error = True
    db.session.rollback()
    flash(sys.exc_info(), category='danger')
  finally:
    db.session.close()
    if error:
      return render_template('forms/new_show.html', form=form)
    else:
      flash('Show was successfully listed!', category='success')
      # redirect user to the home page
      return redirect(url_for('index'))

# Delete Show
# ----------------------------------------------------------------
@app.route('/shows/<show_id>', methods=['DELETE'])
def delete_show(show_id):
  # TODO: Complete this endpoint for taking a show_id, and using
  # SQLAlchemy ORM to delete a record. Handle cases where the session commit could fail.
  error = True
  try:
    show = Show.query.get(show_id)
    if show:
      db.session.delete(show)
      db.session.commit()
      flash(f'Show was deleted successfully', category="success")
    else:
      error = True
      flash("Show ID: {show_id} not found", category="danger")
  except:
    error = True
    db.session.rollback()
    flash(sys.exc_info(), category='danger')
  finally:
    db.session.close()
    if error:
      return redirect(url_for('shows'))

  return redirect(url_for('shows'))

# Handle Unknow url (Page not found)
@app.errorhandler(404)
def not_found_error(error):
    return render_template('errors/404.html'), 404

# Handle Server Internal Error
@app.errorhandler(500)
def server_error(error):
  return render_template('errors/500.html'), 500


if not app.debug:
  file_handler = FileHandler('error.log')
  file_handler.setFormatter(
      Formatter('%(asctime)s %(levelname)s: %(message)s [in %(pathname)s:%(lineno)d]')
  )
  app.logger.setLevel(logging.INFO)
  file_handler.setLevel(logging.INFO)
  app.logger.addHandler(file_handler)
  app.logger.info('errors')