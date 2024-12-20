import json
from flask import Flask, render_template, request, redirect, flash, url_for, session
from datetime import datetime


def load_clubs():
    with open('clubs.json') as c:
        clubs_list = json.load(c)['clubs']
        return clubs_list


def load_competitions():
    with open('competitions.json') as comps:
        competitions_list = json.load(comps)['competitions']

        for comp in competitions_list:
            if datetime.strptime(comp["date"], "%Y-%m-%d %H:%M:%S") < datetime.now():
                comp["past"] = True
            else:
                comp["past"] = False

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
    try:
        club = [club for club in clubs if club['email'] == request.form['email']][0]
        session["name"] = club["name"]
    except IndexError:
        flash("No account found")
        return render_template("index.html")
    return render_template('welcome.html', club=club, competitions=competitions)


def find_club(club):
    found_club = [c for c in clubs if c["name"] == club][0]
    return found_club


def find_competition(competition):
    found_competition = [c for c in competitions if c["name"] == competition][0]
    return found_competition


@app.route('/book/<competition>/<club>')
def book(competition, club):
    found_club = find_club(club)
    found_competition = find_competition(competition)
    if found_club and found_competition:
        max_places = min(12, int(found_club["points"]), int(found_competition["numberOfPlaces"]))
        return render_template('booking.html', club=found_club, competition=found_competition,
                               max_places=max_places)
    else:
        flash("Something went wrong-please try again")
        return render_template('welcome.html', club=club, competitions=competitions)


def validate_booking_conditions(club, competition, places):
    date = datetime.strptime(competition["date"], "%Y-%m-%d %H:%M:%S")

    if (places > 12 or places > int(club["points"])
            or places > int(competition["numberOfPlaces"]) or date < datetime.now()):
        return False
    return True


def reduce_places_in_competition(competition, places):
    competition["numberOfPlaces"] = int(competition["numberOfPlaces"]) - places


def reduce_club_points(club, places):
    club["points"] = int(club["points"]) - places


@app.route('/purchasePlaces', methods=['POST'])
def purchase_places():
    form_data = request.form

    competition = find_competition(form_data["competition"])
    club = find_club(form_data["club"])
    places_required = int(form_data["places"])

    if validate_booking_conditions(club, competition, places_required):
        reduce_places_in_competition(competition, places_required)
        reduce_club_points(club, places_required)
        flash('Great-booking complete!')

    else:
        flash("Something went wrong-please try again")
    return render_template('welcome.html', club=club, competitions=competitions)


@app.route('/clubs')
def clubs_points_board():
    return render_template('clubs_board.html', clubs=clubs)


@app.route('/backHome')
def back_home():
    if session.get("name"):
        club = find_club(session.get("name"))
        return render_template('welcome.html', club=club, competitions=competitions)


@app.route('/logout')
def logout():
    session.pop('name', None)
    return redirect(url_for('index'))
