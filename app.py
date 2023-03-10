from flask import Flask, request, render_template, redirect, flash
from surveys import *
from flask_debugtoolbar import DebugToolbarExtension


app = Flask(__name__)

app.secret_key="anystringhere"

responses  = []

@app.route("/")
def root():
    """Begin the survey"""
    return render_template("home.html", title=satisfaction_survey.title, instructions=satisfaction_survey.instructions)


@app.route("/questions/<int:qnum>")
def question(qnum):
    """present a form for the current question"""

    q_list=satisfaction_survey.questions

    #Make sure the user hasn't skipped any questions
    if qnum > len(responses):
        flash("Please answer the questions in order.")
        return redirect("/questions/" + str(len(responses)))

    # #make sure the user can't go back once the survey is complete
    # if len(responses) >= len(q_list):
    #     flash("Sorry, you can't change your answers once the survey is complete.")
    #     return render_template("finnished.html", answers=responses)  

    #Send the user forward    
    if qnum < len(q_list):
         return render_template("question_form.html", choices=q_list[qnum].choices, current_question=q_list[qnum].question, title=satisfaction_survey.title, instructions=satisfaction_survey.instructions, q_num = qnum)
    else:
        return render_template("finnished.html", answers=responses)     


@app.route("/questions/submit")
def record_response():
    """Record the response and redirect user to the next question"""

    #make sure the user can't go back once the survey is complete
    if len(responses) >= len(satisfaction_survey.questions):
        flash("Sorry, you can't change your answers once the survey is complete.")
        return render_template("finnished.html", answers=responses)  

    q_num=int(request.args["answer_num"])
    response=request.args["answer"]

    #Replace response if already answered.
    if 0 <= q_num < len(responses):
        responses[q_num]=response
    else:
        responses.append(response)

    return redirect("/questions/"+ str(q_num+1))
