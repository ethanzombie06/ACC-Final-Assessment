
from Database import Users, Bookings, Content, db
import forms

import datetime
import sqlalchemy
from flask import Flask, render_template, redirect, flash, url_for, request
from flask_login import LoginManager, login_required, login_user, logout_user, current_user
from werkzeug.security import check_password_hash, generate_password_hash

def are_overlapping(range1_start, range1_end, range2_start, range2_end):
    return range1_start < range2_end and range1_end >= range2_start
# run with : python -m flask --app main run --debug

app = Flask(__name__)
app.config["SECRET_KEY"] = 'aFjoiuhauiofjhnwauiojf12312dasdauoawyh4e978a3ur89y2h9fu732h2h789rrfh9u23ghfyw9837r'
app.config["SQLALCHEMY_DATABASE_URI"] = "sqlite:///project.db"

db.init_app(app)

login_manager = LoginManager()
login_manager.init_app(app)

with app.app_context():
    db.create_all()

@login_manager.user_loader
def load_user(user_id):
    return Users.query.get(user_id)


@app.route("/")
def indexpage():
    return render_template("IndexPage.html")

@app.route("/ParkInfo")
def ParkInfoPage():
    return render_template("ParkInfoPage.html")

@app.route("/Educational")
def EducationalPage():
    data = Content.query.all()
    if data == []:
        Tigers = Content(Content_Id="1",Title= "Tigers",Img="tiger",Body="""Tigers, the largest wild cats in the world, are unique and fascinating creatures.
                                                They are solitary hunters and carnivores, feeding on large mammals. Interestingly, 
                                                they are also good swimmers, a trait not common in the cat family. Each tiger is distinct, 
                                                with no two tigers having the same stripes. There are five subspecies of tigers today, 
                                                including the Bengal and Siberian tigers. However, these magnificent beasts are endangered, 
                                                with their range reduced to around 7% of its former size due to hunting and habitat loss. Their roar, 
                                                which can be heard as far as three kilometers away, serves as a reminder of their power 
                                                and the urgent need for their conservation.""")
        
        Zebras = Content(Content_Id="2",Title="Zebras",Img="zebras",Body="""Zebras, known for their distinctive black and white stripes, are as unique as 
                                                    they are fascinating. There are three species of zebras: the plains zebra, 
                                                    Grevy’s zebra, and mountain zebra. Each zebra has a unique stripe pattern, 
                                                    much like human fingerprints. As herbivores, zebras feed on plants, grasses, 
                                                    and roots. They are social creatures, living in large groups known as herds. 
                                                    Zebras can reach speeds of up to 68.4 km/h and have excellent eyesight, even in 
                                                    color. However, some species of zebras are endangered, highlighting the need 
                                                    for their conservation. Their uniqueness and survival skills serve as a 
                                                    reminder of their importance in our ecosystem. """)
        RedPandas = Content(Content_Id="3",Title="RedPandas",Img="redpanda",Body="""Red pandas, often referred to as the “firefox,” are small mammals 
                                                        native to the eastern Himalayas and southwestern China. 
                                                        Despite their name, they are not closely related to giant 
                                                        pandas. With their reddish-brown fur, bushy tails, and 
                                                        “masked” faces, they are easily one of the most adorable 
                                                        creatures in the zoo. They are arboreal, spending most of 
                                                        their time in trees, and are known for their acrobatic skills. 
                                                        Red pandas primarily eat bamboo, but they also consume eggs, birds, 
                                                        and insects. They are a vulnerable species due to habitat loss 
                                                        and poaching, making their presence in zoos crucial for conservation efforts. 
                                                        Come and marvel at these charming creatures in our zoo! """)
        db.session.add(Tigers)
        db.session.add(Zebras)
        db.session.add(RedPandas)
        db.session.commit()
        data = Content.query.all()
    imgLinks = []
    for i in data:
        imgLinks.append(url_for('static', filename='/photo_assets/{}.jpg'.format(i.Img)))
    return render_template("EducationalPage.html",data = data,imgLinks = imgLinks)

@app.route("/Animals/<Animal>")
def AnimalPage(Animal):
    data = Content.query.filter_by(Title = Animal).one_or_none()
    if data == None:
        return render_template("ErrorPage.html",Error = """
                                Sorry We could not find '{0}' in our databases try 
                                adding a capital letter to the start of each word 
                                and an s to the end of the the animal name. 
                                It is also possible that we dont currently supply 
                                information on this animal.""".format(Animal),)
    imgLink = (url_for('static', filename='photo_assets/{}.jpg'.format(data.Img)))
    mp3Link = (url_for('static', filename='Sound_assets/{}.mp3'.format(data.Img)))
    return render_template("AnimalPage.html",data = data,imgLink = imgLink, videolink = mp3Link)

@app.route("/SignUp", methods=['POST','GET'])
def SignUpPage():
    form = forms.RegistrationForm()
    if form.validate_on_submit():
        try:
            user = Users(id=None,Username = form.Username.data,Email = form.Email.data,Password = generate_password_hash(form.Password.data)) # convert form data to user object
            db.session.add(user)
            db.session.commit()
            flash("Account succsesfully created please sign in")
            return redirect(url_for("SignInPage"))
        except(Exception):
            flash("That email is already in use please try again.")
    elif request.method == 'POST':
        flash("Make sure the confirm password is the same as the main password and that the email is a valid email!")
    return render_template("SignInUpPage.html", form = form, title = "Sign Up")

@app.route("/SignIn", methods=['POST','GET'])
def SignInPage():
    form = forms.LoginForm()
    if form.validate_on_submit():
        User = Users.query.filter_by(Email = form.Email.data).first() # query for user 
        if User != None: # if user exists
            if check_password_hash(User.Password, form.Password.data): # check if password matches
                login_user(User)
                flash("You have been successfully logged in")
                return redirect(url_for("ParkInfoPage"))
            else:
                flash("The details you have input are incorrect please try again")
        else:
            flash("The details you have input are incorrect please try again")
    return render_template("SignInUpPage.html", form = form, title = "Sign In")

@app.route("/SignOut")
@login_required
def SignOut():
    logout_user()
    return redirect(url_for("ParkInfoPage"))

@app.route("/ZooBooking", methods=['POST','GET'])
@login_required
def ZooBookingPage():
    form = forms.ZooBooking()
    if form.validate_on_submit():
            date = form.TimeSlot.data.strftime('%d/%m/%Y')# converting the inputed date to a usable format
            booking = Bookings(id = None, Booking_type = "Zoo",Email = current_user.Email, Attendees = form.Attendees.data,Start = date, End = date)
            #https://stackoverflow.com/questions/10624937/convert-datetime-object-to-a-string-of-date-only-in-python
            #reffered to this link to find out how to convert date to string
            db.session.add(booking)
            db.session.commit()
            flash("Booking succsesfully created!")
            return redirect(url_for("ParkInfoPage"))
    return render_template("SignInUpPage.html", form = form, title = "Book a ticket for the zoo!")

@app.route("/HotelBooking", methods=['POST','GET'])
@login_required
def HotelBookingPage():
    form = forms.HotelBooking()
    if form.validate_on_submit():
            if form.StartTime.data >= form.EndTime.data:
                flash("Error: The end date must be after the start date")
            else:
                # converting the inputed dates to a usable format
                start = form.StartTime.data.strftime('%d/%m/%Y')
                end = form.EndTime.data.strftime('%d/%m/%Y')
                data = Bookings.query.filter_by(Booking_type = "Hotel").all()
                count = 0
                OverLappingEnds = [] 
                for i in data:
                    if are_overlapping(start,end,i.Start,i.End): # look for overlapping bookings if the ammount is more than the ammount of rooms
                        #flash("{0}-{1} is overlapping {2}-{3} ".format(start,end,i.Start,i.End))# Used for seeing overlapping time not in final product.
                        OverLappingEnds.append(i.End)
                        count+= 1
                if count >=5: # replace five with ammount of rooms availble
                    flash("Error: Sorry we are fully booked during this time. try booking after: {0}".format(min(OverLappingEnds)))
                else:
                    booking = Bookings(id = None, Booking_type = "Hotel",Email = current_user.Email, Attendees = form.Attendees.data,Start = start, End = end)
                    #https://stackoverflow.com/questions/10624937/convert-datetime-object-to-a-string-of-date-only-in-python
                    #reffered to this link to find out how to convert date to string
                    db.session.add(booking)
                    db.session.commit()
                    flash("Booking succsesfully created!")
                    return redirect(url_for("ParkInfoPage"))
    return render_template("SignInUpPage.html", form = form, title = "Book a ticket for the Hotel!") # passing form and title to front end

@app.route("/Profile", methods=['POST','GET'])
@login_required
def ProfilePage():
    data = Bookings.query.filter_by(Email = current_user.Email).all()
    return render_template("ProfilePage.html",data = data)

if __name__ == '__main__':
    app.run()