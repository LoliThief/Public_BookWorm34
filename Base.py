#Our files
from GoogleSheetExtracter import get_value

#from pdfreader import take_info_from_pdf
#from operator import attrgetter

Number_of_books = 98

def make_float(s):
    res = s
    if(s == ' '):
        res = 0
    if(s == "0,5"):
        res = 0.5
    if (s == "-0,5"):
        res = -0.5
    if (s == "-1, 1"):
        res = 2
    if (s == "1, -1"):
        res = 2
    return res

skill_index = {
    "Achiever" : 0,
    "Arranger" : 1,
    "Belief" : 2,
    "Consistency" : 3,
    "Deliberative" : 4,
    "Discipline" : 5,
    "Focus" : 6,
    "Responsibility" : 7,
    "Restorative" : 8,
    "Activator" : 9,
    "Command" : 10,
    "Communication" : 11,
    "Competition" : 12,
    "Maximizer" : 13,
    "Self-Assurance" : 14,
    "Significance" : 15,
    "Woo" : 16,
    "Adaptability" : 17,
    "Connectedness" : 18,
    "Developer" : 19,
    "Empathy" : 20,
    "Harmony" : 21,
    "Includer" : 22,
    "Individualization" : 23,
    "Positivity" : 24,
    "Relator" : 25,
    "Analytical" : 26,
    "Context" : 27,
    "Futuristic" : 28,
    "Ideation" : 29,
    "Input" : 30,
    "Intellection" : 31,
    "Learner" : 32,
    "Strategic" : 33,
}

class Book:
    # author is a string and the rating is a integer
    def __init__(self, Title, Author, Link):
        self.title = Title
        self.author = Author
        self.disc = ""
        self.rating = float(0)
        if(Link != 0):
            self.link = Link
        else:
            self.link = "no_link"

def get_books(nfile, skills):
    library = []

    for i in range(Number_of_books):
        title = get_value(3 + i, 2)
        author = get_value(3 + i, 3)
        link = get_value(3 + i, 6)
        cur_bk = Book(title, author, link)
        library.insert(0, cur_bk)

    """
    inf = take_info_from_pdf(nfile)
    skills = inf[0]
    """

    for i in range(34):
        #print(skills[i], ' ', skill_index[skills[i]] , end=": ")
        for j in range(Number_of_books):
            cur = (get_value(3 + j, 7 + skill_index[skills[i]]))
            try:
                cur = float( make_float(cur) )
            except  ValueError:
                #print("Unknown value", type(cur), cur)
                cur = 0
            except:
                cur = 0
                print(cur)
            if(i <= 19):
                if(cur == 1 or cur == 0.5):
                    library[j].rating += (cur * (20 - i))
            if(i >= 14):
                if(cur == -1 or cur == -0.5):
                    library[j].rating += (cur * (13 - i))
            if(cur == 2):
                if(i <= 16):
                    library[j].rating += 17 - (i)
                else:
                    library[j].rating += i - 16

    return sorted(library, key=lambda x: x.rating, reverse=True)