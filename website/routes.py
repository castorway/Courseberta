from flask import Blueprint, render_template, request, flash, redirect, url_for, session
from flask_login import login_required, current_user
from . import models
from . import db
import text2emotion as te
import json

# needed for sentiment analysis
import nltk
nltk.download('omw-1.4')

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
                    show_modal="questionModal", 
                    modal_errors=[{
                        "text": "Please pick a course name.",
                        "modal": "questionModal"}])
            elif len(course_number) == 0:
                return render_template('home.html', user=current_user, 
                    show_modal="questionModal", modal_errors=[{
                        "text": "Please enter a course ID.",
                        "modal": "questionModal"}])
            elif len(course_number) <= 2:
                return render_template('home.html', user=current_user, 
                    show_modal="questionModal", modal_errors=[{
                        "text": "Please enter a valid course ID.",
                        "modal": "questionModal"}])
            elif len(text) <= 2:
                return render_template('home.html', user=current_user, 
                    show_modal="questionModal", modal_errors=[{
                        "text": "Please enter your question.",
                        "modal": "questionModal"}])

            else:
                print('> ask submitted:', course_tag, course_number, text, flush=True)
                
                # add question to database
                question = models.Question(course_acronym=course_tag, course_number=course_number, question=text)
                
                emotion = te.get_emotion(text) # returns a dictionary, eg {"Happy": 0.53}
                maxemotion = max(emotion, key=emotion.get) # use key=emotion.get to sort by dict values

                # if maxemotion is 0 then all emotions were 0, so pick Neutral
                if emotion[maxemotion] == 0:
                    maxemotion = "Neutral"

                question = models.Question(course_acronym=course_tag, course_number=course_number, question=text, sentiment=maxemotion)

                print('Emotion found:', emotion, 'max:', maxemotion)
                
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
                    show_modal="answerModal1", modal_errors=[{
                        "text": "Please pick a course name.",
                        "modal": "answerModal1"}])
            elif len(course_number) == 0:
                return render_template('home.html', user=current_user, 
                    show_modal="answerModal1", modal_errors=[{
                        "text": "Please enter a course ID.",
                        "modal": "answerModal1"}])
            elif len(course_number) <= 2:
                return render_template('home.html', user=current_user, 
                    show_modal="answerModal1", modal_errors=[{
                        "text": "Please enter a valid course ID.",
                        "modal": "questionModal"}])

            # store in session so we know what the incoming answer is for
            # session['current_course'] = [course_tag, course_number]

            questions = models.Question.query.filter_by(course_acronym=course_tag, course_number=course_number)
            print("> Got questions\n", [q.question for q in questions])

            # show_answer2 should cause page to automatically show modal for seeing list of questions
            return render_template('home.html', user=current_user, show_modal="answerModal2",
                course_tag=course_tag, course_number=course_number, questions=questions)

        # if form submitted from Answer #2 (for choosing a question to answer)
        elif form_submit == "answer2":
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

            emotion = te.get_emotion(text) # returns a dictionary, eg {"Happy": 0.53}
            maxemotion = max(emotion, key=emotion.get) # use key=emotion.get to sort by dict values

            # if maxemotion is 0 then all emotions were 0, so pick Neutral
            if emotion[maxemotion] == 0:
                maxemotion = "Neutral"

            answer = models.Answer(answer=text, sentiment=maxemotion, question=question)

            db.session.add(answer)   
            db.session.commit()       

            flash("Your answer has been submitted.", category="success")
            return render_template('home.html', user=current_user)


        elif form_submit == "view1":

            course_tag = request.form['courseTag']
            course_number = request.form['courseNumber']
            
            if course_tag == "base":
                return render_template('home.html', user=current_user, 
                    show_modal="viewModal1", modal_errors=[{
                        "text": "Please pick a course name.",
                        "modal": "viewModal1"}])
            elif len(course_number) == 0:
                return render_template('home.html', user=current_user, 
                    show_modal="viewModal1", modal_errors=[{
                        "text": "Please enter a course ID.",
                        "modal": "viewModal1"}])
            elif len(course_number) <= 2:
                return render_template('home.html', user=current_user, 
                    show_modal="viewModal1", modal_errors=[{
                        "text": "Please enter a valid course ID.",
                        "modal": "viewModal1"}])

            questions = models.Question.query.filter_by(course_acronym=course_tag, course_number=course_number)
            print("> Got questions\n", [q.question for q in questions])

            # set session variables for view2
            session['current_course_info'] = {
                "course_tag": course_tag,
                "course_number": course_number
            }

            # get ratings for this user that are positive
            my_ratings = models.Rating.query.filter_by(user_id=current_user.id, value=1)
            pos_rated_ans_ids = [r.answer_id for r in my_ratings]

            # show_answer2 should cause page to automatically show modal for seeing list of questions
            return render_template('home.html', user=current_user, show_modal="viewModal2",
                course_tag=course_tag, course_number=course_number, questions=questions,
                pos_rated_ans_ids=pos_rated_ans_ids)

        elif form_submit.startswith("view2"):

            answer_id = int(request.form["answerSelected"])
            ratings = models.Rating.query.filter_by(user_id=current_user.id, answer_id=answer_id)

            print("got ratings:", [r.user_id for r in ratings])

            if ratings:
                # if the user has already rated this answer, toggle the rating

                rating = ratings[0]
                rating.value = 1 if rating.value == 0 else 0 # toggle

                answer = models.Answer.query.get(int(answer_id))
                # then we need to change value of answer
                if rating.value == 1:
                    answer.agree += 1
                else:
                    answer.agree -= 1

            else:
                # user hasnt rated yet

                # add new rating
                rating = models.Rating(user_id=current_user.id, answer_id=answer_id, value=1)
                db.session.add(rating)

                # increment answer.agree
                answer = models.Answer.query.get(answer_id)
                answer.agree += 1

            # commit changes
            db.session.commit()

            # need to rerender view2

            course_tag = session['current_course_info']['course_tag']
            course_number = session['current_course_info']['course_number']

            questions = models.Question.query.filter_by(course_acronym=course_tag, course_number=course_number)
            print("> Got questions\n", [q.question for q in questions])

            # get ratings for this user
            my_ratings = models.Rating.query.filter_by(user_id=current_user.id)
            pos_rated_ans_ids = [r.answer_id for r in my_ratings]

            return render_template('home.html', user=current_user, show_modal="viewModal2",
                course_tag=course_tag, course_number=course_number, questions=questions,
                pos_rated_ans_ids=pos_rated_ans_ids)
            
        elif form_submit == "rating1":
            course_tag = request.form['courseTag']
            course_number = request.form['courseNumber']
            
            # input validation
            if course_tag == "base":
                return render_template('home.html', user=current_user, 
                    show_modal="ratingModal1", modal_errors=[{
                        "text": "Please pick a course name.",
                        "modal": "ratingModal1"}])
            elif len(course_number) == 0:
                return render_template('home.html', user=current_user, 
                    show_modal="ratingModal1", modal_errors=[{
                        "text": "Please enter a course ID.",
                        "modal": "ratingModal1"}])
            elif len(course_number) <= 2:
                return render_template('home.html', user=current_user, 
                    show_modal="ratingModal1", modal_errors=[{
                        "text": "Please enter a valid course ID.",
                        "modal": "ratingModal1"}])

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
                return render_template('home.html', user=current_user, show_modal="ratingModal1",
                    modal_errors=[{
                        "text": "This course is not being taught in the current or next semester.",
                        "modal": "ratingModal1"}])
                
            if course_tag == "base":
                return render_template('home.html', user=current_user, 
                    show_modal="ratingModal1", modal_errors=[{
                        "text": "Please pick a course name.",
                        "modal": "ratingModal1"}])
            elif len(course_number) == 0:
                return render_template('home.html', user=current_user, 
                    show_modal="ratingModal1", modal_errors=[{
                        "text": "Please enter a course ID.",
                        "modal": "ratingModal1"}])
            elif len(course_number) <= 2:
                return render_template('home.html', user=current_user, 
                    show_modal="ratingModal1", modal_errors=[{
                        "text": "Please enter a valid course ID.",
                        "modal": "ratingModal1"}])

            # show_answer2 should cause page to automatically show modal for seeing list of professors
            return render_template('home.html', user=current_user, show_modal="ratingModal2",
                course_tag=course_tag, course_number=course_number, profs=ProfList)


    else:
        return render_template('home.html', user=current_user)

@routes.route('/view', methods=['GET', 'POST'])
def view():
    return render_template('view.html', user=current_user)