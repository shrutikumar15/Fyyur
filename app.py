#----------------------------------------------------------------------------#
# Imports
#----------------------------------------------------------------------------#

import json
import dateutil.parser
import babel
from flask import Flask, render_template, request, Response, flash, redirect, url_for
from flask_moment import Moment
from flask_sqlalchemy import SQLAlchemy
import logging
from logging import Formatter, FileHandler
from flask_wtf import FlaskForm
from forms import *
from sqlalchemy import func
from sqlalchemy.exc import SQLAlchemyError
from sqlalchemy.orm import aliased
from flask_migrate import Migrate
from sqlalchemy.orm.exc import NoResultFound
from werkzeug.exceptions import abort
from models import Venue

#----------------------------------------------------------------------------#
# App Config.
#----------------------------------------------------------------------------#

app = Flask(__name__)
moment = Moment(app)
app.config.from_object('config')
db = SQLAlchemy(app)
migrate = Migrate(app, db)

with app.app_context():
    db.init_app(app)
# TODO: connect to a local postgresql database

#----------------------------------------------------------------------------#
# Models.
#----------------------------------------------------------------------------#


class Venue(db.Model):
    __tablename__ = 'Venue'
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String)
    city = db.Column(db.String(120))
    state = db.Column(db.String(120))
    address = db.Column(db.String(120))
    phone = db.Column(db.String(120))
    genres = db.Column(db.ARRAY(db.String))
    image_link = db.Column(db.String(500))
    facebook_link = db.Column(db.String(120))
    website_link = db.Column(db.String(120))
    seeking_talent = db.Column(db.Boolean)
    seeking_description = db.Column(db.String(500))
    shows = db.relationship('Show', backref='Venue', lazy='dynamic')
    #areas = db.relationship('Area', backref='Venue', lazy='dynamic')

    def search(self):
        return{
            'id': self.id,
            'name': self.name,
        }

    def details(self):
        genress = []
        s = ""
        self.genres += ','
        for i in self.genres:
            if i != ',':
                if i != '"' and i != '{' and i != '}':
                    s += i
            else:
                genress.append(s)
                s = ""
        return{
            'id': self.id,
            'name': self.name,
            'genres': genress,
            'address': self.address,
            'city': self.city,
            'state': self.state,
            'phone': self.phone,
            'website_link': self.website_link,
            'facebook_link': self.facebook_link,
            'seeking_talent': self.seeking_talent,
            'seeking_description': self.seeking_description,
            'image_link': self.image_link,

        }


class Artist(db.Model):
    __tablename__ = 'Artist'
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String)
    genres = db.Column(db.ARRAY(db.String))
    city = db.Column(db.String(120))
    state = db.Column(db.String(120))
    phone = db.Column(db.String(120))
    website_link = db.Column(db.String)
    facebook_link = db.Column(db.String(120))
    seeking_venue = db.Column(db.Boolean)
    seeking_description = db.Column(db.String(500))
    image_link = db.Column(db.String(500))
    shows = db.relationship('Show', backref='Artist', lazy='dynamic')

    # TODO: implement any missing fields, as a database migration using Flask-Migrate
    def search(self):
        return{
            'id': self.id,
            'name': self.name,
        }

    def details(self):
        genress = []
        s = ""
        self.genres += ','
        for i in self.genres:
            if i != ',':
                if i != '"' and i != '{' and i != '}':
                    s += i
            else:
                genress.append(s)
                s = ""
        return{
            'id': self.id,
            'name': self.name,
            'genres': genress,
            'city': self.city,
            'state': self.state,
            'phone': self.phone,
            'website_link': self.website_link,
            'facebook_link': self.facebook_link,
            'seeking_venue': self.seeking_venue,
            'seeking_description': self.seeking_description,
            'image_link': self.image_link,

        }


class Show(db.Model):
    __tablename__ = 'Show'
    id = db.Column(db.Integer, primary_key=True)
    venue_id = db.Column(db.Integer, db.ForeignKey('Venue.id'), nullable=False)
    artist_id = db.Column(db.Integer, db.ForeignKey(
        'Artist.id'), nullable=False)
    start_time = db.Column(db.DateTime, nullable=False)

    def details_artist(self):
        return {
            'artist_id': self.artist_id,
            'artist_name': self.Artist.name,
            'artist_image_link': self.Artist.image_link,
            'start_time': self.start_time
        }

    def details_venue(self):
        return {
            'venue_id': self.venue_id,
            'venue_name': self.Venue.name,
            'venue_image_link': self.Venue.image_link,
            'start_time': self.start_time
        }

    def details(self):
        return {
            'venue_id': self.venue_id,
            'venue_name': self.Venue.name,
            'artist_id': self.artist_id,
            'artist_name': self.Artist.name,
            'artist_image_link': self.Artist.image_link,
            'start_time': self.start_time
        }


class Area(db.Model):
    __tablename__ = 'Area'
    id = db.Column(db.Integer, primary_key=True)
    city = db.Column(db.String(120),  nullable=False)
    state = db.Column(db.String(120),  nullable=False)
    venues = db.Column(db.ARRAY(db.String), nullable=False)
    ids = db.Column(db.ARRAY(db.Integer), nullable=False)


# TODO Implement Show and Artist models, and complete all model relationships and properties, as a database migration.

#----------------------------------------------------------------------------#
# Filters.
#----------------------------------------------------------------------------#


def format_datetime(value, format='medium'):
    date = dateutil.parser.parse(value)
    if format == 'full':
        format = "EEEE MMMM, d, y 'at' h:mma"
    elif format == 'medium':
        format = "EE MM, dd, y h:mma"
    return babel.dates.format_datetime(date, format)


app.jinja_env.filters['datetime'] = format_datetime

#----------------------------------------------------------------------------#
# Controllers.
#----------------------------------------------------------------------------#


@app.route('/')
def index():
    return render_template('pages/home.html')


#  Venues
#  ----------------------------------------------------------------

@app.route('/venues')
def venues():
    # TODO: replace with real venues data.
    #       num_shows should be aggregated based on number of upcoming shows per venue.
    form = VenueForm()
    data = Area.query.order_by(Area.city)
    return render_template('pages/venues.html', areas=(data))


@app.route('/venues/search', methods=['POST'])
def search_venues():
    # TODO: implement search on artists with partial string search. Ensure it is case-insensitive.
    # seach for Hop should return "The Musical Hop".
    # search for "Music" should return "The Musical Hop" and "Park Square Live Music & Coffee"
    venue_query = Venue.query.filter(
        Venue.name.ilike('%' + request.form['search_term'] + '%'))
    print(venue_query)
    venue_list = list(map(Venue.search, venue_query))
    response = {
        "count": len(venue_list),
        "data": venue_list
    }
    return render_template('pages/search_venues.html', results=response, search_term=request.form.get('search_term', ''))


@app.route('/venues/<int:venue_id>')
def show_venue(venue_id):
    # shows the venue page with the given venue_id
    # TODO: replace with real venue data from the venues table, using venue_id
    form = VenueForm()
    venue_query = Venue.query.get(venue_id)
    if venue_query:
        venue_details = Venue.details(venue_query)
        current_time = datetime.now().strftime('%Y-%m-%d')
        new_shows_query = Show.query.options(db.joinedload('Artist')).filter(
            Show.venue_id == venue_id).filter(Show.start_time > current_time).all()
        new_show = list(map(Show.details_artist, new_shows_query))
        venue_details["upcoming_shows"] = new_show
        venue_details["upcoming_shows_count"] = len(new_show)
        past_shows_query = Show.query.options(db.joinedload('Artist')).filter(
            Show.venue_id == venue_id).filter(Show.start_time <= current_time).all()
        past_shows = list(map(Show.details_artist, past_shows_query))
        venue_details["past_shows"] = past_shows
        venue_details["past_shows_count"] = len(past_shows)
        print(venue_details)
        upcoming_shows_query = Show.query.options(db.joinedload('Artist')).filter(
            Show.venue_id == venue_id).filter(Show.start_time >= current_time).all()
        return render_template('pages/show_venue.html', venue=venue_details)
    return render_template('errors/404.html')

#  Create Venue
#  ----------------------------------------------------------------


@app.route('/venues/create', methods=['GET'])
def create_venue_form():
    form = VenueForm()
    return render_template('forms/new_venue.html', form=form)


@app.route('/venues/create', methods=['POST'])
def create_venue_submission():
    # TODO: insert form data as a new Venue record in the db, instead
    # TODO: modify data to be the data object returned from db insertion
    # on successful db insert, flash success
    data = request.form
    try:
        new_venue = Venue(
            genres=data.getlist("genres"),
            name=data.get("name"),
            address=data.get("address"),
            city=data.get("city"),
            state=data.get("state"),
            facebook_link=data.get("facebook_link"),
            phone=data.get("phone"),
            website_link=data.get("website_link"),
            image_link=data.get("image_link"))
        db.session.add(new_venue)
        db.session.commit()
        flash('Venue ' + request.form['name'] + ' was successfully listed!')
    except SQLAlchemyError as e:
        flash('An error occurred. Venue ' +
              request.form['name'] + ' could not be listed.')
    try:

        exists = Area.query.filter_by(city=data.get("city")).first()
        print(exists)
        # for ex in exists:
        #print (yes)
        v_id = Venue.query.filter_by(name=data.get("name")).first()
        id = v_id.id
        if exists is None:
            print("yes")
            list_venue = []
            list_id = []
            list_venue.append(data.get("name"))
            list_id.append(id)
            new_area = Area(
                city=data.get("city"),
                state=data.get("state"),
                venues=list_venue,
                ids=list_id
            )
            db.session.add(new_area)
            db.session.commit()
        else:
            # Area.query.filter_by(city=data.get("city")).first().update({"venues":ven})
            ven = exists.venues
            ven.append(data.get("name"))
            id_l = exists.ids
            id_l.append(id)
            # temp.append(data.get("name"))
            db.session.query(Area).filter_by(
                city=data.get("city")).update({"venues": ven})
            db.session.query(Area).filter_by(
                city=data.get("city")).update({"ids": id_l})
            #exists.venues = ven
            db.session.commit()
            pass

    except SQLAlchemyError as e:
        print(e)
        flash('An error occurred. Area ' +
              request.form['name'] + ' could not be listed.')
    return render_template('pages/home.html')

    # TODO: on unsuccessful db insert, flash an error instead.
    # e.g., flash('An error occurred. Venue ' + data.name + ' could not be listed.')
    # see: http://flask.pocoo.org/docs/1.0/patterns/flashing/


@app.route('/venues/<venue_id>', methods=['POST'])
def delete_venue(venue_id):
    # TODO: Complete this endpoint for taking a venue_id, and using
    # SQLAlchemy ORM to delete a record. Handle cases where the session commit could fail.
    try:
        ven = Venue.query.filter_by(id=venue_id).first()
        print(ven)
        area = Area.query.filter_by(city=ven.city).first()
        print(area)
        if area is not None:
            l_venues = area.venues
            l_ids = area.ids
            l_venues.remove(ven.name)
            l_ids.remove(ven.id)
            db.session.query(Area).filter_by(
                city=ven.city).update({"venues": l_venues})
            db.session.query(Area).filter_by(city=ven.city).update({"ids": l_ids})        
        Venue.query.filter_by(id=venue_id).delete()
        db.session.commit()
        flash(' Venue successfully deleted.')
        return render_template('pages/home.html')
    except SQLAlchemyError as e:
        print(e)
        flash('An error occurred. Venue  could not be deleted.')
        return render_template('pages/home.html')
    # BONUS CHALLENGE: Implement a button to delete a Venue on a Venue Page, have it so that
    # clicking that button delete it from the db then redirect the user to the homepage
    return render_template('pages/home.html')

#  Artists
#  ----------------------------------------------------------------
@app.route('/artists')
def artists():
    # TODO: replace with real data returned from querying the database
    form = ArtistForm()
    data = Artist.query.all()
    return render_template('pages/artists.html', artists=data)


@app.route('/artists/search', methods=['POST'])
def search_artists():
    # TODO: implement search on artists with partial string search. Ensure it is case-insensitive.
    # seach for "A" should return "Guns N Petals", "Matt Quevado", and "The Wild Sax Band".
    # search for "band" should return "The Wild Sax Band".
    artist_query = Artist.query.filter(
        Artist.name.ilike('%' + request.form['search_term'] + '%'))
    print(artist_query)
    artist_list = list(map(Artist.search, artist_query))
    response = {
        "count": len(artist_list),
        "data": artist_list
    }
    return render_template('pages/search_artists.html', results=response, search_term=request.form.get('search_term', ''))


@app.route('/artists/<int:artist_id>')
def show_artist(artist_id):
    # shows the venue page with the given venue_id
    # TODO: replace with real venue data from the venues table, using venue_id
    form = ArtistForm()
    artist_query = Artist.query.get(artist_id)
    if artist_query:
        artist_details = Artist.details(artist_query)
        current_time = datetime.now().strftime('%Y-%m-%d')
        upcoming_shows_query = Show.query.options(db.joinedload('Artist')).filter(
            Show.artist_id == artist_id).filter(Show.start_time >= current_time).all()
        for query in upcoming_shows_query:
            print(query.id)
            print(query.artist_id)
            print(query.venue_id)
            print(query.start_time)
        upcoming_shows_list = list(
            map(Show.details_venue, upcoming_shows_query))
        artist_details["upcoming_shows"] = upcoming_shows_list
        artist_details["upcoming_shows_count"] = len(upcoming_shows_list)
        past_shows_query = Show.query.options(db.joinedload('Artist')).filter(
            Show.artist_id == artist_id).filter(Show.start_time <= current_time).all()
        past_shows_list = list(map(Show.details_venue, past_shows_query))
        artist_details["past_shows"] = past_shows_list
        artist_details["past_shows_count"] = len(past_shows_list)
        print(artist_details)
        return render_template('pages/show_artist.html', artist=artist_details)
    return render_template('errors/404.html')

#  Update
#  ----------------------------------------------------------------
@app.route('/artists/<int:artist_id>/edit', methods=['GET'])
def edit_artist(artist_id):
    artist = Artist.query.get(artist_id)
    print(artist.genres)
    genress = []
    s = ""
    artist.genres += ','
    for i in artist.genres:
        if i != ',':
            if i != '"' and i != '{' and i != '}':
                s += i
            else:
                genress.append(s)
                s = ""
    artist.genres = genress
    print(artist.genres)
    # TODO: populate form with fields from artist with ID <artist_id>
    return render_template('forms/edit_artist.html', artist=artist)


@app.route('/artists/<int:artist_id>/edit', methods=['POST'])
def edit_artist_submission(artist_id):
    # TODO: take values from the form submitted, and update existing
    # artist record with ID <artist_id> using the new attributes
    data = request.form
    try:
        name = data.get("name")
        city = data.get("city")
        state = data.get("state")
        phone = data.get("phone")
        genres = data.getlist("genres")  
        facebook_link = data.get("facebook_link")
        image_link = data.get("image_link")
        website_link = data.get("website_link")
        artist = Artist.query.get(artist_id)
        db.session.query(Artist).filter_by(id=artist_id).update({"name": name})
        db.session.query(Artist).filter_by(id=artist_id).update({"city": city})
        db.session.query(Artist).filter_by(id=artist_id).update({"state": state})
        db.session.query(Artist).filter_by(id=artist_id).update({"phone": phone})
        db.session.query(Artist).filter_by(id=artist_id).update({"genres": genres})
        db.session.query(Artist).filter_by(id=artist_id).update({"facebook_link": facebook_link})
        db.session.query(Artist).filter_by(id=artist_id).update({"image_link": image_link})
        db.session.query(Artist).filter_by(id=artist_id).update({"website_link": website_link})
        db.session.commit()
        flash('Artist'+ name + 'successfully updated!')
    except SQLAlchemyError as e:
        flash('Artist'+ name + 'could not be successfully updated. Please try again.')
    #artist.update({"name": name})  
    return redirect(url_for('show_artist', artist_id=artist_id))


@app.route('/venues/<int:venue_id>/edit', methods=['GET'])
def edit_venue(venue_id):
    venue = Venue.query.get(venue_id)
    print(venue.genres)
    genress = []
    s = ""
    venue.genres += ','
    for i in venue.genres:
        if i != ',':
            if i != '"' and i != '{' and i != '}':
                s += i
            else:
                genress.append(s)
                s = ""
    print (genress)
    #venue.genres = genress
    print(venue.genres)
    # TODO: populate form with values from venue with ID <venue_id>
    return render_template('forms/edit_venue.html', venue=venue)


@app.route('/venues/<int:venue_id>/edit', methods=['POST'])
def edit_venue_submission(venue_id):
    # TODO: take values from the form submitted, and update existing
    # venue record with ID <venue_id> using the new attributes
    data = request.form
    try:
        name = data.get("name")
        city = data.get("city")
        state = data.get("state")
        address = data.get("address")
        phone = data.get("phone")
        genres = data.getlist("genres")  
        facebook_link = data.get("facebook_link")
        image_link = data.get("image_link")
        website_link = data.get("website_link")
        venue = Venue.query.get(venue_id)
        db.session.query(Venue).filter_by(id=venue_id).update({"name": name})
        db.session.query(Venue).filter_by(id=venue_id).update({"city": city})
        db.session.query(Venue).filter_by(id=venue_id).update({"state": state})
        db.session.query(Venue).filter_by(id=venue_id).update({"address": address})
        db.session.query(Venue).filter_by(id=venue_id).update({"phone": phone})
        db.session.query(Venue).filter_by(id=venue_id).update({"genres": genres})
        db.session.query(Venue).filter_by(id=venue_id).update({"facebook_link": facebook_link})
        db.session.query(Venue).filter_by(id=venue_id).update({"image_link": image_link})
        db.session.query(Venue).filter_by(id=venue_id).update({"website_link": website_link})
        db.session.commit()
        flash('Venue '+ name + ' was successfully updated!')
    except SQLAlchemyError as e:
        flash('Venue '+ name + ' could not be successfully updated. Please try again.')
    return redirect(url_for('show_venue', venue_id=venue_id))

#  Create Artist
#  ----------------------------------------------------------------


@app.route('/artists/create', methods=['GET'])
def create_artist_form():
    form = ArtistForm()
    return render_template('forms/new_artist.html', form=form)


@app.route('/artists/create', methods=['POST'])
def create_artist_submission():
    # called upon submitting the new artist listing form
    # TODO: insert form data as a new Venue record in the db, instead
    # TODO: modify data to be the data object returned from db insertion
    data = request.form
    try:
        new_artist = Artist(
            genres=data.getlist("genres"),
            name=data.get("name"),
            city=data.get("city"),
            state=data.get("state"),
            facebook_link=data.get("facebook_link"),
            phone=data.get("phone"),
            image_link=data.get("image_link"))
        # print (data.getlist("genres"))
        db.session.add(new_artist)
        db.session.commit()
        flash('Artist ' + request.form['name'] + ' was successfully listed!')
    except SQLAlchemyError as e:
        flash('An error occurred. Artist ' +
              request.form['name'] + ' could not be listed.')
    return render_template('pages/home.html')

    # on successful db insert, flash success
    # flash('Artist ' + request.form['name'] + ' was successfully listed!')
    # TODO: on unsuccessful db insert, flash an error instead.
    # e.g., flash('An error occurred. Artist ' + data.name + ' could not be listed.')
    # return render_template('pages/home.html')


#  Shows
#  ----------------------------------------------------------------

@app.route('/shows')
def shows():
    # displays list of shows at /shows
    # TODO: replace with real venues data.
    #       num_shows should be aggregated based on number of upcoming shows per venue.
    shows_query = Show.query.all()
    shows_mapper = list(map(Show.details, shows_query))
    data = shows_mapper
    return render_template('pages/shows.html', shows=data)


@app.route('/shows/create',  methods=['GET'])
def create_shows_form():
    # renders form. do not touch.
    form = ShowForm()
    return render_template('forms/new_show.html', form=form)


@app.route('/shows/create', methods=['POST'])
def create_show_submission():
    # called to create new shows in the db, upon submitting new show listing form
    # TODO: insert form data as a new Show record in the db, instead
    form = ShowForm()
    data = request.form
    try:
        new_show = Show(
            artist_id=data.get('artist_id'),
            venue_id=data.get("venue_id"),
            start_time=data.get("start_time"))
        db.session.add(new_show)
        db.session.commit()
        flash('Show was successfully listed!')
    except SQLAlchemyError as e:
        flash('Show was not listed. Please try again.')
    return render_template('pages/home.html')

    # on successful db insert, flash success
    # flash('Show was successfully listed!')
    # TODO: on unsuccessful db insert, flash an error instead.
    # e.g., flash('An error occurred. Show could not be listed.')
    # see: http://flask.pocoo.org/docs/1.0/patterns/flashing/


@app.errorhandler(404)
def not_found_error(error):
    return render_template('errors/404.html'), 404


@app.errorhandler(500)
def server_error(error):
    return render_template('errors/500.html'), 500


if not app.debug:
    file_handler = FileHandler('error.log')
    file_handler.setFormatter(
        Formatter(
            '%(asctime)s %(levelname)s: %(message)s [in %(pathname)s:%(lineno)d]')
    )
    app.logger.setLevel(logging.INFO)
    file_handler.setLevel(logging.INFO)
    app.logger.addHandler(file_handler)
    app.logger.info('errors')

#----------------------------------------------------------------------------#
# Launch.
#----------------------------------------------------------------------------#

# Default port:
if __name__ == '__main__':
    app.run()

# Or specify port manually:
'''
if __name__ == '__main__':
    port = int(os.environ.get('PORT', 5000))
    app.run(host='0.0.0.0', port=port)
'''
