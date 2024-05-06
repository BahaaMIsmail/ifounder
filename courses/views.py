from django.shortcuts import render,HttpResponse,redirect
from django.contrib.auth import authenticate,login,logout
from django.contrib.auth.decorators import login_required
from .models import * 
from .forms import *
from json import dumps
from random import shuffle
from django.core.mail import send_mail

def auth(request):
    return request.user.is_authenticated

def is_teacher(request): 
    if auth(request) :   
        if request.user.email in  ['biifounder@gmail.com','bahaaismailres@gmail.com'] : 
            return request.user.username 
    return False

def deleteAll():
    for Mod in [YearEval, SubjectEval, UnitEval, LessonEval, OutcomeEval, QEval] : 
        Mod.objects.all().delete()
    for Mod in [Year, Subject, Unit, Lesson, Outcome, Question, QDubl] : 
        Mod.objects.all().delete()

#======================================================================================================
def EmailSender(email_subject, message,receiver_emails):
        send_mail(
        email_subject,
        message,
        'biifounder@gmail.com',
        receiver_emails,
        fail_silently=False,
        )


def AddUser(request,year):  
    user=request.user  
    YearEval.objects.create(k=year, user=user)    
    for subject in  Subject.objects.filter(p=year):      
        SubjectEval.objects.create(k=subject, user=user)
        for unit in Unit.objects.filter(p=subject): 
            UnitEval.objects.create(k=unit, user=user)
            for lesson in Lesson.objects.filter(p=unit): 
                LessonEval.objects.create(k=lesson, user=user)
                for outcome in Outcome.objects.filter(p=lesson): 
                    OutcomeEval.objects.create(k=outcome, user=user)
                    for question in Question.objects.filter(p=outcome): 
                        QEval.objects.create(k=question, user=user)
    return redirect('open', year.k)

def updateUsers(Eval, k, p, y):  
    for user in User.objects.filter(y=y): 
        Eval.objects.create(k=k, user=user,p=p)

def addAdmin(request): 
    for year in Year.objects.all():
        if not YearEval.objects.filter(k=year): 
            AddUser(request, year)

def HomePage(request):  
    # deleteAll()
    # AddUser(request,Year.objects.get(name='10')) 
    if request.method == 'POST':   
        if "visitor" in request.POST:            
            y = request.POST.get('year') 
            year = Year.objects.get(name=y)
            return redirect('open', year.k)     
            
        elif "register" in request.POST:          
            form = MyUserCreationForm(request.POST)
            if form.is_valid():
                user = form.save(commit=False)
                user.name = request.POST.get('name')
                user.email = request.POST.get('email')
                user.year = request.POST.get('year')
                user.gov = request.POST.get('gov')
                user.prov = request.POST.get('prov') 
                user.school = request.POST.get('school')                
                user.save()  
                login(request, user)
                year = Year.objects.get(name=user.year)  
                AddUser(request, year)                
                return redirect('home')  
            else: 
                return HttpResponse("يوجد خطأ في تسجيلك")   
        elif "login" in request.POST:            
            email=request.POST.get('email')
            pass1=request.POST.get('pass')
            user=authenticate(request,email=email,password=pass1)            
            if user is not None:
                login(request,user) 
                return redirect('home')
            else:
                return HttpResponse ("كلمة السر خطأ")
        elif 'enquirey' in request.POST:
            email=request.POST.get('email')
            email_subject = 'from ' + email
            message = request.POST.get('message')
            EmailSender(email_subject, message, ['bahaaismailres@gmail.com'])
            return HttpResponse ("نشكركم على التواصل معنا وسوف يتم الرد على استفساركم في أقرب وقت ممكن إن شاء الله")   
    else:   
        if is_teacher(request) or not request.user.is_authenticated:             
            form = MyUserCreationForm()  
            context = {'teacher':is_teacher(request), 'years':Year.objects.all(), 'form':form}
            context['allusers'] = dumps([u.email for u in User.objects.all()])
            return render (request,'courses/home.html',context)
        else:             
            context = {'teacher':is_teacher(request)}        
            y = User.objects.get(email=request.user).year
            return redirect('open', Year.objects.get(name=y).k)
        
   
@login_required(login_url='login')
def Logout(request):
    logout(request)
    return redirect('home')


table = {
    'h':[ 'y' , '',   ''       ,  ''          ,  'الصفحة الرئيسية' ,  'الصفوف الدراسية' ],
    'y':[ 's' , 'h',   Year     ,  YearEval    ,  'صف'               ,  'المواد الدراسية' ],
    's':[ 'u' , 'y',   Subject  ,  SubjectEval ,  'مادة'             ,  'وحدات المادة'    ],
    'u':[ 'l' , 's',  Unit     ,  UnitEval    ,  'وحدة'             ,  'دروس الوحدة'     ],
    'l':[ 'o' , 'u',  Lesson   ,  LessonEval  ,  'درس'              ,  'الأهداف التعليمية في هذا الدرس'    ],
    'o':[ 'q' , 'l',  Outcome  ,  OutcomeEval ,  'مخرج'             ,  ''                 ],
    'q':[ 'd'  , 'o',  Question ,  QEval          ,  'سؤال '            ,  ''                 ],
    'd':[ ''  , 'q',  QDubl ,  ''          ,  'سؤال '            ,  ''                 ],
}


yarab = {'9':'تاسع','10':'عاشر','11':'حادي عشر'}

def Object(request, k):  
    b = k[0]   
    if k[0] == 'h': 
        return redirect('home')
    else:      
        [c, p] = table[b][:2]          
        object = table[b][2].objects.get(k=k)
        Child = table[c][2]
        Eval, ChildEval = table[b][3], table[c][3]   
        
        percent = 0 
        weaknesses = []
        auth = request.user.is_authenticated
        if auth: 
            user = request.user
            percent = Eval.objects.get(k=object, user=user).percent   
            if b == 's':
                weaknesses = [] 
                for unit in Unit.objects.filter(p=object): 
                    for lesson in Lesson.objects.filter(p=unit): 
                        for outcome in Outcome.objects.filter(p=lesson):
                            opercent = OutcomeEval.objects.get(k=outcome, user=user).score 
                            if opercent < 70: 
                                weaknesses += [[opercent, outcome.k, outcome.name]] 
                weaknesses = sorted(weaknesses)
                weaknesses = [{'percent':w[0], 'wk':w[1], 'name':w[2]} for w in weaknesses]

        context = {'teacher': is_teacher(request), 'auth':auth, 'object':object, 
                   'k':k, 'b':b, 'ara':table[b][4], 'name': object.name,
                   'percent':percent, 'weaknesses':weaknesses,                                      
                    'para':table[p][4], 
                    'cara':table[c][4],                     
                   }   
        if b == 'y': 
            context['name'] = yarab[object.name]
        if b != 'y': 
            context['p']= object.p.k
            context['parent'] = object.p.name          
        if b == 'o': 
            context['contents'] = dumps( [ cont+'.' for cont in object.content.split('.')])
            questions = []
            for question in Question.objects.filter(p=object) : 
                questions += [question]+[q for q in QDubl.objects.filter(p=question)]
            context['questions'] = questions  
            return render (request,'courses/outcome.html', context)
        else:
            context['contents'] = table[b][5]  
            children = []  
            for child in Child.objects.filter(p=object): 
                cpercent = 0 
                if auth: 
                    cpercent = ChildEval.objects.get(k=child, user=user).percent                    
                children += [{'c':child, 'percent':cpercent}]                       
            context['children'] = children
        return render (request,'courses/object.html', context)


fields = {
    'o': ['content', 'img', 'video'],
    'q': ['source','img', 'op1', 'op2', 'op3', 'op4', 'hint', 'video', 'level'], 
    'd': ['source','img', 'op1', 'op2', 'op3', 'op4', 'hint', 'video', 'level'], 
}

def Create(request, p):
    if request.method == 'POST':  
        name = request.POST.get('name')        
        b = p[0] 
        c = table[b][0]   
        Obj = table[c][2]       
        Eval = table[c][3]
        repeated = 0   
        if c != 'y': 
            Parent = table[b][2]    
            parent = Parent.objects.get(k=p)     
            if c !='q' and Obj.objects.filter(p=parent, name=name) : 
                repeated = 1
        elif Year.objects.filter(name=name): 
            repeated = 1   
        
        if not repeated:    
            if c == 'y': 
                object = Obj.objects.create(k=c, name=name)
            elif c =='s': 
                object = Obj.objects.create(k=c, name=name, p=parent)  
            elif c == 'u': 
                object = Obj.objects.create(k=c, name=name, p=parent, y=parent.p)
            elif c in ['o','l']: 
                object = Obj.objects.create(k=c, name=name, p=parent, y=parent.y)
            else: 
                object = Obj.objects.create(k=c, name=name, p=parent, l=parent.p, u=parent.p.p, s=parent.p.p.p)
            object.k += str(object.id)
            if c == 'y': 
                yname = object.name
            elif c in ['q','o','l','u','s']: 
                if c == 's': 
                    yname = object.p.name
                elif c == 'q':
                    yname = object.p.y.name  
                else:
                    yname = object.y.name   
                      
            for user in User.objects.filter(year=yname):                
                Eval.objects.create(k=object, user=user)      
            if not Eval.objects.filter(k=object, user=User.objects.get(email='biifounder@gmail.com')):
                Eval.objects.create(k=object, user=User.objects.get(email='biifounder@gmail.com'))                
            if c in  ['o','q']:
                childfields = fields[c]
                for field in childfields: 
                    setattr(object, field, request.POST.get(field))
            object.save()             
            return redirect('open', p)
        else: 
            return HttpResponse("هذا العنوان موجود بالفعل اضغط سهم العودة للتغيير") 
    else: 
        b = p[0]  
        c = table[b][0]
        context = {'teacher':is_teacher(request), 'p':p, 'child':c, 'cara':table[c][4]}     
    return render (request,'courses/create_update.html', context)


def Dublicate(request, k):
    question = Question.objects.get(k=k) 
    if request.method == 'POST':
        # QDubl.objects.create(k='d', p=question, name=question.name, source=question.source, img=question.img, hint=question.hint, video=question.video, 
        #     op1=question.op1, op2=question.op2, op3=question.op3, op4=question.op4, level=question.level)
        # dubl = QDubl.objects.get(k='d')
        # dubl.k += str(dubl.id)
        # dubl.save()      
        if request.POST.get('name') : 
            name = request.POST.get('name')
        dubl = QDubl.objects.create(k='d', name=name, p=question)
        dubl.k += str(dubl.id)
        obfields = fields['d'] 
        for field in obfields: 
            inp = request.POST.get(field) 
            if inp == '.' :
                setattr(dubl, field, '') 
            elif inp:
                setattr(dubl, field, inp)
        dubl.save()
        return redirect('open', dubl.p.p.k)
    else:                
        context = {'teacher':is_teacher(request), 'child':k[0], 'object': question}
    return render(request, 'courses/create_update.html', context)


def Update(request, k):    
    b = k[0]
    object = table[b][2].objects.get(k=k) 
    if request.method == 'POST':        
        p = k  
        if b == 'q': 
            p = object.p.k
        elif b == 'd': 
            p = object.p.p.k
        if request.POST.get('name') : 
            object.name = request.POST.get('name')
        if b in ['d','q','o']:             
            obfields = fields[b] 
            for field in obfields: 
                if request.POST.get(field) :  
                    setattr(object, field, request.POST.get(field))
        object.save()
        return redirect('open', p)
    context = {'teacher':is_teacher(request), 'child':b, 'object': object}
    return render(request, 'courses/create_update.html', context)

def Delete(request, k):      
    if request.method == 'POST':  
        b = k[0]
        object = table[b][2].objects.get(k=k)     
        p = object.p.k   
        if b == 'd': 
            p = object.p.p.k
        if b == 'q': 
            for dubl in QDubl.objects.filter(p=object):
                dubl.delete()
        object.delete()
        return redirect('open', p)
    return render(request, 'courses/delete.html')

#_________________________________________________________________________________________


def gatherQuestions(k): 
    b = k[0]
    object = table[b][2].objects.get(k=k)
    if b == 'o': 
        questions = [q for q in Question.objects.filter(p=object)]
    elif b == 'l': 
        questions = [q for q in Question.objects.filter(l=object)]
    elif b == 'u': 
        questions = [q for q in Question.objects.filter(u=object)]
    elif b == 's': 
        questions = [q for q in Question.objects.filter(s=object)]
    return questions

def MakeQuestions(request, k, nqs): 
    questions = gatherQuestions(k)   
    auth = request.user.is_authenticated
    if auth:    
        user = request.user        
        shuffle(questions)    
        mcqL, shqL = [],[]      
        for q in questions:  
            eval = QEval.objects.get(k=q, user=user)    
            ds = [q]+ [d for d in QDubl.objects.filter(p=q)]
            shuffle(ds)
            mcqL += [[[d for d in ds if d.op2][0], eval]]
            shqL += [[[d for d in ds if (not d.op2)][0], eval]]
        
        if not nqs:             
            mcqs, shqs = [],[] 
            for f in [1,0]: 
                for l in ['1','2']: 
                    mcqs += [L[0] for L in mcqL if L[1].score==-1 and L[1].flag==f and L[0].level==l]
                    shqs += [L[0] for L in shqL if L[1].score==-1 and L[1].flag==f and L[0].level==l]
            for f in [1,0]: 
                for s in [0,1]:
                    for l in ['1','2']: 
                        mcqs += [L[0] for L in mcqL if L[1].flag==f and L[1].score==s and L[0].level==l]
                        shqs += [L[0] for L in shqL if L[1].flag==f and L[1].score==s and L[0].level==l]
            questions = mcqs[:int(0.66*len(mcqs)+1)]+shqs[int(0.66*len(shqs)):] 
        else :             
            mcqs, shqs = [], []
            for s in (0,-1,1):
                for l in ('1','2'):
                    mcqs += [L[0] for L in mcqL if L[1].score==s and L[0].level==l]
                    shqs += [L[0] for L in shqL if L[1].score==s and L[0].level==l]
            questions = mcqs[:nqs]+shqs[nqs:]      
        shuffle(questions)
    else: 
        questions = questions[:3]

    JQuestions = []
    number = 1
    for q in questions:
        if 'd' in q.k: 
            d = q.p
        else: 
            d=q
        flag, score = 0,0 
        if auth: 
            Eval = QEval.objects.get(k=d, user=user) 
            flag, score = Eval.flag, Eval.score           
        d = {'k':d.k, 'question':q.name, 'img':'', 'hint':q.hint, 'video':'',
                'choice':'', 'delay':0, 'flagged':'', 
                'flag':flag, 'score':score} 
        if q.img: 
            d['img'] = q.img.url
        if q.video: 
            d['video'] = q.video
        number += 1
        if q.op2:
            options = [q.op1, q.op2]
            if q.op3: options+=[q.op3]
            if q.op4: options += [q.op4]
            shuffle(options)
            d['correct'] = q.op1 
            d['options'] = options                            
        else: 
            d['answer'] = q.op1
            d['correct'] = '1' 
            d['options'] = ['1','0']
        JQuestions += [d]    
    return dumps(JQuestions)
 
def updateScores(request): 
    user = request.user
    submitted = request.POST.get('submitted')
    submitted = submitted.split(',')
    for j in range(0, len(submitted)-1, 3): 
        q = Question.objects.get(k=submitted[j])
        newEval = QEval.objects.get(k=q, user=user)         
        newEval.score = int(submitted[j+1])
        newEval.flag = int(submitted[j+2])
        newEval.save()
    return submitted[-1]


def Practice(request, k):    
    if request.POST: 
        if request.user.is_authenticated:  
            updateScores(request)             
        return redirect('open', k)
    else: 
        outcome = Outcome.objects.get(k=k)
        questions = MakeQuestions(request, k, 0)    
        context = {'object':outcome, 'k':k, 'questions':questions, 'purpose':'pract', 'auth':request.user.is_authenticated}    
    return render (request,'courses/practice.html', context)



def foundationLevel(user,k): 
    questions = gatherQuestions(k)
    corrects, foundations = 0, 0
    for q in questions : 
        if q.level == '1' : 
            foundations += 1 
        if QEval.objects.get(k=q, user=user).score == 1:
            corrects += 1
    if corrects <= foundations:
        return True
    return False  


def objectAttrs(request, k):
    user = request.user
    b = k[0]
    object = table[b][2].objects.get(k=k)  
    objectEval = False
    if b != 'y': 
        objectEval = table[b][3].objects.get(k=k, user=user)   
    return b, user, object, objectEval

dnqs = {'s':2, 'u':2, 'l':2, 'o':2}
def updatePercent(user,k):     
    def calcPercent(user, k) :   
        b = k[0]   
        [Obj, Modeval] = table[b][2:4] 
        object = Obj.objects.get(k=k)
        Eval = Modeval.objects.get(k=object, user=user)      
        score, total, percent = Eval.score, Eval.total, 0   
        if total > 0 and score > 0:      
            percent = 100*round(score/total,2)
        if b in ['s','u','l']: 
            c = table[b][0]
            [midObj, midEval] = table[c][2:4]   
            midevals = [midEval.objects.get(k=m, user=user) for m in midObj.objects.filter(p=object)] 
            midpercents = [meval.percent for meval in midevals]
            midpercent = 0 
            if midpercents:                 
                midpercent = sum(midpercents)/len(midpercents)
            percent = 0.4*midpercent+0.6*percent
        if int(total/dnqs[b])  == 1 : 
            percent = min(percent, 85)
        if foundationLevel(user,k):
            percent = min(percent, 50) 
        Eval.percent = int(round(percent))
        Eval.save()
        return object.p.k 
    while k[0] in ['o','l','u','s'] :   
        k = calcPercent(user, k) 
    if k[0] == 'y': 
        year = Year.objects.get(k=k)
        Eval = YearEval.objects.get(k=year, user=user) 
        subpercents = [SubjectEval.objects.get(k=s, user=user).percent for s in Subject.objects.filter(p=year)]
        subEval = 0 
        if subpercents :
            subEval = sum(subpercents)/len(subpercents)
        Eval.percent = int(round(subEval)) 
        Eval.save()


def Assessment(request, k):      
    user = request.user
    b = k[0]
    object = table[b][2].objects.get(k=k)  
    objectEval = table[b][3].objects.get(k=object, user=user)    
    if request.POST:  
        totalscore = updateScores(request)         
        objectEval.score += int(totalscore)  
        objectEval.save()
        updatePercent(user,k)
        return redirect('open', k) 
    else:        
        nqs = 2
        objectEval.total += nqs 
        objectEval.save()        
        updatePercent(user,k)                         
        questions = MakeQuestions(request, k, nqs)          
        context = {'object':object, 'k':k, 'questions':questions, 'purpose':'test'}            
    return render (request,'courses/practice.html', context)

























#=======================================================================================================

# def deleteAll():
#     for Mod in [YearEval, SubjectEval, UnitEval, LessonEval, OutcomeEval, QEval] : 
#         Mod.objects.all().delete()
#     for Mod in [Year, Subject, Unit, Lesson, Outcome, Question, QDubl] : 
#         Mod.objects.all().delete()

# def zeroEvals(ModEval): 
#     for Eval in ModEval.objects.all():
#         Eval.score = 0
#         Eval.flag = 0
#         Eval.total = 0
#         Eval.percdnt = 0        
#         Eval.save()

# from pandas to Model
    # import pandas as pd    
    # School.objects.all().delete()
    # df = pd.read_csv('schools.csv')
    # for index, row in df.iterrows():
    #     print(row['school'], row['province'], row['governorate'])
    #     School.objects.create(school=row['school'], prov=row['province'], gov=row['governorate'])
        # print(row)
    # for s in School.objects.filter(prov='البريمي'): 
    #     print(s.school)

# def weeklyReport() 
    # for user in User.objects.all(): 
        # email_subject = 'التقرير الأسبوعي من المؤسس التفاعلي'
        # message = ''
        # for subject in user.subjects.all() : 
        #     percent = str(SubjectEval.objects.get(k=subject.k, user=request.user).percent)
        #     message += 'Yout score in ' + subject.name + ' is ' + percent + '%'
        # EmailSender(email_subject, message, [user.email])


# for subject in Subject.objects.all(): 
#     for user in subject.users.all(): 
#         user.subjects.add(subject)
#     print(subject.k,subject.users.all())

# for user in User.objects.all(): 
#     print(user.subjects.all())