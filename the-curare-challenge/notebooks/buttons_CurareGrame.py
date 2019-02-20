import ipywidgets as widgets
import csv
# . - . . - .     . - . . - . . - .     . - .     . - .     . - .     . - .     . - .     . - .     . - .         
# Button creation functions:   define_question buttons: simple, drop_down 
# . - . . - .     . - . . - . . - .     . - .     . - .     . - .     . - .     . - .     . - .     . - .
def define_question(options, description, button_type):
    if button_type == 'Radio':
        q = widgets.RadioButtons(options = options, value = None, description = description, disabled=True)
    else: 
         if button_type == 'Dropdown':
              q = widgets.Dropdown(options=options, value=None,description=description,disabled=True,)
    return q

def drop_down_question(drop_options, description, collectionsNames):

    children = [widgets.Dropdown(options=name, description='',value=None) for name in drop_options]
    tab = widgets.Tab()
    tab.children = children
    items= collectionsNames
    for i in range(len(items)):
        tab.set_title(i, items[i])
    q = tab    
    return q

# . - . . - .     . - . . - . . - .     . - .     . - .     . - .     . - .     . - .     . - .     . - .         
# Timer function    timer(btn,lbl,q) 
# btn - receive a button object
# lbl - receive a label object
#    we use lbl.value to get timer value
# q - receive a multiple option object
#    we use q.value to get answered value

# . - . . - .     . - . . - . . - .     . - .     . - .     . - .     . - .     . - .     . - .     . - .     
import time, threading

def timer(btn,lbl,q):        

    cnt =int(lbl.value)   
    on=btn.value 
    desc=q.description

    if desc!='Submitted':
        if on==True:      
            threading.Timer(1, timer, [btn,lbl,q]).start()
            cnt = cnt+1                        
            lbl.value = str(cnt)
            btn.description='Submit answer'
            q.disabled=False

        elif on==False:
            threading.Timer(1, timer, [btn,lbl,q]).start()
            btn.description='Activate'
            q.disabled=True

        else:
            None

    if cnt!=0 and btn.description=='Activate':
        threading.Timer(1, timer, [btn,lbl,q]).start()
        q.description='Submitted'
        btn.visibility='hidden'
        btn.description='--'
        btn.disbled=True  

        
# . - . . - .     . - . . - . . - .     . - .     . - .     . - .     . - .     . - .     . - .     . - .         
# Timer function    timerTab(btn,lbl,q) 
# . - . . - .     . - . . - . . - .     . - .     . - .     . - .     . - .     . - .     . - .     . - .
def timerTab(btn,lbl,q):        

    cnt=int(lbl.value)   
    on=btn.value 
    desc=q.children[0].description

    if desc!='Submitted':
        if on==True:      
            threading.Timer(1, timerTab, [btn,lbl,q]).start()
            cnt = cnt+1                        
            lbl.value = str(cnt)
            btn.description='Submit answer'
            for i in range(len(q.children)):
                q.children[i].disabled=False

        elif on==False:
            threading.Timer(1, timerTab, [btn,lbl,q]).start()
            btn.description='Activate'
            for i in range(len(q.children)):
                q.children[i].disabled=True

        else:
            None

    if cnt!=0 and btn.description=='Activate':
        threading.Timer(1, timerTab, [btn,lbl,q]).start()
        for i in range(len(q.children)):
            q.children[i].description='Submitted'
        btn.visibility='hidden'
        btn.description='--'
        btn.disbled=True  
        
#. - . . - .     . - . . - . . - .     . - .     . - .     . - .     . - .     . - .     . - .     . - .         
# Log Effort and Response Time
# . - . . - .     . - . . - . . - .     . - .     . - .     . - .     . - .     . - .     . - .     . - .

def collect_QuestionEffort():
    effortW = []
    for e in range(7):
        effortW.append(widgets.ToggleButtons(options=['Low', 'Regular', 'High'],
                                             description='Select Effort:',disabled=False,value=None)) 
    return effortW


def collect_ResponseTime():
    timeLblW = []
    for t in range(7):
        timeLblW.append(widgets.Text(value='0',description='',disabled=True))
    return timeLblW 


#. - . . - .     . - . . - . . - .     . - .     . - .     . - .     . - .     . - .     . - .     . - .         
# Log Effort and Response Time
# . - . . - .     . - . . - . . - .     . - .     . - .     . - .     . - .     . - .     . - .     . - .



def collect_UserEffort_answers(effortW):
    
    userEffortL = []
    for e in effortW:
        userEffortL.append(e.value) 
    return userEffortL
        
# collect time from answers
def collect_TimeResponse_answers(timeLblW):
    qtimeL=[]
    for t in timeLblW:
        qtimeL.append(int(t.value))
    return  qtimeL  

# tuple for answers
def collect_Questions_answers(q1, q2, q3, q4, q5, q7):
    qans1=q1.options[2]
    qans2=q2.options[0]
    qans4=q4.options[1]
    qans3=q3.options[3]
    qans5=[q5.children[0].options[3],q5.children[1].options[0],q5.children[2].options[5],q5.children[3].options[5],q5.children[4].options[0]]
    qans7=[q7.children[0].options[3],q7.children[1].options[0],q7.children[2].options[5],q7.children[3].options[5],q7.children[4].options[0]]
    qans = [qans1,qans2,qans3,qans4,qans5,qans7]
    return qans

def compute_Score(q1, q2, q3, q4, q5, q7, qans):
    scoreL = [0.0]*7

    if q1.value == qans[0]: scoreL[0]=1 
    if q2.value == qans[1]: scoreL[1]=1 
    if q4.value == qans[3]: scoreL[3]=1 
    if q3.value == qans[2]: scoreL[2]=1 

    if qans[4][0] == q5.children[0].value: scoreL[4]=scoreL[4] + 0.2
    if qans[4][1] == q5.children[1].value: scoreL[4]=scoreL[4] + 0.2
    if qans[4][2] == q5.children[2].value: scoreL[4]=scoreL[4] + 0.2
    if qans[4][3] == q5.children[3].value: scoreL[4]=scoreL[4] + 0.2
    if qans[4][4] == q5.children[4].value: scoreL[4]=scoreL[4] + 0.2

    #if q6.value ==qans6: scoreL[5]=1

    if qans[5][0] == q7.children[0].value: scoreL[5]=scoreL[5] + 0.2
    if qans[5][1] == q7.children[1].value: scoreL[5]=scoreL[5] + 0.2
    if qans[5][2] == q7.children[2].value: scoreL[5]=scoreL[5] + 0.2
    if qans[5][3] == q7.children[3].value: scoreL[5]=scoreL[5] + 0.2
    if qans[5][4] == q7.children[4].value: scoreL[5]=scoreL[5] + 0.2

    return scoreL

def estimate_Effort(scoreL, qtimeL):
    calcEffortL = []
    maxcEffort = 100
    for i in range(0,len(scoreL)):
        if scoreL[i] == 0: 
            calcEffortL.append(maxcEffort)
        else:
            if int(qtimeL[i]) > 300: qtimeL[i] = 300 # 5 min limit
            tmp=int(qtimeL[i])/scoreL[i]
            calcEffortL.append((tmp*100)/1800)   
    return calcEffortL

def store_Game_Results(scoreL,qtimeL,userEffortL,calcEffortL,elapsed):
    # qid | time | score | user_effort | calculated_effort | execution_time (cpu)
    header=['qid', 'score', 'time', 'user_effort', 'calculated_effort', 'execution_time'] 
    qid=list(range(1,8))
    elapsedL = [elapsed]*7

    rows = zip(qid,scoreL,qtimeL,userEffortL,calcEffortL,elapsedL)

    with open("../results/match1.csv", mode="w") as f:
        #writer = csv.writer(f, delimiter=',', quotechar='"', quoting=csv.QUOTE_MINIMAL)
        writer = csv.writer(f, delimiter=',')
        writer.writerow(header)
        for row in rows:
            writer.writerow(row)
            