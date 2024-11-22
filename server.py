import json
from flask import Flask, render_template, request, redirect, flash, url_for


def load_clubs():
    with open('clubs.json') as c:
        clubs_list = json.load(c)['clubs']
        return clubs_list


def load_competitions():
    with open('competitions.json') as comps:
        competitions_list = json.load(comps)['competitions']
        return competitions_list


app = Flask(__name__)
app.secret_key = 'something_special'

competitions = load_competitions()
clubs = load_clubs()


@app.route('/')
def index():
    return render_template('index.html')


@app.route('/showSummary', methods=['POST'])
def show_summary():
    club = [club for club in clubs if club['email'] == request.form['email']][0]
    return render_template('welcome.html', club=club, competitions=competitions)


@app.route('/book/<competition>/<club>')
def book(competition, club):
    found_club = [c for c in clubs if c['name'] == club][0]
    found_competition = [c for c in competitions if c['name'] == competition][0]
    if found_club and found_competition:
        return render_template('booking.html', club=found_club, competition=found_competition)
    else:
        flash("Something went wrong-please try again")
        return render_template('welcome.html', club=club, competitions=competitions)


def find_competition(form_data):
    competition = [c for c in competitions if c["name"] == form_data["competition"]][0]
    return competition


def find_club(form_data):
    club = [c for c in clubs if c["name"] == form_data["club"]][0]
    return club


def validate_booking_conditions(places):
    if places > 12:
        return False
    return True


def reduce_places_in_competition(competition, places):
    competition["numberOfPlaces"] = int(competition["numberOfPlaces"]) - places


def reduce_club_points(club, places):
    club["points"] = int(club["points"]) - places


@app.route('/purchasePlaces', methods=['POST'])
def purchase_places():
    form_data = request.form

    competition = find_competition(form_data)
    club = find_club(form_data)
    places_required = int(form_data["places"])
    print(places_required)

    if validate_booking_conditions(places_required):
        reduce_places_in_competition(competition, places_required)
        reduce_club_points(club, places_required)
        flash('Great-booking complete!')

    else:
        flash('You are not allowed to book more than 12 places.')
    return render_template('welcome.html', club=club, competitions=competitions)


# TODO: Add route for points display

@app.route('/logout')
def logout():
    return redirect(url_for('index'))
