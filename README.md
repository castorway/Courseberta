<p align="center">
  <img width="128" height="128" src="website/static/shield.svg">
</p>
<h1 align="center">Courseberta</h1>

Courseberta is here to help you get your questions answered. Make an account and ask/answer questions through a clean and streamlined interface. Like others' answers if you agree and check out a list of profs teaching the current or upcoming semester for any course taught at the UofA.

The devpost for the project can be found [here](https://devpost.com/software/courseberta).

## Inspiration
As students, we want to be able to quickly learn about the courses we are taking, ideally through first-hand information. Websites and apps like Reddit and Discord, are useful, but disorganized; they can require digging in order to find specific topics. Our webapp is organized with the intent to make the question-and-answer process as direct as possible. It organizes all the courses out in a neat manner and keeps questions attached to the course the question is about. This way, students don’t have to go digging around to find posts about previous topics--information is exponentially easier to find!

## What it does
Our app allows students to ask, answer, and view questions on specific courses. Questions are found under the related course, making it much easier for students to find information about the particular course they are interested in. A Ratings page allows students to check the ratings of professors that are currently teaching the course *for* that particular course, using data parsed from [ratemyprofessors.com](https://www.ratemyprofessors.com/).

## How we built it
We used HTML, CSS, and Bootstrap 5 for the front end of the website. For the backend, we used Flask, Python, and some Javascript. We also used Jinja to connect the backend and frontend. We developed two custom webscrapers using [beautifulsoup4](https://www.crummy.com/software/BeautifulSoup/), and added sentiment analysis of questions and answers with [text2emotion](https://github.com/aman2656/text2emotion-library). We used Twilio and SendGrid APIs to securely send verification codes to users' email addresses when signing up. We built the webapp using a VSCode extension called LiveShare, which allowed all of us to work together on the same project in real time.

## Challenges we ran into
One of the common IP address provided by SendGrid (which we used for email verification) was put on a blacklist, preventing us from sending verification emails to @ualberta.ca domains. It was unbanned later in the hackathon. We later ran into problems with Twilio request limits. Finally, we made the mistake of uploading our .env files to our Github repository--when the repository was made public, our SendGrid account was suspended since we had accidentally posted our API keys publicly. This was a valuable lesson!

VSCode liveshare would also constantly reformat our code after saves, and randomly revert back to older versions of the code. It also appeared to write random code that we were unable to delete. In the webscraper part of our project, the JSON files we generated took about 30 minutes just to process because of how much information they contained. It was also difficult to create such a complex application on a single webpage since we used models to display all of our information.

## Accomplishments that we're proud of
We are very proud of the overall complexity of our webapp. We think we managed to implement a large amount of functionality in the given time frame. We are also very proud of the overall design of our website; we worked hard to make it minimalistic and elegant.

## What we learned
We learned a lot about webscraping and backend development with Javascript. We also learned what happens when you accidentally upload an API key to Github.

## What's next for Courseberta
We want to host the website because it is currently only hosted locally; if hosted, we feel that it could be a really helpful resource for students. We could expand to other universities and their courses. We could also allow students to rate professors directly from Courseberta, in order to stay true to our design philosophy of keeping all the functionality students might need in one place.
