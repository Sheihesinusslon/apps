from flask import Flask, render_template, request, redirect, url_for, flash
import requests
import sys
from config import API_KEY
import time
from flask_sqlalchemy import SQLAlchemy

app = Flask(__name__)
app.secret_key = b'_5#y2L"F4Q8z\n\xec]/'
db = SQLAlchemy(app)
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///weather.db'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = 0


class City(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(40), unique=True, nullable=False)

    def __repr__(self):
        return f'{self.name}'


db.create_all()


class CityNotExist(Exception):
    pass


class CityInDb(Exception):
    pass


def is_valid(city_name):
    r = requests.get(f'http://api.openweathermap.org/data/2.5/weather?q={city_name}&units=metric&appid={API_KEY}')
    if r.status_code == 404:
        raise CityNotExist
    in_db = City.query.filter_by(name=city_name).first()
    if in_db:
        raise CityInDb
    return True


def determine_time(utc_time):
    local_time = time.gmtime().tm_hour + utc_time // 3600
    if 9 < local_time < 17:
        image = 'day'
    elif 20 > local_time <= 23 or 0 < local_time < 6:
        image = 'night'
    else:
        image = 'evening-morning'
    return image


def get_weather_info(city: City):
    r = requests.get(f'http://api.openweathermap.org/data/2.5/weather?q={city.name}&units=metric&appid={API_KEY}')
    data = r.json()
    weather_info = {
        'city_id': city.id,
        'city': city.name,
        'weather': data['weather'][0]['description'],
        'temp': int(data['main']['temp']),
        'time': determine_time(int(data['timezone']))
    }
    return weather_info


@app.route('/', methods=['GET', 'POST'])
def index():
    if request.method == 'POST':
        city_name = request.form['city_name']
        try:
            if is_valid(city_name):
                city = City(name=city_name)
                db.session.add(city)
                db.session.commit()
        except CityNotExist:
            flash("The city doesn't exist!")
        except CityInDb:
            flash('The city has already been added to the list!')
        return redirect(url_for('index'))
    else:
        cities = City.query.all()
        cards = tuple(get_weather_info(city) for city in cities)
        return render_template('index.html', cards=cards)


@app.route('/delete/<int:city_id>', methods=['GET', 'POST'])
def delete(city_id):
    city = City.query.filter_by(id=city_id).first()
    if city:
        db.session.delete(city)
        db.session.commit()
    return redirect(url_for('index'))


# don't change the following way to run flask:
if __name__ == '__main__':
    if len(sys.argv) > 1:
        arg_host, arg_port = sys.argv[1].split(':')
        app.run(host=arg_host, port=arg_port)
    else:
        app.run()
