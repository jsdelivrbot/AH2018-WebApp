from flask import Flask, request, session, render_template, url_for, redirect
from flask_googlemaps import GoogleMaps, Map, icons
from email.utils import parseaddr # used for checking email formet
from sqlalchemy.orm import sessionmaker
import os, math
from datetime import datetime # datetime is used for saving animal register date
from database import *

app = Flask(__name__)
GoogleMaps(app, key='AIzaSyDunBer2z_LST4C2FNDv6DZZ39jlE82vU8')
# google map key
engine = create_engine('sqlite:///HOTSIX.db', echo=True)

# def PointsInCircum(r,n=5):
#     pi = 3
#     return [(round(math.cos(2*pi/n*x)*r, 4), round(math.sin(2*pi/n*x)*r, 4)) for x in range(0,n+1)]

@app.route('/') # 시작 화면
def home():
    # 로그인 되어 있지 않으면 로그인 페이지로 이동
    if not session.get('logged_in'):
        # flash로 메세지 받은 건 템플릿에서 처리
        return render_template('login.html')
    # 로그인 되었으면 바로 인덱스 페이지로 이동
    else:
        return render_template('index.html', username = session.get('username'))

@app.route('/login', methods=['POST']) # 로그인
def login(): # login.html에서 받은 데이터 사용
    username = str(request.form['username']) # username
    password = str(request.form['password']) # password
    Session = sessionmaker(bind=engine)
    s = Session() # session 생성
    query = s.query(User).filter(User.username.in_([username]), User.password.in_([password]))
    result = query.first()
    if result: # result = True
        session['logged_in'] = True # 로그인 성공
        session['username'] = username
    # else:
    #     flash('wrongData') # 잘못된 데이터
    return home() # 시작 화면으로 가서 처리

@app.route('/registerAnimal', methods=['GET', 'POST'])
def register_animal():
    if request.method == 'POST':
        animal_owner = session.get('user_id')
        # animal owner
        animal_name = request.form('animalname')
        # animal name 
        animal_age = request.form('animalage')
        # animal age
        animal_register_date = datetime.datetime.today().year 
        # register year (for keep track of animal age)
        animal_weight = request.form('animalweight')
        # animal weight
        animal_kind = request.form('animalkind')
        # animal kind
        animal_sex = request.form('animalsex')
        # animal sex
        Session = sessionmaker(bind=engine)
        session = Session()
        session.add(Animal(
            animal_owner, animal_name, animal_age, 
            animal_register_date, animal_weight, 
            animal_kind, animal_sex
        ))
        session.commit()
        return home()
    else:
        return render_template('register.html')

@app.route('/map')
def map():
    base = [37.5061058, 127.0616346]
    circle = {
        'stroke_color': '#0000FF',
        'stroke_opacity': .5,
        'stroke_weight': 5,
        'fill_color': '#FFFFFF',
        'fill_opacity': .2,
        'center': {
                  'lat': base[0],
                  'lng': base[1]
        },
        'radius': 17,
    }
    circlemap = Map(
        identifier="map", varname="map",
        lat=base[0], lng=base[1], zoom = 20,
        markers=[(base[0], base[1])],
        circles=[circle]
    )
    return render_template('map.html', map=circlemap)

@app.errorhandler(404)
def page_not_found(e):
    return render_template('404.html'), 404

if __name__ == '__main__':
    app.secret_key = os.urandom(12)
    app.run(debug = True)
    