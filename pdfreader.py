# PIP libraries
import pdfminer.high_level
import borb
from borb.pdf.canvas.color.color import HexColor
from borb.pdf.page.page import Page
from borb.pdf.pdf import PDF

skill_list = {
    'Achiever' : 1,
    'Arranger' : 1,
    'Belief' : 1,
    "Consistency" : 1,
    "Deliberative" : 1,
    "Discipline" : 1,
    "Focus" : 1,
    "Responsibility" : 1,
    "Restorative" : 1,
    "Activator" : 1,
    "Command" : 1,
    "Communication" : 1,
    "Competition" : 1,
    "Maximizer" : 1,
    "Self-Assurance" : 1,
    "Significance" : 1,
    "Woo" : 1,
    "Adaptability" : 1,
    "Connectedness" : 1,
    "Developer" : 1,
    "Empathy" : 1,
    "Harmony" : 1,
    "Includer" : 1,
    "Individualization" : 1,
    "Positivity" : 1,
    "Relator" : 1,
    "Analytical" : 1,
    "Context" : 1,
    "Futuristic" : 1,
    "Ideation" : 1,
    "Input" : 1,
    "Intellection" : 1,
    "Learner" : 1,
    "Strategic" : 1,
}

save_name_history = False

def take_name_from_pdf(text):
    res = ""
    yes = False
    cnt = 0
    for word in text:
        if (word == b'teamwork.'):
            yes = True
            continue
        #print(word.decode("utf-8", errors='ignore'))
        if(yes):
            res += word.decode('utf-8', errors='ignore')
            #res += word
            break

    txt_file = open('test_text.txt', 'w')
    txt_file.truncate(0)
    txt_file.close()
    global save_name_history
    if(save_name_history == True):
        txt_file = open("Name_history.txt", "a+")
        txt_file.write(res + "\n")
        txt_file.close()
    return res


def take_info_from_pdf(PDF_Name):

    if(PDF_Name[-1] != 'f' and PDF_Name[-2] != 'd' and PDF_Name[-3] != 'p' and PDF_Name[-4] != '.'):
        return ["invalid PDF", "unknown file type"]

    with open(PDF_Name, "rb") as pdf_file_handle:
        input_pdf = PDF.loads(pdf_file_handle)

    first_page = borb.pdf.Document()
    first_page.append_page(input_pdf.get_page(0))

    with open("first_page.pdf", "wb") as pdf_out_handle:
        PDF.dumps(pdf_out_handle, first_page)
    pdf_out_handle.close()

    pdf_file = open("first_page.pdf", "rb")
    txt_file = open("test_text.txt", "a+")

    try:
        pdfminer.high_level.extract_text_to_fp(pdf_file, txt_file)
    except UnicodeEncodeError:
        return ["invalid PDF", "unknown symbols"]
    except:
        return ["invalid PDF", "unreadable"]

    pdf_file.close()
    txt_file.close()
    txt_file = open("test_text.txt", "rb")

    text = txt_file.readline()
    a = text.split()
    cnt = 0
    skills = []
    for i in a:
        #print(i.decode('unicode_escape'), end=' ')
        if(i == b"STRENGTHEN" or i == b"NAVIGATE"):# or i == b'\xaSTRENGTHEN'):
            continue
        """ 
        if(cnt > 100):
            break
        """
        global skill_list
        try:
            if(skill_list[i.decode("unicode_escape")] == 1):
                #print(i.decode('unicode_escape'), end = ' ')
                skills.insert(0, i.decode('unicode_escape'))
        except:
           #print("не работает  : (")
            pass

        cnt += 1

    skills.reverse()
    txt_file.close()

    cnt = 0
    for i in skills:
        try:
            cnt += skill_list[i]
        except :
           return ["invalid PDF", "skills_error"]
        if(cnt == 34):
            break
    if(cnt != 34):
        return ["invalid PDF", "not_a_GALLUP"]
    name_from_pdf = take_name_from_pdf(a)

    #print(name_from_pdf)

    if(name_from_pdf == ""):
        name_from_pdf = "Dear User"

    return [skills, name_from_pdf]


"""
inf = take_info_from_pdf("ASSYLKHAN.pdf")
print(inf)
"""

"""
skills = take_skills_from_pdf("salih.pdf")
print(skills)
skills = take_skills_from_pdf("test2.pdf")
print(skills)
"""