from flask import Flask, render_template, request
from weather_util import get_weather, get_weather_by_coord
import crawl_util as cu
import map_util as mu
import image_util as iu
import os, random

app = Flask(__name__)

# flask 2.3 에서는 이 코드만 사용 가능
with app.app_context():
    global quote, quotes   # quote, quotes를 전역변수로 만듦-> 함수 밖에서도 사용 가능
    global addr     # session이 없는 상태라 global계속 지정해줌
    filename = os.path.join(app.static_folder, 'data/todayQuote.txt')
    with open(filename, encoding='utf-8') as f:
        quotes = f.readlines()
    quote = random.sample(quotes, 1)[0]
    addr = '수원시 장안구'

""" @app.before_first_request
 def before_first_request():    # 단 한번만 보여주는 함수
     global quote, quotes
     global addr
     filename = os.path.join(app.static_folder, 'data/todayQuote.txt')
     with open(filename, encoding='utf-8') as f:
         quotes = f.readlines()
     quote = random.sample(quotes, 1)[0]
     addr = '수원시 장안구'"""

################ for AJAX ##################
@app.route('/change_quote')
def change_quote():
    global quote
    quote = random.sample(quotes, 1)[0]
    return quote

@app.route('/change_addr')
def change_addr():
    global addr
    addr = request.args.get('addr')
    return addr

@app.route('/weather')
def weather():
    addr = request.values['addr']       # args.get('addr')+ 
    lat, lng = mu.get_coord(addr + '청')
    html = get_weather_by_coord(app, lat, lng)
    return html

@app.route('/change_profile', methods=['POST']) # post 안하면 안받아짐-오류
def change_profile():
    file_image = request.files['image']
    filename = os.path.join(app.static_folder, f'upload/{file_image.filename}')
    file_image.save(filename) # 저장
    mtime = iu.change_profile(app, filename)
    return str(mtime)
##########################################

@app.route("/")
def home():
    menu = {"ho": 1, "us": 0, "cr": 0, "sc": 0}
    return render_template("prototype/home.html", menu=menu, weather=get_weather(app), 
                           quote=quote, addr=addr)


@app.route("/interpark")
def interpark():
    menu = {"ho": 0, "us": 0, "cr": 1, "sc": 0}
    book_list = cu.interpark()
    return render_template(
        "prototype/interpark.html",
        book_list=book_list,
        menu=menu,
        weather=get_weather(app), quote=quote, addr=addr
    )


@app.route("/genie")
def genie():
    menu = {"ho": 0, "us": 0, "cr": 1, "sc": 0}
    song_list = cu.genie()
    return render_template(
        "prototype/genie.html", song_list=song_list, menu=menu, weather=get_weather(app), 
        quote=quote, addr=addr
    )


@app.route("/siksin", methods=["GET", "POST"])
def siksin():
    menu = {"ho": 0, "us": 0, "cr": 1, "sc": 0}
    if request.method == "GET":
        return render_template(
            "prototype/siksin.html", menu=menu, weather=get_weather(app), 
            quote=quote, addr=addr
        )
    else:
        place = request.form["place"]
        food_list = cu.siksin(place)
        return render_template(
            "prototype/siksin_res.html",
            food_list=food_list,
            menu=menu,
            weather=get_weather(app),
            place=place, quote=quote, addr=addr
        )


@app.route("/schedule")
def schedule():
    menu = {"ho": 0, "us": 0, "cr": 0, "sc": 1}
    return render_template(
        "prototype/schedule.html", menu=menu, weather=get_weather(app), quote=quote
    )


@app.route("/youtube")
def youtube():
    return "준비중 입니다!"


if __name__ == "__main__":
    app.run(debug=True)
