import requests
import json
import math

class Professor:
    def __init__(self, name, num_of_ratings, overall_rating):
        self.name = name
        self.num_of_ratings = num_of_ratings
        self.overall_rating = overall_rating

def GetProfAmount(ID):
    page = requests.get("http://www.ratemyprofessors.com/filter/professor/?&page=1&filter=teacherlastname_sort_s+asc&query=*%3A*&queryoption=TEACHER&queryBy=schoolId&sid="+ str(ID))  # get request for page
    temp_jsonpage = json.loads(page.content)
    num_of_prof = (temp_jsonpage["remaining"] + 20)
    return num_of_prof

def GetProfessors(IDS):
    professors = dict()
    for ID in IDS:
        print(ID)
        numberOfProfs = GetProfAmount(ID)
        NumOfPages = math.ceil(numberOfProfs / 20)
        for i in range(1, NumOfPages + 1):
            page = requests.get("http://www.ratemyprofessors.com/filter/professor/?&page="+ str(i)+ "&filter=teacherlastname_sort_s+asc&query=*%3A*&queryoption=TEACHER&queryBy=schoolId&sid="+ str(ID))
            response = json.loads(page.content)
            temp_list = response["professors"]

            for prof in response["professors"]:
                professor = Professor(f"{prof['tFname']} {prof['tLname']}",prof["tNumRatings"],prof["overall_rating"])
                professors[f"{prof['tFname']} {prof['tLname']}"] = professor
    return professors

