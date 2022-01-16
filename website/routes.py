from flask import Blueprint, render_template, request, flash, redirect, url_for, session
from flask_login import login_required, current_user
from . import models
from . import db
import text2emotion as te

# blueprint object of all the routes defined in this file
routes = Blueprint('routes', __name__)

# ('/') defines root route, or index
# this is the ask/answer/view page
@routes.route('/', methods=['GET', 'POST'])
@login_required
def home():

    print('form submitted:', request.form, flush=True)

    if request.method == 'POST':
        # formSubmit button is the submit button on any form; its value
        # determines the function that should be run

        form_submit = request.form['formSubmit']

        if form_submit == "question":
            course_tag = request.form['courseTag']
            course_number = request.form['courseNumber']
            text = request.form['questionMessage']

            if course_tag == "base":
                flash("Please pick a course name.", category='error')
            elif len(course_number) == 0:
                flash("Please enter a course id.", category="error")
            elif len(course_number) <= 2:
                flash("Please enter a valid course id.", category="error")
            elif len(text) <= 5:
                flash("Please enter your question.", category="error")
            else:
                print('> ask submitted:', course_tag, course_number, text, flush=True)
                
                # add question to database
                question = models.Question(course_acronym=course_tag, course_number=course_number, question=text)
                
                emotion = te.get_emotion(text)
                
                maxemotion = max(emotion)
                print(emotion)
                print(maxemotion)
                
                db.session.add(question)
                db.session.commit()

                flash("Your question has been submitted.", category="success")
                
                # return to homepage with no modal shown
                return redirect(url_for("routes.home"))
                
            # return to question modal
            return render_template('home.html', user=current_user, show_modal="questionModal")

        # if form submitted from Answer #1 (for choosing a course)
        elif form_submit == "answer1":
            course_tag = request.form['courseTag']
            course_number = request.form['courseNumber']
            
            if course_tag == "base":
                flash("Please pick a course name.", category='error')
                return render_template('home.html', user=current_user, show_modal="answerModal1")
            elif len(course_number) == 0:
                flash("Please enter a course id.", category="error")
                return render_template('home.html', user=current_user, show_modal="answerModal1")
            elif len(course_number) <= 2:
                flash("Please enter a valid course id.", category="error")
                return render_template('home.html', user=current_user, show_modal="answerModal1")

            # store in session so we know what the incoming answer is for
            # session['current_course'] = [course_tag, course_number]

            questions = models.Question.query.filter_by(course_acronym=course_tag, course_number=course_number)
            print("> Got questions\n", [q.question for q in questions])

            # show_answer2 should cause page to automatically show modal for seeing list of questions
            return render_template('home.html', user=current_user, show_modal="answerModal2",
                course_tag=course_tag, course_number=course_number, questions=questions)

        # if form submitted from Answer #2 (for choosing a question to answer)
        elif form_submit == "answer2":
            # TODO: integrate with frontend
            question_id = request.form['questionSelected']
            question = models.Question.query.get(int(question_id))

            print("> question selected:", question_id, question.question)
            session['current_question_id'] = question_id

            return render_template('home.html', user=current_user, show_modal="answerModal3", question=question)
            
           # answer = models.Answer(course_acronym=course_acronym, course_number=course_number, question=question)
        
    else:
        return render_template('home.html', user=current_user)

@routes.route('/view', methods=['GET', 'POST'])
def view():
    return render_template('view.html', user=current_user)