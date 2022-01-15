import requests
from bs4 import BeautifulSoup


def create_course_list():
    catalog = requests.get('https://apps.ualberta.ca/catalogue/course')
    catalog_soup = BeautifulSoup(catalog.text, "html.parser")

    # all urls for courses are in <li><a href=url>CMPUT courses</a></li>

    li_elems = catalog_soup.find_all('li')
    course_set = set()

    course_number_list = list()
    course_name_list = list()

    for li in li_elems:
        url_end = li.a.get('href')
        new_url = "https://apps.ualberta.ca" + url_end
        if url_end[0:18] == "/catalogue/course/":
            courses = requests.get(new_url)
            course_soup = BeautifulSoup(courses.text, "html.parser")
            course_names = course_soup.find_all('h4', class_ = 'flex-grow-1')
            for name in course_names:
                name_lines = name.text.strip().splitlines()
                course_number = name_lines[0].split('-')[0].strip()
                course_name = name_lines[0].split('-')[1].strip()
                if not (course_number in course_set):
                    course_set.add(course_number)
                    course_number_list.append(course_number)
                    course_name_list.append(course_name)

    return(course_number_list,course_name_list)


if __name__ == '__main__':
    print(create_course_list())
                