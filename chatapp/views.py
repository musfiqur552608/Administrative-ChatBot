from asyncio.windows_events import NULL
from django.shortcuts import render
from django.http import HttpResponse, JsonResponse
from django.core.files import File
from .models import *

####################################
import nltk
# nltk.download('omw-1.4')
# nltk.download('averaged_perceptron_tagger')
import random
import re, string, unicodedata
from nltk.corpus import wordnet as wn
from nltk.stem.wordnet import WordNetLemmatizer
from collections import defaultdict
import warnings

warnings.filterwarnings("ignore")
# nltk.download('punkt')
# nltk.download('wordnet')
from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.metrics.pairwise import cosine_similarity, linear_kernel
from django.views.decorators.csrf import csrf_exempt
####################################

from nltk.chat.util import Chat, reflections
from chatterbot import ChatBot
from chatterbot.trainers import ListTrainer

reflections = {
  "i am"       : "you are",
  "i was"      : "you were",
  "i"          : "you",
  "i'm"        : "you are",
  "i'd"        : "you would",
  "i've"       : "you have",
  "i'll"       : "you will",
  "my"         : "your",
  "you are"    : "I am",
  "you were"   : "I was",
  "you've"     : "I have",
  "you'll"     : "I will",
  "your"       : "my",
  "yours"      : "mine",
  "you"        : "me",
  "me"         : "you"
}
pairs = [
    [
        r"my name is (.*)",
        ["Hello %1, How are you today ?",]
    ],
    [
        r"hi|hey|hello",
        ["Hello", "Hey there",]
    ],
    [
        r"what is your name ?",
        ["I am a bot created by ROAM TEAM. you can call me MUSU!",]
    ],
    [
        r"how are you ?",
        ["I'm doing good, How about You ?",]
    ],
    
    [
        r"sorry (.*)",
        ["Its alright","Its OK, never mind",]
    ],
    [
        r"I am fine",
        ["Great to hear that, How can I help you?",]
    ],
    [
        r"i'm (.*) doing good",
        ["Nice to hear that","How can I help you?:)",]
    ],
    [
        r"(.*) age?",
        ["I'm a computer program dude, Seriously you are asking me this?",]
    ],
    [
        r"what (.*) want ?",
        ["Make me an offer I can't refuse",]
    ],
    [
        r"(.*) created ?",
        ["Raghav created me using Python's NLTK library ","top secret ;)",]
    ],
    [
        r"(.*) (location|city) ?",
        ['Indore, Madhya Pradesh',]
    ],
    [
        r"how is weather in (.*)?",
        ["Weather in %1 is awesome like always","Too hot man here in %1","Too cold man here in %1","Never even heard about %1"]
    ],
    [
        r"i work in (.*)?",
        ["%1 is an Amazing company, I have heard about it. But they are in huge loss these days.",]
    ],
    [
        r"(.)raining in (.)",
        ["No rain since last week here in %2","Damn its raining too much here in %2"]
    ],
    [
        r"how (.) health(.)",
        ["I'm a computer program, so I'm always healthy ",]
    ],
    [
        r"No",
        ["Please check the student id again",]
    ],
    [
        r"Tell me about my child",
        ["What is your child's student id?"]
    ],
    [
        r"Please, Tell me about my child",
        ["What is your child's student id?"]
    ],
    [
        r"Tell me about my student",
        ["What is your student's student id?"]
    ],
    [
        r"Yes",
        ["Please ask me about your clild, what you want"]
    ],
    [
        r"quit",
        ["Bye take care. See you soon :) ","It was nice talking to you. See you soon :)"]
    ],
]

welcome_input = ["what's up","hey", "hello", "hi", "greetings",]
welcome_response = ["hi", "hey",  "hi there", "hello",]


def welcome(user_response):
    for word in user_response.split():
        if word.lower() in welcome_input:
            return random.choice(welcome_response)

def Normalize(text):
    remove_punct_dict = dict((ord(punct), None) for punct in string.punctuation)
    # word tokenization
    word_token = nltk.word_tokenize(text.lower().translate(remove_punct_dict))

    # remove ascii
    new_words = []
    for word in word_token:
        new_word = unicodedata.normalize('NFKD', word).encode('ascii', 'ignore').decode('utf-8', 'ignore')
        new_words.append(new_word)

    # Remove tags
    rmv = []
    for w in new_words:
        text = re.sub("&lt;/?.*?&gt;", "&lt;&gt;", w)
        rmv.append(text)

    # pos tagging and lemmatization
    tag_map = defaultdict(lambda: wn.NOUN)
    tag_map['J'] = wn.ADJ
    tag_map['V'] = wn.VERB
    tag_map['R'] = wn.ADV
    lmtzr = WordNetLemmatizer()
    lemma_list = []
    rmv = [i for i in rmv if i]
    for token, tag in nltk.pos_tag(rmv):
        lemma = lmtzr.lemmatize(token, tag_map[tag[0]])
        lemma_list.append(lemma)
    return lemma_list




def bot(user_response):
  chat=Chat(pairs,reflections)
  return chat.respond(user_response)

def generateResponse(sent_tokens, user_response):
    u_res = user_response
    robo_response = ''
    if sent_tokens == ['']:
        sent_tokens = []
    if sent_tokens != []:
        sent_tokens.append(user_response)
        TfidfVec = TfidfVectorizer(tokenizer=Normalize, stop_words='english')
        tfidf = TfidfVec.fit_transform(sent_tokens)
        vals = cosine_similarity(tfidf[-1], tfidf)
        idx = vals.argsort()[0][-2]
        flat = vals.flatten()
        flat.sort()
        req_tfidf = flat[-2]
        if (req_tfidf != 0):
            robo_response = robo_response + sent_tokens[idx]    
    else:
        robo_response = bot(u_res)
        print(robo_response)

    return robo_response

@csrf_exempt
def chatbot(request):
        if request.method == 'POST':
            user_response = request.POST['question']
            student_data = Student.objects.all()
            id = "9999"
            name = "None"
            yes = "yes"
            res = "Please ask me about your clild, what you want"
            no = "no"
            ress = "Please check the student id again"
            
            for student_id in student_data:
                if user_response == str(student_id):
                    id = [str(student_id)]
                    name = ["Is your child name {name}".format(name=student_id.student_name)]
                    
                
                    with open('files\\student.txt', 'w', encoding='utf-8') as file:
                        if student_id.student_gender=="male":
                            file.write("The child name is {name}. His student id is {student_id}. His total subjects are {total_subject}. His total obtained mark is {obtained_mark}. His grade is {grade}. His merit rank in class {class_rank}. His merit rank in section {section_rank}. His total paid money {paid}. His total due money {due}.".format(name=student_id.student_name,student_id=student_id, total_subject=student_id.total_subject, obtained_mark=student_id.total_obtain_mark, grade=student_id.total_grade_point, class_rank=student_id.merit_rank_in_class, section_rank=student_id.merit_rank_in_section, paid=student_id.paid, due=student_id.due))
                        else: 
                            file.write("The child name is {name}. Her student id is {student_id}. Her total subjects are {total_subject}. Her total obtained mark is {obtained_mark}. Her grade is {grade}. Her merit rank in class {class_rank}. Her merit rank in section {section_rank}. Her total paid money {paid}. Her total due money {due}.".format(name=student_id.student_name,student_id=student_id, total_subject=student_id.total_subject, obtained_mark=student_id.total_obtain_mark, grade=student_id.total_grade_point, class_rank=student_id.merit_rank_in_class, section_rank=student_id.merit_rank_in_section, paid=student_id.paid, due=student_id.due))
                    break
            data = open('files\\student.txt', 'r', errors='ignore')
            raw = data.read()
            raw = raw.lower()
            sent_tokens = raw.split('.')
            def student(user_response):
                for word in user_response.split():
                    if word.lower() in id:
                        return name
            def yess(user_response):
                for word in user_response.split():
                    if word.lower() in yes:
                        return res
            def noo(user_response):
                for word in user_response.split():
                    if word.lower() in no:
                        return ress

            user_response = user_response.lower()
            if (user_response not in ['bye', 'shutdown', 'exit', 'quit']):
                if (user_response == 'thanks' or user_response == 'thank you'):
                    mydict = "You are welcome.."
                else:
                    if (welcome(user_response) != None):
                        mydict = welcome(user_response)
                    elif(student(user_response) != None):
                        mydict = student(user_response)
                    elif(yess(user_response) != None):
                        mydict = yess(user_response)
                    elif(noo(user_response) != None):
                        mydict = noo(user_response)
                    else:
                        mydict = generateResponse(sent_tokens, user_response)
            else:
                mydict =  "Thanks for connecting me. Bye!!! "
                file = open("files\\student.txt","r+")
                file.truncate(0)
        return JsonResponse({"response": mydict})
#############################################################################

def home(request):
    return render(request, 'index.html')