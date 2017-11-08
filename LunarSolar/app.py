from flask import Flask, render_template, request, json, redirect
from LunarSolar import solar_to_lunar_string, lunar_to_solar_string, day_in_week, \
                       lunar_leap, zodiac_day, zodiac_month, zodiac_year
from flask_sqlalchemy import SQLAlchemy

app = Flask(__name__)
# app.config['SQLALCHEMY_DATABASE_URI'] = 'postgresql+psycopg2://postgres:12345678@localhost:5432/SolarLunar'
# app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///Save.db'
app.config.from_pyfile('app.cfg')
db = SQLAlchemy(app)


class SolarLunar(db.Model):
    __tablename__ = "SolarLunar"
    SLID = db.Column(db.Integer, nullable=False, primary_key=True)
    SolarDay = db.Column(db.String(1000), nullable=False)
    LunarDay = db.Column(db.String(1000), nullable=False)
    LeapMonth = db.Column(db.Integer, nullable=True)

    def __init__(self, SolarDay, LunarDay, LeapMonth, SLID):
        self.SolarDay = SolarDay
        self.LunarDay = LunarDay
        self.LeapMonth = LeapMonth
        self.SLID = SLID

    def __str__(self):
        return "{} - {}-{}".format(self.SolarDay, self.LunarDay, self.LeapMonth)


@app.route('/')
def hello_world():
    return render_template('index.html')


@app.route('/Solar2Lunar', methods=['GET', 'POST'])
def solar_to_lunar():
    try:
        if request.method == 'POST':
            # read the posted values from the UI
            _day = int(request.form['inputSolarDay'])
            _month = int(request.form['inputSolarMonth'])
            _year = int(request.form['inputSolarYear'])
            result = solar_to_lunar_string(_day, _month, _year)
            return json.dumps({'message': result}, ensure_ascii=False)
        else:
            return redirect("/")
    except Exception as ex:
        return json.dumps({'message': 'Lỗi không convert được {}'.format(ex)}, ensure_ascii=False)

@app.route("/DayWeek", methods=['GET', 'POST'])
def day_in_week_convert():
    try:
        if request.method == 'POST':
            _day = int(request.form['inputDay'])
            _month = int(request.form['inputMonth'])
            _year = int(request.form['inputYear'])
            result = day_in_week(_day, _month, _year)
            return json.dumps({'message': result}, ensure_ascii=False)
        else:
            return render_template('DayWeek.html')
    except Exception as ex:
        return json.dumps({'message': 'Lỗi không convert được {}'.format(ex)}, ensure_ascii=False)

@app.route("/LeapYear", methods=['GET', 'POST'])
def leap_year_convert():
    try:
        if request.method == 'POST':
            _year = int(request.form['inputYear'])
            if lunar_leap(_year):
                result = "Năm {} là năm nhuận".format(_year)
            else:
                result = "Năm {} không là năm nhuận".format(_year)
            return json.dumps({'message': result}, ensure_ascii=False)
        else:
            return render_template('LeapYear.html')
    except Exception as ex:
        return json.dumps({'message': 'Lỗi không convert được {}'.format(ex)}, ensure_ascii=False)

@app.route("/DayCanChi", methods=['GET', 'POST'])
def day_zodiac_convert():
    try:
        if request.method == 'POST':
            _day = int(request.form['inputDay'])
            _month = int(request.form['inputMonth'])
            _year = int(request.form['inputYear'])
            result = zodiac_day(_day, _month, _year)
            return json.dumps({'message': result}, ensure_ascii=False)
        else:
            return render_template('DayZodiac.html')
    except Exception as ex:
        return json.dumps({'message': 'Lỗi không convert được {}'.format(ex)}, ensure_ascii=False)


@app.route("/MonthCanChi", methods=['GET', 'POST'])
def month_zodiac_convert():
    try:
        if request.method == 'POST':
            _month = int(request.form['inputMonth'])
            _year = int(request.form['inputYear'])
            result = zodiac_month(_month, _year)
            return json.dumps({'message': result}, ensure_ascii=False)
        else:
            return render_template('MonthZodiac.html')
    except Exception as ex:
        return json.dumps({'message': 'Lỗi không convert được {}'.format(ex)}, ensure_ascii=False)

@app.route("/YearCanChi", methods=['GET', 'POST'])
def year_zodiac_convert():
    try:
        if request.method == 'POST':
            _year = int(request.form['inputYear'])
            result = zodiac_year(_year)
            return json.dumps({'message': result}, ensure_ascii=False)
        else:
            return render_template('YearZodiac.html')
    except Exception as ex:
        return json.dumps({'message': 'Lỗi không convert được {}'.format(ex)}, ensure_ascii=False)

# Convert by get from Database
@app.route('/Lunar2Solar', methods=['GET', 'POST'])
def lunar_to_solar():
    try:
        if request.method == 'POST':
            # read the posted values from the UI
            _day = int(request.form['inputLunarDay'])
            _month = int(request.form['inputLunarMonth'])
            _year = int(request.form['inputLunarYear'])
            try:
                _is_leap_month = request.form['cbMonthLeap']
                _is_leap_month = 1
            except Exception:
                _is_leap_month = 0

            _date = "{}/{}/{}".format(_day, _month, _year)
            s2l = SolarLunar.query.filter(SolarLunar.LunarDay.like('%{}%' \
                                          .format(_date))) \
                                          .filter(SolarLunar.LeapMonth
                                                  == _is_leap_month)\
                                           .first()
            # solar_date = s2l.SolarDay.split("/")
            # solar_day = solar_date[0]
            # solar_month = solar_date[1]
            # solar_year = solar_date[2]
            # day_week = day_in_week(solar_day, solar_month, solar_year)
            return json.dumps({'message': "{} ".format(s2l.SolarDay)
                              }, ensure_ascii=False)
        else:
            return render_template('lunar2solar.html')
    except Exception as ex:
        return json.dumps({'message': 'Lỗi không convert được {}'.format(ex)}, ensure_ascii=False)


if __name__ == '__main__':
    app.run(debug=True)
