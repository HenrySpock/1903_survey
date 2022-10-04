from flask import Flask, render_template, request, redirect, flash, jsonify, make_response, session
from flask_debugtoolbar import DebugToolbarExtension 
from surveys import satisfaction_survey as satsurv

app = Flask(__name__)
app.config['SECRET_KEY'] = "surv_sess"

debug = DebugToolbarExtension(app)

app.config['TEMPLATES_AUTO_RELOAD'] = True
app.config['DEBUG_TB_INTERCEPT_REDIRECTS'] = False

responses = []

print(responses)
print("HelLO there.")

@app.route("/")
def root():
    """Take user to homepage of survey."""
    print(responses)
    responses.clear()
    print(responses)
    title = satsurv.title
    instr = satsurv.instructions
    resp = len(responses)
    # session['username'] = 'Hot Rod'
    # session['seekers'] = ['Starscream', 'Thundercracker', 'Skywarp']
    print('***')
    print(session["username"])
    print(session["seekers"])
    print('***')
    return render_template('home.html', title = title, instr = instr, id = resp)

#Below is the working before checking for index out of bounds
# @app.route("/questions/<int:respid>")
# def question01(respid):
#     respid = len(responses) 
#     print(respid)
#     question = satsurv.questions[respid].question
#     """Take user to homepage of survey."""
#     return render_template('questions.html', qnum=respid + 1, question = question)

#Below handles out of bounds test
@app.route("/questions/<int:respid>")
def question01(respid):
    #The following line prevents a user from skipping a question by insuring the questin id is 
    #based on the responses list rather than the url increment - if you try to visit a question
    #out of order, notice the value of respid before and after the =len(responses)
    print(respid)
    #Notice below that if you try to visit a qeustion out of order, Whoa Nelly! prints to the
    #server but we are still on the correct question. 
    if respid != len(responses):
        print("Whoa nelly!")
        flash("Whoa Nelly!")
    respid = len(responses)
    question = satsurv.questions[respid].question
    print(respid)
    #The following line checks if the respid (which is based on the responses list) to the length of the 
    #list of questions defined in the class satisfaction_survey, which, if true, will always render
    #the thanks.html page without a redirect.
    if respid == len(satsurv.questions):
        print("true") 
        return render_template('thanks.html')
    elif respid > len(satsurv.questions):
        return redirect('questions.html', qnum=respid + 1, question = question)

    else:
        print(respid, len(satsurv.questions))
        # question = satsurv.questions[respid].question
        """Take user to homepage of survey."""
        return render_template('questions.html', qnum=respid + 1, question = question)

@app.route("/answer", methods=["POST"])
def append_to_responses():
    """saves response in responses[] and proceeds to next question."""
    answer = request.form['answer']
    responses.append(answer)

    # if (len(responses) == len(survey.questions)):
    #     return redirect("/surv_complete")
    # else:
    print(responses)
    return redirect(f"/questions/{len(responses)}")

# ------------------------------- 
# ------------------------------- 

# Cookie demo 1 hard-coding
# Basic route:
# @app.route('/demo')
# def res_demo():
#     return "<h1>HELLO!!</h1>"

# Same idea, but with response saved to a variable:
# @app.route('/demo')
# def res_demo():
#     content = "<h1>HELLO!!</h1>"
#     resp = make_response(content)
#     resp.set_cookie('gummi1', 'blue')
#     resp.set_cookie('gummi2', 'red') 
#     return resp

#Cookie demo 2 from form
@app.route("/form-cookie")
def show_form():
    """Form that prompts favorite color."""
    return render_template("form-cookie.html")

@app.route("/handle-form-cookie")
def handle_form():
    fav_color = request.args["fav_color"]
    html = render_template("response-cookie.html", fav_color=fav_color)
    resp = make_response(html)
    resp.set_cookie("fav_color", fav_color)
    return resp