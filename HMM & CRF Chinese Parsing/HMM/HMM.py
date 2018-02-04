#-*-coding:utf-8 -*-
#HMM
#Author: Ao Wang, 15300240004

import sys
import os

def state_affirm(i,len):
    '''
    verify the state of the word
    '''
    if len==1:
        return "S"
    if i==0:
        return "B"
    if i==len-1:
        return "E"
    return "M"

def state2num(state):
    if state=="B":
        return 0
    if state=="M":
        return 1
    if state=="E":
        return 2
    if state=="S":
        return 3

def num2state(num):
    if num==0:
        return 'B'
    if num==1:
        return 'M'
    if num==2:
        return 'E'
    if num==3:
        return 'S'

def HMM_train(file):
    '''
    To train a HMM with an alreay-partitoned corpus.
    Input a string which indicates the path of the training corpus.
    Return InitiateProb, TransProbMatrix, EmitProbMatrix
    '''
    corpus=open(file,"r")#change the path when needed
    lines=corpus.readlines()
    corpus.close()

    StateCountMatrix=[[0 for i in range(4)] for i in range(4)]
    TransProbMatrix=[[0.0 for i in range(4)] for i in range(4)]
    #the matrix of state transportation probability

    InitiateCount=[0 for i in range(4)]
    InitiateProb=[0.0 for i in range(4)]
    #the initial states probability

    EmitProbMatrix={"B":{},"M":{},"E":{},"S":{}}
    #the probability matrix of state to observation

    #order: B M E S
    print "start training"
    for line in lines:
        line = line.decode('utf8')
        line = line.replace(' \n','')
        line = line.replace('\n','')
        words=line.split(" ")

        total_statestr=""
        for word in words:
            word=word.strip()
            statestr=""
            for i in range(len(word)):
                state=state_affirm(i,len(word))
                statestr+=state
            total_statestr+=statestr#get the state string
            for i in range(len(word)):
                EmitProbMatrix[statestr[i]].setdefault(word[i],0)
                EmitProbMatrix[statestr[i]][word[i]]+=1
                #get the num of the EmitProbMatrix
            if word in words and words.index(word)==0:
                InitiateCount[state2num(statestr[0])]+=1
                #get the num of the InitiateCount
        for i in range(len(total_statestr)-1):
            a=state2num(total_statestr[i])
            b=state2num(total_statestr[i+1])
            StateCountMatrix[a][b]+=1
            #get the StateCountMatrix

    for row in range(4):
        row_sum=0;
        for column in range(4):
            row_sum+=StateCountMatrix[row][column]
        for column in range(4):
            TransProbMatrix[row][column]=float(StateCountMatrix[row][column])/float(row_sum)
            #transfer from count to probability

    isum=0
    for i in range(4):
        isum+=InitiateCount[i]
    for i in range(4):
        InitiateProb[i]=float(InitiateCount[i])/float(isum)
        #transfer from count to probability
        
    for key in EmitProbMatrix:
        dsum=0
        for subkey in EmitProbMatrix[key]:
            dsum+=EmitProbMatrix[key][subkey]
        for subkey in EmitProbMatrix[key]:
            EmitProbMatrix[key][subkey]=float(EmitProbMatrix[key][subkey])/float(dsum)
            #transfer from count to probability
    
    print "training finished"
    return InitiateProb,TransProbMatrix,EmitProbMatrix




def partition(sentence,InitiateProb,TransProbMatrix,EmitProbMatrix):
    '''
    Used to partiton Chinese sentences based on Viterbi algorithm.
    InitiateProb: the probability distribution of initial state
    TransProbMatrix: TransProbMatrix[i][j] indicates the probability of transfering from state[i] to state[j]
    EmitProbMatrix: EmitProbMatrix[i][j] = P( Observed[j] | Status[i] )
    '''
    #order: B M E S
    sentence = sentence.decode('utf8')
    sentence = sentence.strip()
    sentence = sentence.replace('\n','')
    length=len(sentence)
    if length==0:
        return []

    weight=[[0.0 for i in range(length)]for i in range(4)]
    path=[[0 for i in range(length)]for i in range(4)]

    #initiate
    if sentence[0] not in EmitProbMatrix['B']:
        weight[0][0]=0.0
    else:
        weight[0][0]=InitiateProb[0] * EmitProbMatrix['B'][sentence[0]]
    weight[1][0]=0.0#start state cannot be M
    weight[2][0]=0.0#start state cannot be E
    if sentence[0] not in EmitProbMatrix['S']:
        weight[3][0]=0.0
    else:
        weight[3][0]=InitiateProb[3] * EmitProbMatrix['S'][sentence[0]]
    #calculate, Viterbi algorithm
    for t in range(1,length):
        for i in range(4):
            tmp_list=[]
            for j in range(4):
                if sentence[t] not in EmitProbMatrix[num2state(i)]:
                    continue
                tmp= weight[j][t-1] * TransProbMatrix[j][i] * EmitProbMatrix[num2state(i)][sentence[t]]
                tmp_list.append(tmp)
            if len(tmp_list)==0:
                tmp_list=[0,0,0,1]
            max_value=max(tmp_list)
            weight[i][t]=max_value
            dotj=tmp_list.index(max_value)
            path[i][t]=dotj
  
    max_node=0
    if weight[2][length-1]>weight[3][length-1]:
        max_node=2
    else:
        max_node=3
    #start going backwards
    res_path=[]
    res_path.append(max_node)
    for i in range(length-2,-1,-1):
        node=path[max_node][i+1]
        max_node=node
        res_path.append(max_node)
    
    path=[]
    for i in range(len(res_path)-1,-1,-1):
        path.append(num2state(res_path[i]))
    
    res=[]
    str_=""
    for i in range(len(path)):
        if path[i]=="B":
            str_=""
            str_+=sentence[i]        
        if path[i]=="M":
            str_+=sentence[i]       
        if path[i]=="E":
            str_+=sentence[i]
            if len(str_)!=0:
                res.append(str_)       
        if path[i]=="S":
            res.append(sentence[i])
            str_=""
    return res
