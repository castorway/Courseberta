from flask import Blueprint, render_template, request, flash, redirect, url_for, session
from flask_login import login_required, current_user
from . import models
from . import db
import text2emotion as te
import json

# Prof Dictionary //CoursesAndProfs.json
f = open("CoursesAndProfs.json")
FileData = f.read()
f.close()

CourseData = json.loads(FileData)

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
                return render_template('home.html', user=current_user, 
                    show_modal="questionModal", error_text="Please pick a course name.")
            elif len(course_number) == 0:
                return render_template('home.html', user=current_user, 
                    show_modal="questionModal", error_text="Please enter a course id.")
            elif len(course_number) <= 2:
                return render_template('home.html', user=current_user, 
                    show_modal="questionModal", error_text="Please enter a valid course id.")
            elif len(text) <= 2:
                return render_template('home.html', user=current_user, 
                    show_modal="questionModal", error_text="Please enter your question.")

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
            return render_template('home.html', user=current_user, show_modal="questionModal", validated=validated)

        # if form submitted from Answer #1 (for choosing a course)
        elif form_submit == "answer1":
            course_tag = request.form['courseTag']
            course_number = request.form['courseNumber']
            
            if course_tag == "base":
                return render_template('home.html', user=current_user, 
                    show_modal="answerModal1", error_text="Please pick a course name.")
            elif len(course_number) == 0:
                return render_template('home.html', user=current_user, 
                    show_modal="answerModal1", error_text="Please enter a course id.")
            elif len(course_number) <= 2:
                return render_template('home.html', user=current_user, 
                    show_modal="answerModal1", error_text="Please enter a valid course id.")

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

            return render_template('home.html', user=current_user, show_modal="answerModal3", 
                question=question)
            
           # answer = models.Answer(course_acronym=course_acronym, course_number=course_number, question=question)
        
        elif form_submit == "answer3":
            text = request.form['answerMessage']

            question_id = request.form['questionSelected']
            question = models.Question.query.get(int(question_id))

            if len(text) <= 5:
                return render_template('home.html', user=current_user,
                    error_text="Please enter your answer.")
            
            print("> got answer:", text)
            print("> question selected:", question_id, question.question)

            answer = models.Answer(answer=text, question=question)  
            db.session.add(answer)   
            db.session.commit()       

            flash("Your answer has been submitted.", category="success")
            return render_template('home.html', user=current_user)


        elif form_submit == "view1":

            course_tag = request.form['courseTag']
            course_number = request.form['courseNumber']
            
            if course_tag == "base":
                return render_template('home.html', user=current_user, 
                    show_modal="answerModal1", error_text="Please pick a course name.")
            elif len(course_number) == 0:
                return render_template('home.html', user=current_user, 
                    show_modal="answerModal1", error_text="Please enter a course id.")
            elif len(course_number) <= 2:
                return render_template('home.html', user=current_user, 
                    show_modal="answerModal1", error_text="Please enter a valid course id.")

            questions = models.Question.query.filter_by(course_acronym=course_tag, course_number=course_number)
            print("> Got questions\n", [q.question for q in questions])

            # show_answer2 should cause page to automatically show modal for seeing list of questions
            return render_template('home.html', user=current_user, show_modal="viewModal2",
                course_tag=course_tag, course_number=course_number, questions=questions)
            
        elif form_submit == "rating1":
            course_tag = request.form['courseTag']
            course_number = request.form['courseNumber']

            try:
                ProfList = CourseData[course_tag][course_number]
                for di in ProfList:
                    print(di['Name'], di['Rating'], di['NumOfRatings'])
                    """
                    GT Lee N/A 0
                    Mesbah Sharaf 4.5 255
                    Alexander Gainer 4.2 255 
                    """

            except:
                print("Course does not exist") 
                flash("This course is not being taught in the current or next semester",category="error")
                
            if course_tag == "base":
                return render_template('home.html', user=current_user, 
                    show_modal="answerModal1", error_text="Please pick a course name.")
            elif len(course_number) == 0:
                return render_template('home.html', user=current_user, 
                    show_modal="answerModal1", error_text="Please enter a course id.")
            elif len(course_number) <= 2:
                return render_template('home.html', user=current_user, 
                    show_modal="answerModal1", error_text="Please enter a valid course id.")

            # show_answer2 should cause page to automatically show modal for seeing list of professors
            return render_template('home.html', user=current_user, show_modal="ratingModal2",
                course_tag=course_tag, course_number=course_number, profs=ProfList)

        


    else:
        return render_template('home.html', user=current_user)

@routes.route('/view', methods=['GET', 'POST'])
def view():
    return render_template('view.html', user=current_user)