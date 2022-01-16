import requests
import json
from bs4 import BeautifulSoup

catalog = requests.get('https://apps.ualberta.ca/catalogue/course')
catalog_soup = BeautifulSoup(catalog.text, "html.parser")

# all urls for courses are in <li><a href=url>CMPUT courses</a></li>

li_elems = catalog_soup.find_all('li')

for li in li_elems:
    url_end = li.a.get('href')
    new_url = "https://apps.ualberta.ca" + url_end
    if url_end[0:18] == "/catalogue/course/":
        courses = requests.get(new_url)
        course_soup = BeautifulSoup(courses.text, "html.parser")
        course_names = course_soup.find_all('a', class_ = 'btn-secondary')
        for button in course_names:
            url_course = button.get('href')
            new_url_course = "https://apps.ualberta.ca" + url_course

            Course_info = requests.get('https://apps.ualberta.ca/catalogue/course')
            Instructors_soup = BeautifulSoup(Course_info.text, "html.parser")

            link_list = Instructors_soup.find_all('a')
            for link in link_list:
                if link.get('href')[0:22] == "/catalogue/instructor/":

                    Instructor_page_catalog = requests.get('https://apps.ualberta.ca' + link.get('href'))
                    Instructors_page_soup = BeautifulSoup(Course_info.text, "html.parser")

                    print(Instructors_page_soup.find("h2", {"class":"card-title.mb-2"}))


            
