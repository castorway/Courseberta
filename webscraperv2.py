import requests
import json
from bs4 import BeautifulSoup
import time
import GetProfs

catalog = requests.get('https://apps.ualberta.ca/catalogue/course')
catalog_soup = BeautifulSoup(catalog.text, "html.parser")

# all urls for courses are in <li><a href=url>CMPUT courses</a></li>

li_elems = catalog_soup.find_all('li')

Professor_Ratings = GetProfs.GetProfessors([1407,17474,1409]) # [1407,17474,1409]

Prof_Json_List = list()

f = open("CourseAndProfs.json", "w")

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

            Course_info = requests.get(new_url_course)
            Instructors_soup = BeautifulSoup(Course_info.text, "html.parser")

            link_list = Instructors_soup.find_all('a')

            Prof_Text = ""
            Prof_Set = set()
            ProfList = list()
            

            for link in link_list:
                if link.get('href') != None and len(link.get('href')) >= 22 and link.get('href')[0:22] == "/catalogue/instructor/":

                    Instructors_Page = 'https://apps.ualberta.ca' + link.get('href')
                    
                    Instructor_page_catalog = requests.get(Instructors_Page)
                    Instructors_page_soup = BeautifulSoup(Instructor_page_catalog.text, "html.parser")

                    Instructor_Name = Instructors_page_soup.find("h2", {"class":"card-title"}).text.split(',')[0]
                    if not(Instructor_Name in Prof_Set):
                        Prof_Set.add(Instructor_Name)
                        Rating = Professor_Ratings.get(Instructor_Name,GetProfs.Professor(Instructor_Name,0,"N/A"))
                        ProfList.append({"Name": Instructor_Name, "Rating": Rating.overall_rating, "NumOfRatings": Rating.num_of_ratings}) 
                        
                        Prof_Text = Prof_Text + '\t' + Instructor_Name + ', Rating: '+ Rating.overall_rating + '\n'

                                
                                
                        
                        

            if len(Prof_Text) > 0:
                print(Instructors_soup.find("h2", {"class":"m-0"}).text+': ')
                Course_Split = Instructors_soup.find("h2", {"class":"m-0"}).text.split('-')[0].strip().split(' ')
                Course_Name = Instructors_soup.find("h2", {"class":"m-0"}).text.split('-')[1].strip()
                                               
                Course_Accronym = " ".join(Course_Split[0:len(Course_Split)-1])
                Course_Number = " ".join(Course_Split[len(Course_Split)-1])
                Prof_Json_List.append({"Accronym": Course_Accronym, "Number": Course_Number, "Professors": ProfList})
                print(Prof_Text)

JsonString = json.dumps(Prof_Json_List)
f.write(JsonString)
f.close()



            
