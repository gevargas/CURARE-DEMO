import pandas as pd
import dash
import dash_core_components as dcc
import dash_html_components as html
from dash.dependencies import Input, Output, State

import datetime
import json
import timeit
import csv


#-------------------------------------------------------------------------------------------------------------------------------#
#                                                    Global variables 
#
#-------------------------------------------------------------------------------------------------------------------------------


effortW = []
timeLblW = []
q_answers = []
elapsed_time = 0

start_time = timeit.default_timer()
execution_time = timeit.default_timer() - start_time

#-------------------------------------------------------------------------------------------------------------------------------#
#                                                    Layout and tables schema constants 
#
#-------------------------------------------------------------------------------------------------------------------------------


external_stylesheets = ['https://codepen.io/chriddyp/pen/bWLwgP.css']

colors = {
    'background': '#111111',
    'text': '#171c42'
}

tabs_styles = {
    'height': '44px'
}
tab_style = {
    'borderBottom': '1px solid #d6d6d6',
    'padding': '6px',
    'fontWeight': 'bold'
}

tab_selected_style = {
    'borderTop': '1px solid #d6d6d6',
    'borderBottom': '1px solid #d6d6d6',
    'backgroundColor': '#119DFF',
    'color': 'white',
    'padding': '6px'
}

posts_attributes = [
                {'label':'Id', 'value':'Id'},
                {'label':'PostTypeId', 'value':'PostTypeId'},
                {'label': 'AcceptedAnswerId', 'value': 'AcceptedAnswerId'},
                {'label':'ParentId', 'value':'ParentId'},
                {'label':'CreationDate', 'value': 'CreationDate'},  
                {'label':'DeletionDate', 'value': 'DeletionDate'},
                {'label':'Score', 'value': 'Score'},
                {'label': 'ViewCount', 'value':'ViewCount'},
                {'label': 'Body', 'value':'Body'},
                {'label':   'OwnerUserId', 'value':'OwnerUserId'},
                {'label':'OwnerDisplayName', 'value': 'OwnerDisplayName'},            
                {'label':'LastEditorUserId', 'value':'LastEditorUserId'},
                {'label':'LastEditorDisplayName', 'value':'LastEditorDisplayName'},
                {'label':'LastEditDate', 'value': 'LastEditDate'},
                {'label':'LastActivityDate', 'value':'LastActivityDate'},
                {'label':'Title', 'value': 'Title'},
                {'label': 'Tags', 'value': 'Tags'},
                {'label':'AnswerCount', 'value':'AnswerCount'},
                {'label':'CommentCount', 'value':'CommentCount'},
                {'label':'FavoriteCount', 'value':'FavoriteCount'},
                {'label':'ClosedDate', 'value': 'ClosedDate'},                 
                {'label':'CommunityOwnedDate', 'value':'CommunityOwnedDate'}
             ]

badges_attributes = [
                {'label': '--', 'value': '--'},
                {'label': 'Id', 'value': 'Id'}, 
                {'label':'UserId', 'value': 'UserId'},
                {'label':'Name', 'value': 'Name'},
                {'label':'Date', 'value': 'Date'},
                {'label':'Class', 'value': 'Class'},
                {'label':'TagBased', 'value': 'TagBased'}
]

comments_attributes = [
            {'label':'--', 'value': '--'},
            {'label':'Id', 'value':'Id'},
            {'label':'PostId', 'value': 'PostId'},
            {'label':'Score', 'value': 'Score'},
            {'label':'Text', 'value': 'Text'},
            {'label':'CreationDate', 'value': 'CreationDate'},
            {'label':'UserDisplayName', 'value': 'UserDisplayName'},
            {'label':'UserId', 'value': 'UserId'}
]


users_attributes = [
        {'label':'--', 'value':'--'},
        {'label':'Id', 'value': 'Id'},
        {'label':'Reputation', 'value': 'Reputation'},
        {'label':'CreationDate', 'value':'CreationDate'},
        {'label':'DisplayName', 'value': 'DisplayName'},
        {'label':'LastAccessDate', 'value': 'LastAccessDate'},
        {'label':'WebsiteUrl','value': 'WebsiteUrl'},
        {'label':'Location', 'value': 'Location'},
        {'label':'AboutMe', 'value': 'AboutMe'},
        {'label':'Views', 'value':'Views'},
        {'label':'UpVotes', 'value':'UpVotes'},
        {'label':'DownVotes', 'value':'DownVotes'},
        {'label':'ProfileImageUrl', 'value':'ProfileImageUrl'},
        {'label':'EmailHash', 'value': 'EmailHash'},
        {'label':'AccountId','value': 'AccountId'}
]

votes_attributes = [
        {'label':'--', 'value': '--'},
        {'label':'Id', 'value': 'Id'},
        {'label':'PostId', 'value': 'PostId'},
        {'label':'VoteTypeId', 'value': 'VoteTypeId'},
        {'label':'UserId', 'value': 'UserId'},
        {'label':'CreationDate', 'value': 'CreationDate'},
        {'label':'BountyAmount', 'value': 'BountyAmount'},
         ]


q_releases_options = [
                        {'label': 'January 1rst 2018', 'value': 'R1'},
                        {'label': 'January 2nd 2018', 'value': 'R2'},
                        {'label': 'January 3rd 2018', 'value': 'R3'}
                    ]


#-------------------------------------------------------------------------------------------------------------------------------#
#                                        General chronometer, questions & effort functions 
#
#-------------------------------------------------------------------------------------------------------------------------------

#. -  . -. -  . -. -  . -. -  . -. -  . -. -  . -. -  . -. -  . -. -  . -. -  . -. -  . -. -  . -
# define_question(question):  returns a textual layout with the text given in question
#
#. -  . -. -  . -. -  . -. -  . -. -  . -. -  . -. -  . -. -  . -. -  . -. -  . -. -  . -. -  . -

def define_question(question):
    return html.Div([html.H4(children= question, 
                         style={
                        'textAlign': 'center',
                        'color': colors['text'],
                        'fontFamily': 'Helvetica'
                        })
                    ], style={'columnCount': 1, 'marginBottom': 25, 'marginTop': 30, 'marginLeft': 65}
                   )

#. -  . -. -  . -. -  . -. -  . -. -  . -. -  . -. -  . -. -  . -. -  . -. -  . -. -  . -. -  . -
# chronometre(id1, id2, q): creates two buttons labeled id1 and id2 for a question 1 
#                           returns the buttons layout START and STOP labeled id1-q, id2-q
#
#. -  . -. -  . -. -  . -. -  . -. -  . -. -  . -. -  . -. -  . -. -  . -. -  . -. -  . -. -  . -

def chronometre(id1, id2, q):
    
    button_id1 = 'btn-' + str(id1) + '-q' + str(q)
    button_id2 = 'btn-' + str(id2) + '-q' + str(q)
    
    return html.Div([
                        html.Button('Start', id=button_id1, n_clicks_timestamp='0'),
                        html.Button('Stop',  id=button_id2, n_clicks_timestamp='0'),
                        html.Div(id= ('container-button-timestamp-' + str(q)) ),
                        ], style={'columnCount': 1, 'marginBottom': 25, 'marginTop': 30, 'marginLeft': 65})



#. -  . -. -  . -. -  . -. -  . -. -  . -. -  . -. -  . -. -  . -. -  . -. -  . -. -  . -. -  . -
# define_radioMultipleOptions(inputId, outputId, radio_options): 
#
# creates a radio component labeled by inputId containing a set of options labeled by the elements in 
# radio_options whose output will be labeled by outputId
#
#. -  . -. -  . -. -  . -. -  . -. -  . -. -  . -. -  . -. -  . -. -  . -. -  . -. -  . -. -  . -

def define_radioMultipleOptions(inputId, outputId, radio_options):
    return html.Div([html.Div([dcc.RadioItems( id = inputId,
                                                options= radio_options,
                                                value=''
                                              )
                               ], style={'color': 'black', 'fontSize': 15, 'fontFamily': 'Helvetica'}),
                     html.Div(id= outputId )
                    ], style={'columnCount': 1, 'marginBottom': 25, 'marginTop': 25, 'marginLeft': 65}
                   )

#. -  . -. -  . -. -  . -. -  . -. -  . -. -  . -. -  . -. -  . -. -  . -. -  . -. -  . -. -  . -
# define_tabMultipleOptions(objectId, dropdown_options, q): 
#
# creates a Tab labeled by  objectId containing a set of tabs labeled by the elements of dropdown_options (constant) 
# for a question identified by q
#
#. -  . -. -  . -. -  . -. -  . -. -  . -. -  . -. -  . -. -  . -. -  . -. -  . -. -  . -. -  . -


def define_tabMultipleOptions(objectId, dropdown_options, q):
    children_tabs = [dcc.Tab( label =name, 
                             value = ('tab-' + name + '-q-' + str(q)), 
                             style=tab_style, selected_style=tab_selected_style) for name in dropdown_options]
    return html.Div([
                        html.Div([
                                    dcc.Tabs(id= objectId, value='tabs-' + str(q), children= children_tabs, style=tabs_styles)
                                 ]),
                        html.Div(id= 'tabs-content-' + str(q) )
                        
                     ], style={'columnCount': 1, 'color': 'black', 'marginLeft': 65, 'marginRight':500, 'marginBottom': 25}
                    )

#. -  . -. -  . -. -  . -. -  . -. -  . -. -  . -. -  . -. -  . -. -  . -. -  . -. -  . -. -  . -
# define_dropdownMultipleOptions(objectId, dropdown_options, q, multi_option): 
#
# creates a dropdown multiple options component labeled by objectId containing a set of options 
# labeled by the elements of dropdown_options (constant) 
# for a question identified by q where the choice can be mutliple (multi_option = true)
#
#. -  . -. -  . -. -  . -. -  . -. -  . -. -  . -. -  . -. -  . -. -  . -. -  . -. -  . -. -  . -

def define_dropdownMultipleOptions(objectId, dropdown_options, q, multi_option):
    return html.Div([
                     html.Div([dcc.Dropdown(
                                    id= objectId,
                                    options= dropdown_options,
                                    value='',
                                    multi = multi_option
                                    )
                              ], style={'color': 'black', 'fontSize': 12, 'fontFamily': 'Helvetica'}
                             ),
                    html.Div(id= ('output-container-'+ str(q)))
                   ], style={'columnCount': 1, 'color': 'black', 'marginLeft': 65, 'marginRight':500, 'marginBottom': 25}
                    )


#. -  . -. -  . -. -  . -. -  . -. -  . -. -  . -. -  . -. -  . -. -  . -. -  . -. -  . -. -  . -
# match_EvaluateEffort(q) creates a slider for estimating the effort labeled by q 
#
# q is the id of the question associated to the effort slider
#. -  . -. -  . -. -  . -. -  . -. -  . -. -  . -. -  . -. -  . -. -  . -. -  . -. -  . -. -  . -

def match_EvaluateEffort(q):
    print("Slider", q)
    return html.Div([

            html.H4(children='Evaluate Effort', 
                             style={
                            #'textAlign': 'center',
                            'color': colors['text'],
                            'fontFamily': 'Helvetica',
                           # 'marginLeft': 65,
                            'marginRight':80,
                            }),

                   dcc.Slider(id = ('slider-input-container-'+ str(q)),
                            min=0,
                            max=4,
                            marks={
                                0:  {'label': 'None', 'style': {'color': '#111111', 'fontSize': 15, 'fontFamily':'Helvetica'}},
                                1: {'label': 'Low', 'style': {'color': '#111111', 'fontSize': 15, 'fontFamily':'Helvetica'}},
                                2: {'label': 'Regular', 'style': {'color': '#111111', 'fontSize': 15, 'fontFamily':'Helvetica'}},
                                3: {'label': 'High', 'style': {'color': '#f50', 'fontSize': 15, 'fontFamily':'Helvetica'}}
                            },
                            step=1,
                            value=0,
                            #updatemode = 'mouseup',
                            dots = True,
                ),
        
                html.Div(id= ('slider-output-container-'+ str(q)))
               ], style={'columnCount': 1, 'color': 'black', 'marginLeft': 65, 'marginRight':500, 'marginBottom': 25})


# ********************************************************************************************************************
#                                       Manipulating time, question answers & effort 
#                                                     in a Match
# ********************************************************************************************************************

#. -  . -. -  . -. -  . -. -  . -. -  . -. -  . -. -  . -. -  . -. -  . -. -  . -. -  . -. -  . -
# update_list(key, value): given a key and a value, search key in global variable q_answers
# to define a new answer (value)  to the list of answer given to a given question (key)
#
# q_answers[['q1', [v11, v12]], ... ['qn', [vn1]] 
#  given key = qn & value = vn2 --> q_answers[['q1', [v11, v12]], ... ['qn', [vn1, vn2]] 
# 
#. -  . -. -  . -. -  . -. -  . -. -  . -. -  . -. -  . -. -  . -. -  . -. -  . -. -  . -. -  . -

def update_list(key, value):
    for i in range(len(q_answers)):
        if q_answers[i][0] == key:
               q_answers[1].append(value)
        else: q_answers.append([key, [value]])       
    return q_answers


#. -  . -. -  . -. -  . -. -  . -. -  . -. -  . -. -  . -. -  . -. -  . -. -  . -. -  . -. -  . -
# define_Questions_answers(): defines the "correct" answers for every question of the Match
#. -  . -. -  . -. -  . -. -  . -. -  . -. -  . -. -  . -. -  . -. -  . -. -  . -. -  . -. -  . -

def define_Questions_answers():
    qans1=['R3']
    qans2=['R1']
    qans4=['R2']
    qans3= ['Score', 'FavoriteCount', 'ViewCount']
    qans5= [['q51', ['Id', 'Name']], 
            ['q52', ['PostId', 'Score']], 
            ['q53', ['Id', 'Score', 'Tags']], 
            ['q54', []], 
            ['q55', []]]
    qans6= [['q61', ['Name']], 
            ['q62', ['Id']], 
            ['q63', ['Id']], 
            ['q64', ['Id', 'DisplayName']], 
            ['q65', ['Id', 'PostId']]]
    qans = [qans1,qans2,qans3,qans4,qans5,qans6]
    return qans

#. -  . -. -  . -. -  . -. -  . -. -  . -. -  . -. -  . -. -  . -. -  . -. -  . -. -  . -. -  . -
# lookup_queryAnswer(q_answers, question): returns the answer given to a question contained 
#                                          in the answers list of the match in global variable q_answers
# 
#. -  . -. -  . -. -  . -. -  . -. -  . -. -  . -. -  . -. -  . -. -  . -. -  . -. -  . -. -  . -


def lookup_queryAnswer(q_answers, question):
    answer = ''
    if len(q_answers) == 0: 
        return answer
    else:
        for i in range(len(q_answers)):
            if q_answers[i][0] == question:               
                answer = q_answers[i][1]
                return answer
            else: i = i+1
        if i == len(q_answers):
            return answer

#. -  . -. -  . -. -  . -. -  . -. -  . -. -  . -. -  . -. -  . -. -  . -. -  . -. -  . -. -  . -
# add_queryEffort(q, value, effort): given a question id (q), value (0 - 3), and effort (low, regular, effort)
#                                    update global variable effortW adding or updating the effort associated to
#                                    answer q
#
# Given effortW = [['q1', 2, 'Regular'],  ['q2', 2, 'Regular'],  ['q3', 3, 'High'],  
#                  ['q4', 2, 'Regular'], ['q5', 3, 'High'],  ['q6', 3, 'High']]

#       add_queryEffort('q1', 2, 'High')
#
# OUTPUT
#   effortW = [['q1', 2, 'High'], ['q2', 2, 'Regular'], ['q3', 3, 'High'], ['q4', 2, 'Regular'], 
#              ['q5', 3, 'High'], ['q6', 3, 'High']]
#. -  . -. -  . -. -  . -. -  . -. -  . -. -  . -. -  . -. -  . -. -  . -. -  . -. -  . -. -  . -


def add_queryEffort(q, value, effort):
    answer = ''
    i = 0
    print("Initial effort list", effortW)
    if len(effortW) == 0: 
         effortW.append([q, value, effort])
         return answer 
    else:
        for i in range(0, len(effortW)):
            if effortW[i][0] == q:   
                print("found", effortW[i][0], q)
                effortW[i][1] = value
                effortW[i][2] = effort
                answer = "found"
                print("New effort list", effortW)
                return answer
            
    if answer == '':
        print("not found")
        effortW.append([q, value, effort])
        print("New effort list", effortW)
        return answer

#. -  . -. -  . -. -  . -. -  . -. -  . -. -  . -. -  . -. -  . -. -  . -. -  . -. -  . -. -  . -
# L1_similar_L2(L1, L2): estimate the degree of similarity between to lists L1 and L2
# 
# OUTPUT: similarity
#. -  . -. -  . -. -  . -. -  . -. -  . -. -  . -. -  . -. -  . -. -  . -. -  . -. -  . -. -  . -


def L1_similar_L2(L1, L2):
    similarity = 0
    if len(L2) == 0: return similarity
    else: 
          if len(L1) == 0: return similarity
          else: 
                for i in range(0,len(L1)):
                    for j in range(0,len(L2)):
                        print(L1[i],  L2[j])
                        if  unicode(L1[i], "utf-8")  in L2[j] : 
                            similarity = similarity + 1
                            print(L1[i],  L2[j], similarity)
                        else: 
                            similarity = similarity
    if len(L2) > len(L1): similarity = (float(similarity) / len(L2)) 
    else: similarity = (float(similarity) / len(L1)) 
    return  similarity


#. -  . -. -  . -. -  . -. -  . -. -  . -. -  . -. -  . -. -  . -. -  . -. -  . -. -  . -. -  . -
# compute_Score( qans, q_answers) : compute final score (scoreL) comparing the collected answers with predefined ones
# INPUT
# qans:   list of answers collected during the match
# q_answers: predefined "correct" answers
#
# OUTPUT
# score L is a list where every element is the score of a question represented by its position in the list
#. -  . -. -  . -. -  . -. -  . -. -  . -. -  . -. -  . -. -  . -. -  . -. -  . -. -  . -. -  . -

def compute_Score(qans, q_answers):
    scoreL = [0.0]
    if len(qans) == 0 or len(q_answers) == 0: return scoreL
    else:
        scoreL = [0.0]*7
        if qans[0][0] == q_answers[0]: scoreL[0] = 1 
        if qans[1][0] == q_answers[1]: scoreL[1] = 1 

        givenAnswer_q3 = lookup_queryAnswer(q_answers, 'q3')
        scoreL[2]= (scoreL[3]* 0.2) + L1_similar_L2(qans[3][0], givenAnswer_q3)

        if qans[3][0] == q_answers[3]: scoreL[3] = 1 

        givenAnswer_q51 = lookup_queryAnswer(q_answers, 'q51')
        givenAnswer_q52 = lookup_queryAnswer(q_answers, 'q52')
        givenAnswer_q53 = lookup_queryAnswer(q_answers, 'q53')
        givenAnswer_q54 = lookup_queryAnswer(q_answers, 'q54')
        givenAnswer_q55 = lookup_queryAnswer(q_answers, 'q55')

        scoreL[4]= (scoreL[4]* 0.2) + L1_similar_L2(qans[4][0][1], givenAnswer_q51)
        scoreL[4]= (scoreL[4]* 0.2) + L1_similar_L2(qans[4][1][1], givenAnswer_q52)
        scoreL[4]= (scoreL[4]* 0.2) + L1_similar_L2(qans[4][2][1], givenAnswer_q53)
        scoreL[4]= (scoreL[4]* 0.2) + L1_similar_L2(qans[4][3][1], givenAnswer_q54)
        scoreL[4]= (scoreL[4]* 0.2) + L1_similar_L2(qans[4][4][1], givenAnswer_q55)

        givenAnswer_q61 = lookup_queryAnswer(q_answers, 'q61')
        givenAnswer_q62 = lookup_queryAnswer(q_answers, 'q62')
        givenAnswer_q63 = lookup_queryAnswer(q_answers, 'q63')
        givenAnswer_q64 = lookup_queryAnswer(q_answers, 'q64')
        givenAnswer_q65 = lookup_queryAnswer(q_answers, 'q65')

        scoreL[5]= (scoreL[5]* 0.2) + L1_similar_L2(qans[5][0][1], givenAnswer_q61)
        scoreL[5]= (scoreL[5]* 0.2) + L1_similar_L2(qans[5][1][1], givenAnswer_q62)
        scoreL[5]= (scoreL[5]* 0.2) + L1_similar_L2(qans[5][2][1], givenAnswer_q63)
        scoreL[5]= (scoreL[5]* 0.2) + L1_similar_L2(qans[5][3][1], givenAnswer_q64)
        scoreL[5]= (scoreL[5]* 0.2) + L1_similar_L2(qans[5][4][1], givenAnswer_q65)
        return scoreL


#. -  . -. -  . -. -  . -. -  . -. -  . -. -  . -. -  . -. -  . -. -  . -. -  . -. -  . -. -  . -
# estimate_Effort(scoreL, qtimeL) : estimate the effort combining the time spent to answer a question qtimeL
#                                   and the computed score
#
# INPUT
# scoreL:   list of scores for every question
# qtimeL:   list of time spent to answer each question
# where a question is represented by its position in the list
#
# OUTPUT
# calcEffortL: list of estimated effort for every question
#. -  . -. -  . -. -  . -. -  . -. -  . -. -  . -. -  . -. -  . -. -  . -. -  . -. -  . -. -  . -

def estimate_Effort(scoreL, qtimeL):
    calcEffortL = []
    if len(qtimeL) == 0: return calcEffortL
    else: 
        maxcEffort = 100
        for i in range(0,len(scoreL)):
            if scoreL[i] == 0: 
                calcEffortL.append(maxcEffort)
            else:
                if int(qtimeL[i][1]) > 300: qtimeL[i][1] = 300 # 5 min limit
                tmp=int(qtimeL[i][1])/scoreL[i]
                calcEffortL.append((tmp*100)/1800)   
        return calcEffortL

#. -  . -. -  . -. -  . -. -  . -. -  . -. -  . -. -  . -. -  . -. -  . -. -  . -. -  . -. -  . -
# get_questions_time(q_time_list): flatten the list of spent time per question
# [['q1', t1], ... ['qn', tn]] --> [t1, ... , tn]
#. -  . -. -  . -. -  . -. -  . -. -  . -. -  . -. -  . -. -  . -. -  . -. -  . -. -  . -. -  . -

def get_questions_time(q_time_list):
    questions_time = []
    for i in range(0, len(q_time_list)):
        questions_time.append(q_time_list[i][1])
    return questions_time

#. -  . -. -  . -. -  . -. -  . -. -  . -. -  . -. -  . -. -  . -. -  . -. -  . -. -  . -. -  . -
# get_questions_effort(q_effort_list): flatten the list of effort perceived by user for answering a question
# [['q1', v1, e1], ... ['qn', vn, en]] --> [e1, ... , en]
#. -  . -. -  . -. -  . -. -  . -. -  . -. -  . -. -  . -. -  . -. -  . -. -  . -. -  . -. -  . -


def get_questions_effort(q_effort_list):
    questions_effort = []
    for i in range(0, len(q_effort_list)):
        questions_effort.append(q_effort_list[i][2])
    return questions_effort


#. -  . -. -  . -. -  . -. -  . -. -  . -. -  . -. -  . -. -  . -. -  . -. -  . -. -  . -. -  . -
#  get_Results(effortW, timeLblW, q_answers): final results of the Match given the effort, time & 
#                                             answers lists collected for every question
#
#  OUTPUT
#  scoreL: score list 
#  calcEffortL: computed effort list 
#  questions_time: flattened list of collected times spent for every question
#  questions_effort: flattened list of collected effort perception for every question
#. -  . -. -  . -. -  . -. -  . -. -  . -. -  . -. -  . -. -  . -. -  . -. -  . -. -  . -. -  . -

def get_Results(effortW, timeLblW, q_answers):
    
    qans = define_Questions_answers()
    scoreL = compute_Score(qans, q_answers)
    questions_time = get_questions_time(timeLblW)
    questions_effort = get_questions_effort(effortW)
    calcEffortL= estimate_Effort(scoreL, timeLblW) 
   
    return (scoreL, calcEffortL, questions_time, questions_effort )
    
#. -  . -. -  . -. -  . -. -  . -. -  . -. -  . -. -  . -. -  . -. -  . -. -  . -. -  . -. -  . -
# Store results in an CSV at the end of the Match
#. -  . -. -  . -. -  . -. -  . -. -  . -. -  . -. -  . -. -  . -. -  . -. -  . -. -  . -. -  . -
def store_Game_Results(scoreL, qtimeL, userEffortL, calcEffortL, elapsed):
    # qid | time | score | user_effort | calculated_effort | execution_time (cpu)
    header=['qid', 'score', 'time', 'user_effort', 'calculated_effort', 'execution_time'] 
    qid=list(range(1,8))
    elapsedL = [elapsed]*7

    rows = zip(qid,scoreL,qtimeL,userEffortL,calcEffortL,elapsedL)

    with open("../results/temporal/match1.csv", mode="w") as f:
        writer = csv.writer(f, delimiter=',')
        writer.writerow(header)
        for row in rows:
            writer.writerow(row)
#-------------------------------------------------------------------------------------------------------------------------------#
#                                                          Main Layout 
#
#-------------------------------------------------------------------------------------------------------------------------------

app = dash.Dash(__name__, external_stylesheets=external_stylesheets)

app.config['suppress_callback_exceptions']=True

app.layout = html.Div([
    html.Div([
                html.H1(children='The CURARE Challenge', 
                        style={
                        'textAlign': 'center',
                        'color': colors['text'],
                        'fontFamily': 'Helvetica'
                        }),

                html.H2(children='Match 1: exploring raw Stack Overflow data collections', 
                         style={
                        'textAlign': 'center',
                        'color': colors['text'],
                        'fontFamily': 'Helvetica'
                        }),
                ]),
    html.Div([
                define_question('Q1. Which release has the most number of records?'),
                chronometre(1, 2, 1)           
             ], style={'columnCount': 2}),
                define_radioMultipleOptions('q1-choice-input', 'q1-choice-output', q_releases_options),
                match_EvaluateEffort(1),
    
    html.Div([
                define_question('Q2. Which is the release with best quality? (fewest null values)'),
                chronometre(1, 2, 2)           
             ], style={'columnCount': 2}),
                define_radioMultipleOptions('q2-choice-input', 'q2-choice-output', q_releases_options),
                match_EvaluateEffort(2),
    
     html.Div([
                define_question('Q3 Which is/are the attribute(s) in Posts useful to identify the most trendy topic addressed in a release?'),
                chronometre(1, 2, 3)           
             ], style={'columnCount': 2}),
                define_dropdownMultipleOptions('my-dropdown-3', posts_attributes, 3, 'True'),
                match_EvaluateEffort(3),
    
    html.Div([
                define_question('Q4. Which is the release where the attribute UpVote from Users is most evenly distributed?'),
                chronometre(1, 2, 4)           
             ], style={'columnCount': 2}),
                 define_radioMultipleOptions('q4-choice-input', 'q4-choice-output', q_releases_options),
                 match_EvaluateEffort(4),
    
    html.Div([
                define_question('Q5. Which is/are the attribute(s) useful to identify the most trendy topic addressed in the release?'),
                chronometre(1, 2, 5)           
             ], style={'columnCount': 2}),
                 
                 define_tabMultipleOptions('tabs-5', ['Badges', 'Comments', 'Posts', 'Users', 'Votes'], 5),
                 match_EvaluateEffort(5),
    
    html.Div([
                define_question('Q6. Which attributes  can be used as sharding keys to fragment releases using a hash based strategy'),
                chronometre(1, 2, 6)           
             ], style={'columnCount': 2}),
                define_tabMultipleOptions('tabs-6', ['Badges', 'Comments', 'Posts', 'Users', 'Votes'], 6),
                match_EvaluateEffort(6),
    html.Div([
    
                html.Div(id='container-button-basic',
                         children='Press submit to compute results'),
                html.Button('Submit', id='button'),
                
            ], style={'columnCount': 1, 'color': 'black', 'marginLeft': 65, 'marginRight':500, 'marginTop': 80, 'marginBottom': 25}),
   
])

#-------------------------------------------------------------------------------------------------------------------------------#
#                                                  Chronometers Call Backs 
#
#-------------------------------------------------------------------------------------------------------------------------------

#. -  . -. -  . -. -  . -. -  . -. -  . -. -  . -. -  . -. -  . -. -  . -. -  . -. -  . -. -  . -
# Chronometer callback Q1
#. -  . -. -  . -. -  . -. -  . -. -  . -. -  . -. -  . -. -  . -. -  . -. -  . -. -  . -. -  . -
@app.callback(Output('container-button-timestamp-1', 'children'),
             [Input('btn-1-q1', 'n_clicks_timestamp'),
              Input('btn-2-q1', 'n_clicks_timestamp')
              ])
def displayClick_q1(btn1, btn2):
    if int(btn1) > int(btn2):
         elapsed_time = 0
         timeLblW.append(['q1', elapsed_time])
         msg = 'Top chronometer'
    elif int(btn2) > int(btn1):
        elapsed_time = (int(btn2) - int(btn1))/1000
        timeLblW[0][1]= elapsed_time
        msg = ('Elapsed time: ' + str(elapsed_time))
    else:
        msg = ''
    return html.Div([
                    html.H4(msg)
                    ],  style={'columnCount': 1, 'fontFamily':'Helvetica'})

#. -  . -. -  . -. -  . -. -  . -. -  . -. -  . -. -  . -. -  . -. -  . -. -  . -. -  . -. -  . -
# Chronometer callback Q2
#. -  . -. -  . -. -  . -. -  . -. -  . -. -  . -. -  . -. -  . -. -  . -. -  . -. -  . -. -  . -
@app.callback(Output('container-button-timestamp-2', 'children'),
             [Input('btn-1-q2', 'n_clicks_timestamp'),
              Input('btn-2-q2', 'n_clicks_timestamp')
              ])
def displayClick_q2(btn1, btn2):
    if int(btn1) > int(btn2):
        elapsed_time = 0
        timeLblW.append( ['q2', elapsed_time])
        msg = 'Top chronometer'
    elif int(btn2) > int(btn1):
        elapsed_time = (int(btn2) - int(btn1))/1000
        timeLblW[1][1]= elapsed_time
        msg = ('Elapsed time: ' + str(elapsed_time))
    else:
        msg = ''
    return html.Div([
                    html.H4(msg)
                    ],  style={'columnCount': 1, 'fontFamily':'Helvetica'})


#. -  . -. -  . -. -  . -. -  . -. -  . -. -  . -. -  . -. -  . -. -  . -. -  . -. -  . -. -  . -
# Chronometer callback Q3
#. -  . -. -  . -. -  . -. -  . -. -  . -. -  . -. -  . -. -  . -. -  . -. -  . -. -  . -. -  . -
@app.callback(Output('container-button-timestamp-3', 'children'),
             [Input('btn-1-q3', 'n_clicks_timestamp'),
              Input('btn-2-q3', 'n_clicks_timestamp')
              ])
def displayClick_q3(btn1, btn2):
    if int(btn1) > int(btn2):
        elapsed_time = 0
        timeLblW.append( ['q3', elapsed_time])
        msg = 'Top chronometer'
    elif int(btn2) > int(btn1):
        elapsed_time = (int(btn2) - int(btn1))/1000
        timeLblW[2][1]=  elapsed_time
        msg = ('Elapsed time: ' + str(elapsed_time))
    else:
        msg = ''
    return html.Div([
                    html.H4(msg)
                    ],  style={'columnCount': 1, 'fontFamily':'Helvetica'})


#. -  . -. -  . -. -  . -. -  . -. -  . -. -  . -. -  . -. -  . -. -  . -. -  . -. -  . -. -  . -
# Chronometer callback Q4
#. -  . -. -  . -. -  . -. -  . -. -  . -. -  . -. -  . -. -  . -. -  . -. -  . -. -  . -. -  . -
@app.callback(Output('container-button-timestamp-4', 'children'),
             [Input('btn-1-q4', 'n_clicks_timestamp'),
              Input('btn-2-q4', 'n_clicks_timestamp')
              ])
def displayClick_q4(btn1, btn2):
    if int(btn1) > int(btn2):
        elapsed_time = 0
        timeLblW.append( ['q4', elapsed_time])
        msg = 'Top chronometer'
    elif int(btn2) > int(btn1):
        elapsed_time = (int(btn2) - int(btn1))/1000
        timeLblW[3][1]= elapsed_time
        msg = ('Elapsed time: ' + str(elapsed_time))
    else:
        msg = ''
    return html.Div([
                    html.H4(msg)
                    ],  style={'columnCount': 1, 'fontFamily':'Helvetica'})

#. -  . -. -  . -. -  . -. -  . -. -  . -. -  . -. -  . -. -  . -. -  . -. -  . -. -  . -. -  . -
# Chronometer callback Q5
#. -  . -. -  . -. -  . -. -  . -. -  . -. -  . -. -  . -. -  . -. -  . -. -  . -. -  . -. -  . -
@app.callback(Output('container-button-timestamp-5', 'children'),
             [Input('btn-1-q5', 'n_clicks_timestamp'),
              Input('btn-2-q5', 'n_clicks_timestamp')
              ])
def displayClick_q5(btn1, btn2):
    if int(btn1) > int(btn2):
        elapsed_time = 0
        timeLblW.append( ['q5', elapsed_time])
        msg = 'Top chronometer'
    elif int(btn2) > int(btn1):
        elapsed_time = (int(btn2) - int(btn1))/1000
        timeLblW[4][1]=  elapsed_time
        msg = ('Elapsed time: ' + str(elapsed_time))
    else:
        msg = ''
    return html.Div([
                    html.H4(msg)
                    ],  style={'columnCount': 1, 'fontFamily':'Helvetica'})

#. -  . -. -  . -. -  . -. -  . -. -  . -. -  . -. -  . -. -  . -. -  . -. -  . -. -  . -. -  . -
# Chronometer callback Q6
#. -  . -. -  . -. -  . -. -  . -. -  . -. -  . -. -  . -. -  . -. -  . -. -  . -. -  . -. -  . -
@app.callback(Output('container-button-timestamp-6', 'children'),
             [Input('btn-1-q6', 'n_clicks_timestamp'),
              Input('btn-2-q6', 'n_clicks_timestamp')
              ])
def displayClick_q6(btn1, btn2):
    if int(btn1) > int(btn2):
        elapsed_time = 0
        timeLblW.append( ['q6', elapsed_time])
        msg = 'Top chronometer'
    elif int(btn2) > int(btn1):
        elapsed_time = (int(btn2) - int(btn1))/1000
        timeLblW[5][1]=  elapsed_time
        msg = ('Elapsed time: ' + str(elapsed_time))
    else:
        msg = ''
    return html.Div([
                    html.H4(msg)
                    ],  style={'columnCount': 1, 'fontFamily':'Helvetica'})


#-------------------------------------------------------------------------------------------------------------------------------#
#                                                  Effort sliders callbacks 
#
#-------------------------------------------------------------------------------------------------------------------------------

#. -  . -. -  . -. -  . -. -  . -. -  . -. -  . -. -  . -. -  . -. -  . -. -  . -. -  . -. -  . -
# Effort slider callback Q1
#. -  . -. -  . -. -  . -. -  . -. -  . -. -  . -. -  . -. -  . -. -  . -. -  . -. -  . -. -  . -

@app.callback(
    Output(component_id ='slider-output-container-1', component_property ='children'),
    [Input(component_id = 'slider-input-container-1', component_property = 'value')]
)
def update_output_q1(value):
    if value == 0:
        msg = ('You have not selected any effort yet')
        effort = "None"
        return html.Div([
                    html.H4(msg)
               ], style={'columnCount': 1, 'fontFamily':'Helvetica', 'fontSize': 12})
    else: 
        if value == 1:
            effort = "Low"
            add_queryEffort('q1', value, effort)
            print("Effort list status:", effortW)
            msg = ('You have selected: ' + effort)
            return html.Div([
                            html.H4(msg)
                       ], style={'columnCount': 1, 'fontFamily':'Helvetica', 'fontSize': 12})

        elif value == 2:
             effort = "Regular"
             add_queryEffort('q1', value, effort)    
             msg = ('You have selected: ' + effort)
             return html.Div([
                            html.H4(msg)
                       ], style={'columnCount': 1, 'fontFamily':'Helvetica', 'fontSize': 12})
        elif value == 3:
             effort = "High"
             add_queryEffort('q1', value, effort) 
             print("Effort list status:", effortW)
             msg = ('You have selected: ' + effort)
             return html.Div([
                            html.H4(msg)
                       ], style={'columnCount': 1, 'fontFamily':'Helvetica', 'fontSize': 12})


#. -  . -. -  . -. -  . -. -  . -. -  . -. -  . -. -  . -. -  . -. -  . -. -  . -. -  . -. -  . -
# Effort slider callback Q2
#. -  . -. -  . -. -  . -. -  . -. -  . -. -  . -. -  . -. -  . -. -  . -. -  . -. -  . -. -  . -
@app.callback(
    Output(component_id ='slider-output-container-2', component_property ='children'),
    [Input(component_id = 'slider-input-container-2', component_property = 'value')]
)
def update_output_q2(value):
    if value == 0:
        msg = ('You have not selected any effort yet')
        effort = "None"
        return html.Div([
                    html.H4(msg)
               ], style={'columnCount': 1, 'fontFamily':'Helvetica'})
    else: 
        if value == 1:
            effort = "Low"
        elif value == 2:
            effort = "Regular"
        elif value == 3:
            effort = "High"
        add_queryEffort('q2', value, effort)
        msg = ('You have selected: ' + effort)
        return html.Div([
                        html.H4(msg)
                   ], style={'columnCount': 1, 'fontFamily':'Helvetica'})

#. -  . -. -  . -. -  . -. -  . -. -  . -. -  . -. -  . -. -  . -. -  . -. -  . -. -  . -. -  . -
# Effort slider callback Q3
#. -  . -. -  . -. -  . -. -  . -. -  . -. -  . -. -  . -. -  . -. -  . -. -  . -. -  . -. -  . -
@app.callback(
    Output(component_id ='slider-output-container-3', component_property ='children'),
    [Input(component_id = 'slider-input-container-3', component_property = 'value')]
)
def update_output_q3(value):
    if value == 0:
        msg = 'You have not selected any effort yet'
        effort = "None"
        return html.Div([
                    html.H4(msg)
               ], style={'columnCount': 1, 'fontFamily':'Helvetica'})
    else: 
        if value == 1:
            effort = "Low"
        elif value == 2:
            effort = "Regular"
        elif value == 3:
            effort = "High"
        add_queryEffort('q3', value, effort)
        msg = ('You have selected: ' + effort)
        return html.Div([
                        html.H4(msg)
                   ], style={'columnCount': 1, 'fontFamily':'Helvetica'})



#. -  . -. -  . -. -  . -. -  . -. -  . -. -  . -. -  . -. -  . -. -  . -. -  . -. -  . -. -  . -
# Effort slider callback Q4
#. -  . -. -  . -. -  . -. -  . -. -  . -. -  . -. -  . -. -  . -. -  . -. -  . -. -  . -. -  . -
@app.callback(
    Output(component_id ='slider-output-container-4', component_property ='children'),
    [Input(component_id = 'slider-input-container-4', component_property = 'value')]
)
def update_output_q4(value):
    if value == 0:
        msg = 'You have not selected any effort yet'
        effort = "None"
        return html.Div([
                    html.H4(msg)
               ], style={'columnCount': 1, 'fontFamily':'Helvetica'})
    else: 
        if value == 1:
            effort = "Low"
        elif value == 2:
            effort = "Regular"
        elif value == 3:
            effort = "High"
        #effortW.append(['q4', value, effort]) 
        add_queryEffort('q4', value, effort)
        msg = ('You have selected: ' + effort)
        return html.Div([
            html.H4(msg)
        ], style={'columnCount': 1, 'fontFamily':'Helvetica'})


#. -  . -. -  . -. -  . -. -  . -. -  . -. -  . -. -  . -. -  . -. -  . -. -  . -. -  . -. -  . -
# Effort slider callback Q5
#. -  . -. -  . -. -  . -. -  . -. -  . -. -  . -. -  . -. -  . -. -  . -. -  . -. -  . -. -  . -
@app.callback(
    Output(component_id ='slider-output-container-5', component_property ='children'),
    [Input(component_id = 'slider-input-container-5', component_property = 'value')]
)
def update_output_q5(value):
    if value == 0:
        msg = 'You have not selected any effort yet'
        effort = "None"
        return html.Div([
                    html.H4(msg)
               ], style={'columnCount': 1, 'fontFamily':'Helvetica'})
    else: 
        if value == 1:
            effort = "Low"
        elif value == 2:
            effort = "Regular"
        elif value == 3:
            effort = "High"
        add_queryEffort('q5', value, effort)
        msg = ('You have selected: ' + effort)
        return html.Div([
                        html.H4(msg)
                   ], style={'columnCount': 1, 'fontFamily':'Helvetica'})


#. -  . -. -  . -. -  . -. -  . -. -  . -. -  . -. -  . -. -  . -. -  . -. -  . -. -  . -. -  . -
# Effort slider callback Q6
#. -  . -. -  . -. -  . -. -  . -. -  . -. -  . -. -  . -. -  . -. -  . -. -  . -. -  . -. -  . -
@app.callback(
    Output(component_id ='slider-output-container-6', component_property ='children'),
    [Input(component_id = 'slider-input-container-6', component_property = 'value')]
)
def update_output_q6(value):
    if value == 0:
        msg = 'You have not selected any effort yet'
        effort = "None"
        return html.Div([
                    html.H4(msg)
               ], style={'columnCount': 1, 'fontFamily':'Helvetica'})
    else: 
        if  value == 1:
            effort = "Low"
        elif value == 2:
             effort = "Regular"
        elif value == 3:
             effort = "High"
        add_queryEffort('q6', value, effort)
        msg = ('You have selected: ' + effort)
        return html.Div([
                        html.H4(msg)
                   ], style={'columnCount': 1, 'fontFamily':'Helvetica'})

#-------------------------------------------------------------------------------------------------------------------------------#
#                                                  Multiple choice radio callbacks 
#
#-------------------------------------------------------------------------------------------------------------------------------

#. -  . -. -  . -. -  . -. -  . -. -  . -. -  . -. -  . -. -  . -. -  . -. -  . -. -  . -. -  . -
# Multiple choice callback Q1
#. -  . -. -  . -. -  . -. -  . -. -  . -. -  . -. -  . -. -  . -. -  . -. -  . -. -  . -. -  . -
@app.callback(
    Output(component_id = 'q1-choice-output', component_property = 'children'),
    [
        Input(component_id = 'q1-choice-input', component_property = 'value'),
        Input(component_id = 'q1-choice-input', component_property = 'id'),
    ]
)
def callback_choice_q1(dropdown_value, cid): 
        i = 0
        if dropdown_value == '':
            msg = ''
        else:
            if len(q_answers) == 0: 
                q_answers.append(['q1', [dropdown_value]])
                
                msg = ('Choice you\'ve selected: ' + str(dropdown_value))
                return html.Div([
                    html.H4(msg)
                ], style={'columnCount': 1, 'fontSize': 14,'fontFamily':'Helvetica'}
                )
            else:
                for i in range(len(q_answers)):
                    
                    if q_answers[i][0] == 'q1':               
                        
                        msg = ('You had already selected: ' + q_answers[i][0])
                        return html.Div([
                            html.H4('Already selected')
                        ], style={'columnCount': 1, 'fontSize': 14,'fontFamily':'Helvetica'}
                        )
                if i  == len(q_answers):
                    q_answers.append(['q1', [dropdown_value]])
                    msg = ('Choice you\'ve selected: ' + str(dropdown_value))
                    return html.Div([
                        html.H4(msg)
                    ], style={'columnCount': 1, 'fontSize': 14,'fontFamily':'Helvetica'}
                    )


#. -  . -. -  . -. -  . -. -  . -. -  . -. -  . -. -  . -. -  . -. -  . -. -  . -. -  . -. -  . -
# Multiple choice callback Q2
#. -  . -. -  . -. -  . -. -  . -. -  . -. -  . -. -  . -. -  . -. -  . -. -  . -. -  . -. -  . -
@app.callback(
    Output(component_id = 'q2-choice-output', component_property = 'children'),
    [
        Input(component_id = 'q2-choice-input', component_property = 'value'),
        Input(component_id = 'q2-choice-input', component_property = 'id'),
    ]
)
def callback_choice_q2(dropdown_value, cid):     
        if dropdown_value == '':
            msg = ''
        else:
            if len(q_answers) == 0: 
                q_answers.append(['q2', [dropdown_value]])
                msg = ('Choice you\'ve selected: ' + str(dropdown_value))
                return html.Div([
                    html.H4(msg)
                ], style={'columnCount': 1, 'fontSize': 14,'fontFamily':'Helvetica'}
                )
            else:
                for i in range(len(q_answers)):
                    if q_answers[i][0] == 'q2':               
                        
                        msg = ('You had already selected: ' + q_answers[i][0])
                        return html.Div([
                            html.H4('Already selected')
                        ], style={'columnCount': 1, 'fontSize': 14,'fontFamily':'Helvetica'}
                        )
                    else: i = i+1
                if i == len(q_answers):
                    q_answers.append(['q2', [dropdown_value]])
                    msg = ('Choice you\'ve selected: ' + str(dropdown_value))
                    return html.Div([
                        html.H4(msg)
                    ], style={'columnCount': 1, 'fontSize': 14,'fontFamily':'Helvetica'}
                    )
                
#. -  . -. -  . -. -  . -. -  . -. -  . -. -  . -. -  . -. -  . -. -  . -. -  . -. -  . -. -  . -
# Multiple choice callback Q4
#. -  . -. -  . -. -  . -. -  . -. -  . -. -  . -. -  . -. -  . -. -  . -. -  . -. -  . -. -  . -  
@app.callback(
    Output(component_id = 'q4-choice-output', component_property = 'children'),
    [
        Input(component_id = 'q4-choice-input', component_property = 'value'),
        Input(component_id = 'q4-choice-input', component_property = 'id'),
    ]
)
def callback_choice_q4(dropdown_value, cid): 
        if dropdown_value == '':
            msg = ''
        else:
            if len(q_answers) == 0: 
                q_answers.append(['q4', [dropdown_value]])
                msg = ('Choice you\'ve selected: ' + str(dropdown_value))
                return html.Div([
                    html.H4(msg)
                ], style={'columnCount': 1, 'fontSize': 14,'fontFamily':'Helvetica'}
                )
            else:
                for i in range(len(q_answers)):
                    if q_answers[i][0] == 'q4':               
                        msg = ('You had already selected: ' + q_answers[i][0])
                        return html.Div([
                            html.H4('Already selected')
                        ], style={'columnCount': 1, 'fontSize': 14,'fontFamily':'Helvetica'}
                        )
                    else: i = i+1
                if i == len(q_answers):
                    q_answers.append(['q4', [dropdown_value]])
                    msg = ('Choice you\'ve selected: ' + str(dropdown_value))
                    return html.Div([
                        html.H4(msg)
                    ], style={'columnCount': 1, 'fontSize': 14,'fontFamily':'Helvetica'}
                    )

#-------------------------------------------------------------------------------------------------------------------------------#
#                                                  Multiple choice drop down callbacks 
#
#-------------------------------------------------------------------------------------------------------------------------------


#. -  . -. -  . -. -  . -. -  . -. -  . -. -  . -. -  . -. -  . -. -  . -. -  . -. -  . -. -  . -
# Multiple choice drop down callback Q3
#. -  . -. -  . -. -  . -. -  . -. -  . -. -  . -. -  . -. -  . -. -  . -. -  . -. -  . -. -  . -  
@app.callback(
    dash.dependencies.Output('output-container-3', 'children'),
    [dash.dependencies.Input('my-dropdown-3', 'value')])
def update_output_q3(dropdown_value):
    if len(dropdown_value) == 0:
            msg = ''
    else:
            if len(q_answers) == 0: 
                q_answers.append(['q3', [dropdown_value]])
                msg = ('Choice you\'ve selected: ' + str(dropdown_value))
                return html.Div([
                    html.H4(msg)
                ], style={'columnCount': 1, 'fontSize': 14,'fontFamily':'Helvetica'}
                )
            else:
                for i in range(len(q_answers)):
                    if q_answers[i][0] == 'q3':               
                        q_answers[i][1] = dropdown_value
                        msg = ('You added a new attribute to your choice: ' + q_answers[i][0])
                        return html.Div([
                            html.H4('You added a new attribute to your choice'+ str(dropdown_value))
                        ], style={'columnCount': 1, 'fontSize': 14,'fontFamily':'Helvetica'}
                        )
                    else: i = i+1
                if i == len(q_answers):
                    q_answers.append(['q3', [dropdown_value]])
                    msg = ('Choice you\'ve selected: ' + str(dropdown_value))
                    return html.Div([
                        html.H4(msg)
                    ], style={'columnCount': 1, 'fontSize': 14,'fontFamily':'Helvetica'}
                    )



#. -  . -. -  . -. -  . -. -  . -. -  . -. -  . -. -  . -. -  . -. -  . -. -  . -. -  . -. -  . -
# Multiple choice drop down callback Q5
#. -  . -. -  . -. -  . -. -  . -. -  . -. -  . -. -  . -. -  . -. -  . -. -  . -. -  . -. -  . -  
@app.callback(Output('tabs-content-5', 'children'),
              [Input('tabs-5', 'value')])
def render_content_q5(tab):
    
    if tab == 'tab-Badges-q-5':
        print("Tab-1", tab)
        return html.Div([ define_dropdownMultipleOptions('my-dropdown-badges-q5', badges_attributes, 51,'True')])
    
    elif tab == 'tab-Comments-q-5':
        print("Tab-2", tab)
        return html.Div([ define_dropdownMultipleOptions('my-dropdown-comments-q5', comments_attributes, 52, 'True')])
    
    elif tab == 'tab-Posts-q-5':
        print("Tab-3", tab)
        return html.Div([ define_dropdownMultipleOptions('my-dropdown-posts-q5', posts_attributes, 53, 'True')])
            
    elif tab == 'tab-Users-q-5':
        print("Tab-4", tab)
        return html.Div([ define_dropdownMultipleOptions('my-dropdown-users-q5', users_attributes, 54, 'True')])
    
    elif tab == 'tab-Votes-q-5':
        print("Tab-5", tab)
        return html.Div([ define_dropdownMultipleOptions('my-dropdown-votes-q5', votes_attributes, 55, 'True')])



#. -  . -. -  . -. -  . -. -  . -. -  . -. -  . -. -  . -. -  . -. -  . -. -  . -. -  . -. -  . -
# Multiple choice drop down callback Q5_1
#. -  . -. -  . -. -  . -. -  . -. -  . -. -  . -. -  . -. -  . -. -  . -. -  . -. -  . -. -  . -  
@app.callback(
    dash.dependencies.Output('output-container-51', 'children'),
    [dash.dependencies.Input('my-dropdown-badges-q5', 'value')])
def update_output_q5_1(dropdown_value):
    if dropdown_value == '':
            msg = ''
    else:
            print('Initial answers size', len(q_answers))
            if len(q_answers) == 0: 
                q_answers.append(['q51', [dropdown_value]])
                msg = ('Choice you\'ve selected: ' + str(dropdown_value))
                return html.Div([
                    html.H4(msg)
                ], style={'columnCount': 1, 'fontSize': 14,'fontFamily':'Helvetica'}
                )
            else:
                for i in range(len(q_answers)):
                    if q_answers[i][0] == 'q51':               
                        q_answers[i][1] = dropdown_value
                        msg = ('You added a new attribute to your choice: ' + q_answers[i][0])
                        return html.Div([
                            html.H4('You added a new attribute to your choice'+ str(dropdown_value))
                        ], style={'columnCount': 1, 'fontSize': 14,'fontFamily':'Helvetica'}
                        )
                    else: i = i+1
                if i == len(q_answers):
                    q_answers.append(['q51', [dropdown_value]])
                    msg = ('Choice you\'ve selected: ' + str(dropdown_value))
                    return html.Div([
                        html.H4(msg)
                    ], style={'columnCount': 1, 'fontSize': 14,'fontFamily':'Helvetica'}
                    )


#. -  . -. -  . -. -  . -. -  . -. -  . -. -  . -. -  . -. -  . -. -  . -. -  . -. -  . -. -  . -
# Multiple choice drop down callback Q5_2
#. -  . -. -  . -. -  . -. -  . -. -  . -. -  . -. -  . -. -  . -. -  . -. -  . -. -  . -. -  . -  
@app.callback(
    dash.dependencies.Output('output-container-52', 'children'),
    [dash.dependencies.Input('my-dropdown-comments-q5', 'value')])
def update_output_q5_2(dropdown_value):
    if dropdown_value == '':
            msg = ''
    else:
            if len(q_answers) == 0: 
                q_answers.append(['q52', [dropdown_value]])
                msg = ('Choice you\'ve selected: ' + str(dropdown_value))
                return html.Div([
                    html.H4(msg)
                ], style={'columnCount': 1, 'fontSize': 14,'fontFamily':'Helvetica'}
                )
            else:
                for i in range(len(q_answers)):
                    if q_answers[i][0] == 'q52':               
                        q_answers[i][1] = dropdown_value
                        msg = ('You added a new attribute to your choice: ' + q_answers[i][0])
                        return html.Div([
                            html.H4('You added a new attribute to your choice'+ str(dropdown_value))
                        ], style={'columnCount': 1, 'fontSize': 14,'fontFamily':'Helvetica'}
                        )
                    else: i = i+1
                if i == len(q_answers):
                    q_answers.append(['q52', [dropdown_value]])
                    msg = ('Choice you\'ve selected: ' + str(dropdown_value))
                    return html.Div([
                        html.H4(msg)
                    ], style={'columnCount': 1, 'fontSize': 14,'fontFamily':'Helvetica'}
                    )

#. -  . -. -  . -. -  . -. -  . -. -  . -. -  . -. -  . -. -  . -. -  . -. -  . -. -  . -. -  . -
# Multiple choice drop down callback Q5_3
#. -  . -. -  . -. -  . -. -  . -. -  . -. -  . -. -  . -. -  . -. -  . -. -  . -. -  . -. -  . -  
@app.callback(
    dash.dependencies.Output('output-container-53', 'children'),
    [dash.dependencies.Input('my-dropdown-posts-q5', 'value')])
def update_output_q5_3(dropdown_value):
    if dropdown_value == '':
            msg = ''
    else:
            if len(q_answers) == 0: 
                q_answers.append(['q53', [dropdown_value]])
                msg = ('Choice you\'ve selected: ' + str(dropdown_value))
                return html.Div([
                    html.H4(msg)
                ], style={'columnCount': 1, 'fontSize': 14,'fontFamily':'Helvetica'}
                )
            else:
                for i in range(len(q_answers)):
                    if q_answers[i][0] == 'q53':               
                        q_answers[i][1] = dropdown_value
                        msg = ('You added a new attribute to your choice: ' + q_answers[i][0])
                        return html.Div([
                            html.H4('You added a new attribute to your choice'+ str(dropdown_value))
                        ], style={'columnCount': 1, 'fontSize': 14,'fontFamily':'Helvetica'}
                        )
                    else: i = i+1
                if i == len(q_answers):
                    q_answers.append(['q53', [dropdown_value]])
                    msg = ('Choice you\'ve selected: ' + str(dropdown_value))
                    return html.Div([
                        html.H4(msg)
                    ], style={'columnCount': 1, 'fontSize': 14,'fontFamily':'Helvetica'}
                    )

#. -  . -. -  . -. -  . -. -  . -. -  . -. -  . -. -  . -. -  . -. -  . -. -  . -. -  . -. -  . -
# Multiple choice drop down callback Q5_4
#. -  . -. -  . -. -  . -. -  . -. -  . -. -  . -. -  . -. -  . -. -  . -. -  . -. -  . -. -  . -  
@app.callback(
    dash.dependencies.Output('output-container-54', 'children'),
    [dash.dependencies.Input('my-dropdown-users-q5', 'value')])
def update_output_q5_4(dropdown_value):
    if dropdown_value == '':
            msg = ''
    else:
            if len(q_answers) == 0: 
                q_answers.append(['q54', [dropdown_value]])
                msg = ('Choice you\'ve selected: ' + str(dropdown_value))
                return html.Div([
                    html.H4(msg)
                ], style={'columnCount': 1, 'fontSize': 14,'fontFamily':'Helvetica'}
                )
            else:
                for i in range(len(q_answers)):
                    if q_answers[i][0] == 'q54':               
                        q_answers[i][1] = dropdown_value
                        msg = ('You added a new attribute to your choice: ' + q_answers[i][0])
                        return html.Div([
                            html.H4('You added a new attribute to your choice'+ str(dropdown_value))
                        ], style={'columnCount': 1, 'fontSize': 14,'fontFamily':'Helvetica'}
                        )
                    else: i = i+1
                if i == len(q_answers):
                    q_answers.append(['q54', [dropdown_value]])
                    msg = ('Choice you\'ve selected: ' + str(dropdown_value))
                    return html.Div([
                        html.H4(msg)
                    ], style={'columnCount': 1, 'fontSize': 14,'fontFamily':'Helvetica'}
                    )

#. -  . -. -  . -. -  . -. -  . -. -  . -. -  . -. -  . -. -  . -. -  . -. -  . -. -  . -. -  . -
# Multiple choice drop down callback Q5_5
#. -  . -. -  . -. -  . -. -  . -. -  . -. -  . -. -  . -. -  . -. -  . -. -  . -. -  . -. -  . -  
@app.callback(
    dash.dependencies.Output('output-container-55', 'children'),
    [dash.dependencies.Input('my-dropdown-votes-q5', 'value')])
def update_output_q5_5(dropdown_value):
    if dropdown_value == '':
            msg = ''
    else:
            if len(q_answers) == 0: 
                q_answers.append(['q55', [dropdown_value]])
                msg = ('Choice you\'ve selected: ' + str(dropdown_value))
                return html.Div([
                    html.H4(msg)
                ], style={'columnCount': 1, 'fontSize': 14,'fontFamily':'Helvetica'}
                )
            else:
                for i in range(len(q_answers)):
                    if q_answers[i][0] == 'q55':               
                        q_answers[i][1] = dropdown_value
                        msg = ('You added a new attribute to your choice: ' + q_answers[i][0])
                        return html.Div([
                            html.H4('You added a new attribute to your choice'+ str(dropdown_value))
                        ], style={'columnCount': 1, 'fontSize': 14,'fontFamily':'Helvetica'}
                        )
                    else: i = i+1
                if i == len(q_answers):
                    q_answers.append(['q55', [dropdown_value]])
                    msg = ('Choice you\'ve selected: ' + str(dropdown_value))
                    return html.Div([
                        html.H4(msg)
                    ], style={'columnCount': 1, 'fontSize': 14,'fontFamily':'Helvetica'}
                    )


#. -  . -. -  . -. -  . -. -  . -. -  . -. -  . -. -  . -. -  . -. -  . -. -  . -. -  . -. -  . -
# Multiple choice drop down callback Q6
#. -  . -. -  . -. -  . -. -  . -. -  . -. -  . -. -  . -. -  . -. -  . -. -  . -. -  . -. -  . -  
@app.callback(Output('tabs-content-6', 'children'),
              [Input('tabs-6', 'value')])
def render_content_q5(tab):
    
    if tab == 'tab-Badges-q-6':
        print("Tab-1 q6", tab)
        return html.Div([ define_dropdownMultipleOptions('my-dropdown-badges-q6', badges_attributes, 61,'True')])
    
    elif tab == 'tab-Comments-q-6':
        print("Tab-2 q6", tab)
        return html.Div([ define_dropdownMultipleOptions('my-dropdown-comments-q6', comments_attributes, 62, 'True')])
    
    elif tab == 'tab-Posts-q-6':
        print("Tab-3 q6", tab)
        return html.Div([ define_dropdownMultipleOptions('my-dropdown-posts-q6', posts_attributes, 63, 'True')])
            
            
    elif tab == 'tab-Users-q-6':
        print("Tab-4 q6", tab)
        return html.Div([ define_dropdownMultipleOptions('my-dropdown-users-q6', users_attributes, 64, 'True')])
    
    elif tab == 'tab-Votes-q-6':
        print("Tab-5 q6", tab)
        return html.Div([ define_dropdownMultipleOptions('my-dropdown-votes-q6', votes_attributes, 65, 'True')])

#. -  . -. -  . -. -  . -. -  . -. -  . -. -  . -. -  . -. -  . -. -  . -. -  . -. -  . -. -  . -
# Multiple choice drop down callback Q6_1
#. -  . -. -  . -. -  . -. -  . -. -  . -. -  . -. -  . -. -  . -. -  . -. -  . -. -  . -. -  . -  
@app.callback(
    dash.dependencies.Output('output-container-61', 'children'),
    [dash.dependencies.Input('my-dropdown-badges-q6', 'value')])
def update_output_q6_1(dropdown_value):
    if dropdown_value == '':
            msg = ''
    else:
            if len(q_answers) == 0: 
                q_answers.append(['q61', [dropdown_value]])
                msg = ('Choice you\'ve selected: ' + str(dropdown_value))
                return html.Div([
                    html.H4(msg)
                ], style={'columnCount': 1, 'fontSize': 14,'fontFamily':'Helvetica'}
                )
            else:
                for i in range(len(q_answers)):
                    if q_answers[i][0] == 'q61':               
                        q_answers[i][1] = dropdown_value
                        msg = ('You added a new attribute to your choice: ' + q_answers[i][0])
                        return html.Div([
                            html.H4('You added a new attribute to your choice'+ str(dropdown_value))
                        ], style={'columnCount': 1, 'fontSize': 14,'fontFamily':'Helvetica'}
                        )
                    else: i = i+1
                if i == len(q_answers):
                    q_answers.append(['q61', [dropdown_value]])
                    msg = ('Choice you\'ve selected: ' + str(dropdown_value))
                    return html.Div([
                        html.H4(msg)
                    ], style={'columnCount': 1, 'fontSize': 14,'fontFamily':'Helvetica'}
                    )


#. -  . -. -  . -. -  . -. -  . -. -  . -. -  . -. -  . -. -  . -. -  . -. -  . -. -  . -. -  . -
# Multiple choice drop down callback Q6_2
#. -  . -. -  . -. -  . -. -  . -. -  . -. -  . -. -  . -. -  . -. -  . -. -  . -. -  . -. -  . -  
@app.callback(
    dash.dependencies.Output('output-container-62', 'children'),
    [dash.dependencies.Input('my-dropdown-comments-q6', 'value')])
def update_output_q6_2(dropdown_value):
    if dropdown_value == '':
            msg = ''
    else:
            
            if len(q_answers) == 0: 
                q_answers.append(['q62', [dropdown_value]])
                msg = ('Choice you\'ve selected: ' + str(dropdown_value))
                return html.Div([
                    html.H4(msg)
                ], style={'columnCount': 1, 'fontSize': 14,'fontFamily':'Helvetica'}
                )
            else:
                for i in range(len(q_answers)):
                    if q_answers[i][0] == 'q62':               
                        q_answers[i][1] = dropdown_value
                        msg = ('You added a new attribute to your choice: ' + q_answers[i][0])
                        return html.Div([
                            html.H4('You added a new attribute to your choice'+ str(dropdown_value))
                        ], style={'columnCount': 1, 'fontSize': 14,'fontFamily':'Helvetica'}
                        )
                    else: i = i+1
                if i == len(q_answers):
                    q_answers.append(['q62', [dropdown_value]])
                    msg = ('Choice you\'ve selected: ' + str(dropdown_value))
                    return html.Div([
                        html.H4(msg)
                    ], style={'columnCount': 1, 'fontSize': 14,'fontFamily':'Helvetica'}
                    )

#. -  . -. -  . -. -  . -. -  . -. -  . -. -  . -. -  . -. -  . -. -  . -. -  . -. -  . -. -  . -
# Multiple choice drop down callback Q6_3
#. -  . -. -  . -. -  . -. -  . -. -  . -. -  . -. -  . -. -  . -. -  . -. -  . -. -  . -. -  . -  
@app.callback(
    dash.dependencies.Output('output-container-63', 'children'),
    [dash.dependencies.Input('my-dropdown-posts-q6', 'value')])
def update_output_q6_3(dropdown_value):
    if dropdown_value == '':
            msg = ''
    else:
            
            if len(q_answers) == 0: 
                q_answers.append(['q63', [dropdown_value]])
                msg = ('Choice you\'ve selected: ' + str(dropdown_value))
                return html.Div([
                    html.H4(msg)
                ], style={'columnCount': 1, 'fontSize': 14,'fontFamily':'Helvetica'}
                )
            else:
                for i in range(len(q_answers)):
                    if q_answers[i][0] == 'q63':               
                        q_answers[i][1] = dropdown_value
                        msg = ('You added a new attribute to your choice: ' + q_answers[i][0])
                        return html.Div([
                            html.H4('You added a new attribute to your choice'+ str(dropdown_value))
                        ], style={'columnCount': 1, 'fontSize': 14,'fontFamily':'Helvetica'}
                        )
                    else: i = i+1
                if i == len(q_answers):
                    q_answers.append(['q63', [dropdown_value]])
                    msg = ('Choice you\'ve selected: ' + str(dropdown_value))
                    return html.Div([
                        html.H4(msg)
                    ], style={'columnCount': 1, 'fontSize': 14,'fontFamily':'Helvetica'}
                    )

#. -  . -. -  . -. -  . -. -  . -. -  . -. -  . -. -  . -. -  . -. -  . -. -  . -. -  . -. -  . -
# Multiple choice drop down callback Q6_4
#. -  . -. -  . -. -  . -. -  . -. -  . -. -  . -. -  . -. -  . -. -  . -. -  . -. -  . -. -  . -  
@app.callback(
    dash.dependencies.Output('output-container-64', 'children'),
    [dash.dependencies.Input('my-dropdown-users-q6', 'value')])
def update_output_q6_4(dropdown_value):
    if dropdown_value == '':
            msg = ''
    else:
            if len(q_answers) == 0: 
                q_answers.append(['q64', [dropdown_value]])
                
                msg = ('Choice you\'ve selected: ' + str(dropdown_value))
                return html.Div([
                    html.H4(msg)
                ], style={'columnCount': 1, 'fontSize': 14,'fontFamily':'Helvetica'}
                )
            else:
                for i in range(len(q_answers)):
                    if q_answers[i][0] == 'q64':               
                        q_answers[i][1] = dropdown_value
                        msg = ('You added a new attribute to your choice: ' + q_answers[i][0])
                        return html.Div([
                            html.H4('You added a new attribute to your choice'+ str(dropdown_value))
                        ], style={'columnCount': 1, 'fontSize': 14,'fontFamily':'Helvetica'}
                        )
                    else: i = i+1
                if i == len(q_answers):
                    q_answers.append(['q64', [dropdown_value]])
                    msg = ('Choice you\'ve selected: ' + str(dropdown_value))
                    return html.Div([
                        html.H4(msg)
                    ], style={'columnCount': 1, 'fontSize': 14,'fontFamily':'Helvetica'}
                    )

#. -  . -. -  . -. -  . -. -  . -. -  . -. -  . -. -  . -. -  . -. -  . -. -  . -. -  . -. -  . -
# Multiple choice drop down callback Q6_5
#. -  . -. -  . -. -  . -. -  . -. -  . -. -  . -. -  . -. -  . -. -  . -. -  . -. -  . -. -  . -  
@app.callback(
    dash.dependencies.Output('output-container-65', 'children'),
    [dash.dependencies.Input('my-dropdown-votes-q6', 'value')])
def update_output_q6_5(dropdown_value):
    if dropdown_value == '':
            msg = ''
    else:
            
            if len(q_answers) == 0: 
                q_answers.append(['q65', [dropdown_value]])
                msg = ('Choice you\'ve selected: ' + str(dropdown_value))
                return html.Div([
                    html.H4(msg)
                ], style={'columnCount': 1, 'fontSize': 14,'fontFamily':'Helvetica'}
                )
            else:
                for i in range(len(q_answers)):
                    
                    if q_answers[i][0] == 'q65':               
                        q_answers[i][1] = dropdown_value
                        msg = ('You added a new attribute to your choice: ' + q_answers[i][0])
                        return html.Div([
                            html.H4('You added a new attribute to your choice'+ str(dropdown_value))
                        ], style={'columnCount': 1, 'fontSize': 14,'fontFamily':'Helvetica'}
                        )
                    else: i = i+1
                if i == len(q_answers):
                    q_answers.append(['q65', [dropdown_value]])
                    msg = ('Choice you\'ve selected: ' + str(dropdown_value))
                    return html.Div([
                        html.H4(msg)
                    ], style={'columnCount': 1, 'fontSize': 14,'fontFamily':'Helvetica'}
                    )


#-------------------------------------------------------------------------------------------------------------------------------#
#                                                  Submit button callbacks 
#
#-------------------------------------------------------------------------------------------------------------------------------


#. -  . -. -  . -. -  . -. -  . -. -  . -. -  . -. -  . -. -  . -. -  . -. -  . -. -  . -. -  . -
# Submit button callback 
#. -  . -. -  . -. -  . -. -  . -. -  . -. -  . -. -  . -. -  . -. -  . -. -  . -. -  . -. -  . -  
@app.callback(
    dash.dependencies.Output('container-button-basic', 'children'),
    [dash.dependencies.Input('button', 'n_clicks')])
def update_output(n_clicks):
    results = get_Results(effortW, timeLblW, q_answers)
    print("$$$$$$$$$$$$$$$$$", results)
    # (scoreL, calcEffortL, questions_time, questions_effort )
    store_Game_Results(results[0], results[3], results[2], results[1], execution_time)
    msg= "The  button has been clicked  times: " + str(n_clicks)
    return html.Div([
                            html.H4(msg)
                        ], style={'columnCount': 1, 'fontSize': 12, 'fontFamily':'Helvetica'}
                   )

#-------------------------------------------------------------------------------------------------------------------------------#
#                                                  Main app call 
#
#-------------------------------------------------------------------------------------------------------------------------------


if __name__ == '__main__':
    start_time = timeit.default_timer()
    execution_time = timeit.default_timer() - start_time
    app.run_server(debug=True)
    
 