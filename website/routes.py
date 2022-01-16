from flask import Blueprint, render_template, request, flash, redirect, url_for
from flask_login import login_required, current_user
from . import models
from . import db

# blueprint object of all the routes defined in this file
routes = Blueprint('routes', __name__)

# ('/') defines root route, or index
# this is the ask/answer/view page
@routes.route('/', methods=['GET', 'POST'])
@login_required
def home():

    print(request, request.form, flush=True)

    if request.method == 'POST':
        # if form submitted from the ASK modal
        if 'questionMessage' in request.form:
            course_tag = request.form['courseTag']
            course_number = request.form['courseNumber']
            question = request.form['questionMessage']

            print('> ask submitted', course_tag, course_number, question, flush=True)
            
            # add question to database
            question = models.Question(course_acronym=course_tag, course_number=course_number, question=question)
            db.session.add(question)
            db.session.commit()

            return render_template('home.html', user=current_user)

        # if form submitted from the ANSWER modal
        elif 'answerSubmit' in request.form:
            answer = request.form['message']

            print('> answer submitted', answer, flush=True)
            
            # TODO: do this

        # if VIEW button clicked
        elif 'view' in request.form:
            return redirect(url_for('routes.view'))

    else:
        return render_template('home.html', user=current_user)

@routes.route('/view', methods=['GET', 'POST'])
def view():
    return render_template('view.html', user=current_user)