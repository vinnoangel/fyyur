from datetime import datetime
from flask_wtf import FlaskForm
from wtforms import StringField, SelectField, SelectMultipleField, DateTimeField, BooleanField, HiddenField
from wtforms.validators import DataRequired, Length, URL, ValidationError
from fyyur.models import Venue, Artist


# ensure venue ID exist
def validateVenueID(form, field):
    form = ShowForm()
    venue = Venue.query.get(form.venue_id.data)
    if venue == None:
        raise ValidationError("Invalid venue ID")
        
# ensure artist ID exist
def validateArtistID(form, field):
    form = ShowForm()
    artist = Artist.query.get(form.artist_id.data)
    if artist == None:
        raise ValidationError("Invalid artist ID")

class ShowForm(FlaskForm):
    artists = Artist.query.all()
    artist_names = tuple((artist.id, artist.name) for artist in artists)
    artist_id = SelectField('artist_id', choices=artist_names, validators=[DataRequired(), validateArtistID])

    venues = Venue.query.all()
    venue_names = tuple(( venue.id,  venue.name) for  venue in  venues)
    venue_id = SelectField(' venue_id', choices= venue_names, validators=[DataRequired(), validateVenueID])
    
    start_time = DateTimeField(
        'start_time',
        validators=[DataRequired()],
        default= datetime.today()
    )


# ensure there are no venue name duplicate
def validateVenueName(form, field):
    form = VenueForm()
    venue = Venue.query.filter_by(name=form.name.data).first()
    if venue:
        if int(form.id.data) != venue.id:
            raise ValidationError("Name already exists! Please choose another venue name.")

# ensure there are no venue address duplicate
def validateVenueAddress(form, field):
    form = VenueForm()
    venue = Venue.query.filter_by(address=form.address.data).first()
    if venue:
        if int(form.id.data) != venue.id:
            raise ValidationError("Address already exists! Please choose another venue address.")

# ensure there are no venue phone number duplicate
def validateVenuePhone(form, field):
    form = VenueForm()
    venue = Venue.query.filter_by(phone=form.phone.data).first()
    if venue:
        if int(form.id.data) != venue.id:
            raise ValidationError("Phone no. already exists! Please choose another venue phone no.")


class VenueForm(FlaskForm):
    id = HiddenField('id', default=0)
    name = StringField(
        'name', validators=[Length(min=2, max=120), DataRequired(), validateVenueName]
    )
    city = StringField(
        'city', validators=[DataRequired()]
    )
    state = SelectField(
        'state', validators=[DataRequired()],
        choices=[
            ('AL', 'AL'),
            ('AK', 'AK'),
            ('AZ', 'AZ'),
            ('AR', 'AR'),
            ('CA', 'CA'),
            ('CO', 'CO'),
            ('CT', 'CT'),
            ('DE', 'DE'),
            ('DC', 'DC'),
            ('FL', 'FL'),
            ('GA', 'GA'),
            ('HI', 'HI'),
            ('ID', 'ID'),
            ('IL', 'IL'),
            ('IN', 'IN'),
            ('IA', 'IA'),
            ('KS', 'KS'),
            ('KY', 'KY'),
            ('LA', 'LA'),
            ('ME', 'ME'),
            ('MT', 'MT'),
            ('NE', 'NE'),
            ('NV', 'NV'),
            ('NH', 'NH'),
            ('NJ', 'NJ'),
            ('NM', 'NM'),
            ('NY', 'NY'),
            ('NC', 'NC'),
            ('ND', 'ND'),
            ('OH', 'OH'),
            ('OK', 'OK'),
            ('OR', 'OR'),
            ('MD', 'MD'),
            ('MA', 'MA'),
            ('MI', 'MI'),
            ('MN', 'MN'),
            ('MS', 'MS'),
            ('MO', 'MO'),
            ('PA', 'PA'),
            ('RI', 'RI'),
            ('SC', 'SC'),
            ('SD', 'SD'),
            ('TN', 'TN'),
            ('TX', 'TX'),
            ('UT', 'UT'),
            ('VT', 'VT'),
            ('VA', 'VA'),
            ('WA', 'WA'),
            ('WV', 'WV'),
            ('WI', 'WI'),
            ('WY', 'WY'),
        ]
    )
    address = StringField(
        'address', validators=[DataRequired(), validateVenueAddress]
    )
    phone = StringField(
        'phone', validators=[DataRequired(), validateVenuePhone]
    )
    image_link = StringField(
        'image_link'
    )
    genres = SelectMultipleField(
        # TODO implement enum restriction
        'genres', validators=[DataRequired()],
        choices=[
            ('Alternative', 'Alternative'),
            ('Blues', 'Blues'),
            ('Classical', 'Classical'),
            ('Country', 'Country'),
            ('Electronic', 'Electronic'),
            ('Folk', 'Folk'),
            ('Funk', 'Funk'),
            ('Hip-Hop', 'Hip-Hop'),
            ('Heavy Metal', 'Heavy Metal'),
            ('Instrumental', 'Instrumental'),
            ('Jazz', 'Jazz'),
            ('Musical Theatre', 'Musical Theatre'),
            ('Pop', 'Pop'),
            ('Punk', 'Punk'),
            ('R&B', 'R&B'),
            ('Reggae', 'Reggae'),
            ('Rock n Roll', 'Rock n Roll'),
            ('Soul', 'Soul'),
            ('Other', 'Other'),
        ]
    )
    facebook_link = StringField(
        'facebook_link', validators=[URL()]
    )
    website_link = StringField(
        'website_link', validators=[URL()]
    )

    seeking_talent = BooleanField( 'seeking_talent' )

    seeking_description = StringField(
        'seeking_description'
    )


# ensure there are no artist name duplicate
def validateArtistName(form, field):
    form = ArtistForm()
    artist = Artist.query.filter_by(name=form.name.data).first()
    if artist:
        if int(form.id.data) != artist.id:
            raise ValidationError("Name already exists! Please choose another artist name.")

# ensure there are no artist phone number duplicate
def validateArtistPhone(form, field):
    form = ArtistForm()
    artist = Artist.query.filter_by(phone=form.phone.data).first()
    if artist:
        if int(form.id.data) != artist.id:
            print(form.id.data)
            raise ValidationError("Phone no. already exists! Please choose another artist phone no.")


class ArtistForm(FlaskForm):
    id = HiddenField('id', default=0)
    name = StringField(
        'name', validators=[DataRequired(), validateArtistName]
    )
    city = StringField(
        'city', validators=[DataRequired()]
    )
    state = SelectField(
        'state', validators=[DataRequired()],
        choices=[
            ('AL', 'AL'),
            ('AK', 'AK'),
            ('AZ', 'AZ'),
            ('AR', 'AR'),
            ('CA', 'CA'),
            ('CO', 'CO'),
            ('CT', 'CT'),
            ('DE', 'DE'),
            ('DC', 'DC'),
            ('FL', 'FL'),
            ('GA', 'GA'),
            ('HI', 'HI'),
            ('ID', 'ID'),
            ('IL', 'IL'),
            ('IN', 'IN'),
            ('IA', 'IA'),
            ('KS', 'KS'),
            ('KY', 'KY'),
            ('LA', 'LA'),
            ('ME', 'ME'),
            ('MT', 'MT'),
            ('NE', 'NE'),
            ('NV', 'NV'),
            ('NH', 'NH'),
            ('NJ', 'NJ'),
            ('NM', 'NM'),
            ('NY', 'NY'),
            ('NC', 'NC'),
            ('ND', 'ND'),
            ('OH', 'OH'),
            ('OK', 'OK'),
            ('OR', 'OR'),
            ('MD', 'MD'),
            ('MA', 'MA'),
            ('MI', 'MI'),
            ('MN', 'MN'),
            ('MS', 'MS'),
            ('MO', 'MO'),
            ('PA', 'PA'),
            ('RI', 'RI'),
            ('SC', 'SC'),
            ('SD', 'SD'),
            ('TN', 'TN'),
            ('TX', 'TX'),
            ('UT', 'UT'),
            ('VT', 'VT'),
            ('VA', 'VA'),
            ('WA', 'WA'),
            ('WV', 'WV'),
            ('WI', 'WI'),
            ('WY', 'WY'),
        ]
    )
    phone = StringField(
        # TODO implement validation logic for state
        'phone', validators=[DataRequired(), validateArtistPhone]
    )
    image_link = StringField(
        'image_link'
    )
    genres = SelectMultipleField(
        'genres', validators=[DataRequired()],
        choices=[
            ('Alternative', 'Alternative'),
            ('Blues', 'Blues'),
            ('Classical', 'Classical'),
            ('Country', 'Country'),
            ('Electronic', 'Electronic'),
            ('Folk', 'Folk'),
            ('Funk', 'Funk'),
            ('Hip-Hop', 'Hip-Hop'),
            ('Heavy Metal', 'Heavy Metal'),
            ('Instrumental', 'Instrumental'),
            ('Jazz', 'Jazz'),
            ('Musical Theatre', 'Musical Theatre'),
            ('Pop', 'Pop'),
            ('Punk', 'Punk'),
            ('R&B', 'R&B'),
            ('Reggae', 'Reggae'),
            ('Rock n Roll', 'Rock n Roll'),
            ('Soul', 'Soul'),
            ('Other', 'Other'),
        ]
     )
    facebook_link = StringField(
        # TODO implement enum restriction
        'facebook_link', validators=[URL()]
     )

    website_link = StringField(
        'website_link', validators=[URL()]
     )

    seeking_venue = BooleanField( 'seeking_venue',)

    seeking_description = StringField(
            'seeking_description'
     )