from re import A
import gmap
import os 
import re
import pymongo

from flask import Flask, jsonify
from flask import render_template 
from flask import request 
from flask import redirect 
from flask import url_for
from flask_wtf.csrf import CSRFError
from flask_pymongo import PyMongo
#from flask_sqlalchemy import SQLAlchemy
from Models import db
from Models import User
from flask import session 
from flask_wtf.csrf import CSRFProtect 
from Forms import RegisterForm, LoginForm, Postform
import datetime
import math
import sqlite3

app = Flask(__name__)
conn = sqlite3.connect('logintable.db')
basedir = os.path.abspath(os.path.dirname(__file__)) 
dbfile = os.path.join(basedir, 'logintable.db') 
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///' + dbfile
app.config['SQLALCHEMY_COMMIT_ON_TEARDOWN'] = True 
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False 
app.config['SECRET_KEY']='asdfasdfasdfqwerty' 
app.config["MONGO_URI"] = "mongodb://localhost:27017/review"
myclient = pymongo.MongoClient('localhost', 27017)
Gyeonggi = myclient['Gyeonggi']
review = Gyeonggi['review']
csrf = CSRFProtect()
csrf.init_app(app)
db.init_app(app) 
db.app = app 
db.create_all() 
#mongo = PyMongo(app)
#review = mongo.db.review

@app.errorhandler(CSRFError)
def csrf_error(reason):
    print(reason)

@app.route('/')
def mainpage():
    userid = session.get('userid',None)
    return render_template('index.html', userid=userid)
    
@app.route('/register/', methods=['GET', 'POST'])
def register():
    form = RegisterForm()
    if form.validate_on_submit():
        usertable = User(form.data.get('userid'),form.data.get('email'),form.data.get('password')) 
        db.session.add(usertable) 
        db.session.commit() 
        return redirect('/') 
    return render_template('register.html', form=form)

@app.route('/idcheck', methods=['GET', 'POST'])
def idcheck():
    params = request.get_json()
    if(type(params) == dict):
        userid = params['id']
        if(params['id'] == ""):
            return jsonify(result = "success", result2= "아이디를 입력해주세요")
        usertableid = User.query.filter_by(userid=userid).first()
        if(usertableid):
            return jsonify(result = "success", result2= "중복된 아이디입니다")
        else:
            return jsonify(result = "success", result2= "사용가능한 아이디입니다")
    
@app.route('/addresscheck', methods=['GET', 'POST'])
def addresscheck():
    params = request.get_json()
    if(type(params) == dict):
        useraddress = params['address']
        if(params['address'] == ""):
            return jsonify(result = "success", result2= "이메일을 입력해주세요")
        usertableaddress = User.query.filter_by(email=useraddress).first()
        if(usertableaddress):
            return jsonify(result = "success", result2= "중복된 이메일입니다")
        else:
            return jsonify(result = "success", result2= "사용가능한 이메일입니다")

@app.route('/login/', methods=['GET','POST'])  
def login():
    form = LoginForm()
    if form.validate_on_submit():
        session['userid']=form.data.get('userid') 
        return redirect('/') 
    return render_template('login.html', form=form)   

@app.route('/reviewpage/login/', methods=['GET','POST'])  
def reviewpagelogin():
    form = LoginForm()
    if form.validate_on_submit():
        session['userid']=form.data.get('userid') 
        return redirect('/writepage') 
    return render_template('login.html', form=form) 

@app.route('/logout', methods=['GET'])
def logout():
    session.pop('userid', None)
    return redirect('/')

@app.route('/review_page', methods=['GET','POST'])
def review_page():
    current_time = datetime.datetime.now()
    print(current_time)
    form = RegisterForm()

    #for restaurant in review.find():
        #print(restaurant)

    params = request.get_json()
    if(type(params) == dict):
      print(params['title'])
      print(params['content'])
      title = params['title']
      content = params['content']
      writter = params['writter']
      point = params['point']
      post = {
        "title": title,
        "content": content,
        "writter": writter,
        "point" : point,
        "Date": current_time
      }
  
      review.insert_one(post)
      return jsonify(result = "success")

    return render_template('review_page.html')   

@app.route('/ajax', methods=['POST'])
def ajax():
    global datas
    global index
    index = 0
    data = request.get_json()
    a = data['parm1'].split(',')[0].lstrip("(")
    b = data['parm1'].split(',')[1].lstrip(" ").rstrip(")")
    loc_data = gmap.ret_location(float(a), float(b), data['parm2'])

    for i in loc_data:
        title = i['상호명']
        datas = review.aggregate([
            { "$match": { "market": title}},
            { '$group': { '_id': '$market', 'point': { '$avg': '$point'} }}
        ]) 

        data1 = list(datas)
        data1.insert(1, {'point': '0'})
        i['point'] = round(float(data1[0]['point']), 1)

    return jsonify(result = "success", mydata= loc_data)

@app.route('/writepage', methods=['GET', 'POST'])
def writepage():
    form = Postform()
    entertype = session.get('entertype',None)
    userid = session.get('userid',None)
    if(entertype == 'indexbutton'):
        address = session.get('address',None)
        market = session.get('market',None)
        searchtype = session.get('searchtype',None)
        searchcontents = session.get('searchcontents',None)
        current_time = datetime.datetime.now()
        date = str(current_time)[0:10]
    else:
        address = ""
        market = ""
        searchtype = session.get('searchtype',None)
        searchcontents = session.get('searchcontents',None)
        current_time = datetime.datetime.now()
        date = str(current_time)[0:10]


    params = request.get_json()
    if(type(params) == dict):
      market = params['market']
      address = params['address']
      content = params['content']
      writer = params['writer']
      point = params['point']
      post = {
        "content": content,
        "writer": writer,
        "point" : int(point),
        "Date": date,
        "market": market,
        "address": address
      }
  
      review.insert_one(post)
      return jsonify({'redirect': url_for("indexbutton", market=market, address=address)})

    return render_template(
        'writepage.html', 
        entertype=entertype,
        searchtype=searchtype,
        searchcontents=searchcontents,
        form=form, 
        userid=userid, 
        market=market,
        address=address) 

@app.route('/reviewinformation', methods=["POST", "GET"])
def reviewinformation():
    params = request.get_json()
    if(type(params) == dict):
        session['contents'] = params['contents']
        session['point'] = params['point']
        session['writer'] = params['writer']
        session['selectmarket'] = params['market']
        session['selectaddress'] = params['address']
        return jsonify({'redirect': url_for("reviewcontents")})

#타입별 검색
@app.route('/searchtype', methods=["POST", "GET"])
def filledsearch():
    params = request.get_json()
    if(type(params) == dict):
        searchtype = params['searchtype']
        searchcontents = params['searchcontents']
        session['searchtype'] = searchtype
        session['searchcontents'] = searchcontents
        return jsonify({'redirect': url_for("searchcontents", searchtype=searchtype, searchcontents=searchcontents)})        

@app.route('/reviewpage/<searchtype>/<searchcontents>', methods=["POST", "GET"])
def searchcontents(searchtype,searchcontents):
    session['entertype'] = 'searchcontents'
    form = Postform()
    userid = session.get('userid',None)

    page = request.args.get("page", 1, type=int)
    limit = 10

    datas = review.find({searchtype: {'$regex' : searchcontents}}).sort("_id", -1).skip((page - 1) * limit).limit(limit)
    tot_count = review.count_documents({searchtype: {'$regex' : searchcontents}})
    last_page_num = math.ceil(tot_count / limit)
    block_size = 5
    block_num = int((page - 1) / block_size)
    block_start = (block_size * block_num) + 1
    block_end = block_start + (block_size - 1)

    return render_template(
        'reviewpage.html',
        type=session['entertype'],
        searchtype=searchtype,
        searchcontents=searchcontents,
        datas=datas,
        limit=limit,
        page=page,
        block_start=block_start,
        block_end=block_end,
        last_page_num=last_page_num,
        tot_count=tot_count,
        form=form,
        userid=userid)         

#전체 검색
@app.route('/reviewpage', methods=["POST", "GET"])
def allsearch():
    session['entertype'] = 'allsearch'
    form = Postform()
    userid = session.get('userid',None)

    page = request.args.get("page", 1, type=int)
    limit = 10
    datas = review.find({}).sort("_id", -1).skip((page - 1) * limit).limit(limit)
    tot_count = review.count_documents({})
    last_page_num = math.ceil(tot_count / limit)
    block_size = 5
    block_num = int((page - 1) / block_size)
    block_start = (block_size * block_num) + 1
    block_end = block_start + (block_size - 1)

    return render_template(
        'reviewpage.html',
        type=session['entertype'],
        datas=datas,
        limit=limit,
        page=page,
        block_start=block_start,
        block_end=block_end,
        last_page_num=last_page_num,
        tot_count=tot_count,
        form=form,
        userid=userid) 

@app.route('/genre_picks', methods=["POST", "GET"])
def genre_picks():
    params = request.get_json()
    if(type(params) == dict):
        market = params['market']
        address = params['address']
        return jsonify({'redirect': url_for("indexbutton", market=market, address=address)})         

@app.route('/reviewpage1/<market>/<address>', methods=['GET', 'POST'])
def indexbutton(market, address):
    session['entertype'] = 'indexbutton'
    form = Postform()
    session['market'] = market
    session['address'] = address
    userid = session.get('userid',None)

    page = request.args.get("page", 1, type=int)
    limit = 10
    datas = review.find({'market': market}).sort("_id", -1).skip((page - 1) * limit).limit(limit)
    tot_count = review.count_documents({'market': market})
    last_page_num = math.ceil(tot_count / limit)
    block_size = 5
    block_num = int((page - 1) / block_size)
    block_start = (block_size * block_num) + 1
    block_end = block_start + (block_size - 1)

    return render_template(
        'reviewpage.html',
        type=session['entertype'],
        datas=datas,
        limit=limit,
        page=page,
        block_start=block_start,
        block_end=block_end,
        last_page_num=last_page_num,
        tot_count=tot_count,
        market=market,
        address=address,
        form=form,
        userid=userid)

@app.route('/reviewcontents', methods=["POST", "GET"])
def reviewcontents():
    form = Postform()
    userid = session.get('userid',None)
    writer = session.get('writer',None)
    market = session.get('selectmarket',None)
    address = session.get('selectaddress',None)
    contents = session.get('contents',None)
    point = session.get('point',None)
    type = session.get('entertype',None)
    searchtype = session.get('searchtype',None)
    searchcontents = session.get('searchcontents',None)

    return render_template(
        'reviewcontents.html',
        searchtype=searchtype,
        searchcontents=searchcontents,
        type=type,
        writer=writer,
        userid=userid,
        market=market,
        address=address,
        contents=contents,
        point=point,
        form=form)

@app.route('/modify', methods=['POST'])
def modify():
    params = request.get_json()
    if(type(params) == dict):
        modifymarket = params['market']
        modifyaddress = params['address']
        #modifywriter = params['writer']
        modifycontents = params['contents']
        modifypoint = params['point']
    
    current_time = datetime.datetime.now()
    date = str(current_time)[0:10]
    writer = session.get('writer',None)
    market = session.get('selectmarket',None)
    address = session.get('selectaddress',None)
    contents = session.get('contents',None)
    searchtype = session.get('searchtype',None)
    searchcontents = session.get('searchcontents',None)

    review.update_one(
        { 'writer':writer, 'address':address, 'market':market, 'content':contents }, 
        { "$set": { 'market': modifymarket, 'address': modifyaddress, 'content':modifycontents, 'point':modifypoint, 'Date':date } } 
    )
    if(session.get('entertype',None) == "indexbutton"):
        return jsonify({'redirect': url_for("indexbutton", market=market, address=address)})
    elif(session.get('entertype',None) == "searchcontents"):
        return jsonify({'redirect': url_for("searchcontents", searchtype=searchtype, searchcontents=searchcontents)})
    else:
        return jsonify({'redirect': url_for("allsearch")})

@app.route('/delete', methods=['POST'])
def delete():
    writer = session.get('writer',None)
    market = session.get('selectmarket',None)
    address = session.get('selectaddress',None)
    contents = session.get('contents',None)
    searchtype = session.get('searchtype',None)
    searchcontents = session.get('searchcontents',None)

    review.delete_one({'writer':writer, 'address':address, 'market':market, 'content':contents})
    if(session.get('entertype',None) == "indexbutton"):
        return jsonify({'redirect': url_for("indexbutton", market=market, address=address)})
    elif(session.get('entertype',None) == "searchcontents"):
        return jsonify({'redirect': url_for("searchcontents", searchtype=searchtype, searchcontents=searchcontents)})
    else:
        return jsonify({'redirect': url_for("allsearch")})

@app.route('/list1', methods=['GET','POST'])
def list1():
    params = request.get_json()
    if(type(params) == dict):
        list1 = params['list1']
        session['list1'] = list1
        return jsonify({'redirect': url_for("infolist")})  

@app.route('/infolist', methods=['GET','POST'])
def infolist():
    form = Postform()
    list1 = session.get('list1',None)
    return render_template('list.html', list1=list1, form=form)

if __name__ == '__main__':
    app.run('localhost', port=5001, debug=True)