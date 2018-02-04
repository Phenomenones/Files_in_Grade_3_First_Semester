# -*- coding:utf-8 -*-  
#Author: Ao Wang, 15300240004

import sklearn_crfsuite
from sklearn.externals import joblib
import pickle

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

def real_sen_len(sen):
    sen = sen.replace(' \n','')
    sen = sen.replace('\n','')
    words=sen.split(" ")
    i=0
    for word in words:
        for letter in word:
            i+=1
    return i

def real_sen(sen):
    sen = sen.replace(' \n','')
    sen = sen.replace('\n','')
    words=sen.split(" ")
    res=""
    for word in words:
        res+=word
    return res

def character2features(i,sen):
    '''
    get the feature dictionary of the single character of the word
    '''
    sen=real_sen(sen)
    feature_dic={}
    if i >= 1 and i<= real_sen_len(sen)-2:#ordinary situation
        feature_dic["qzh"]=sen[i-1]+sen[i]+sen[i+1]
        feature_dic["qz"]=sen[i-1]+sen[i]
        feature_dic["zh"]=sen[i]+sen[i+1]
        feature_dic["qh"]=sen[i-1]+sen[i+1]
        feature_dic["q"]=sen[i-1]
        feature_dic["z"]=sen[i]
        feature_dic["h"]=sen[i+1]
        return feature_dic

    if i==0 and len(sen)!=1:#the first character, which has no prior character
        feature_dic["qzh"]='*'+sen[i]+sen[i+1]
        feature_dic["qz"]='*'+sen[i]
        feature_dic["zh"]=sen[i]+sen[i+1]
        feature_dic["qh"]='*'+sen[i+1]
        feature_dic["q"]='*'
        feature_dic["z"]=sen[i]
        feature_dic["h"]=sen[i+1]
        return feature_dic

    if i==real_sen_len(sen)-1:#the last character, which has no succeeding character
        feature_dic["qzh"]=sen[i-1]+sen[i]+'*'
        feature_dic["qz"]=sen[i-1]+sen[i]
        feature_dic["zh"]=sen[i]+'*'
        feature_dic["qh"]=sen[i-1]+'*'
        feature_dic["q"]=sen[i-1]
        feature_dic["z"]=sen[i]
        feature_dic["h"]='*'
        return feature_dic

    if len(sen) == 1:#single character situation
        feature_dic["qzh"]='*'+sen[i]+'*'
        feature_dic["qz"]='*'+sen[i]
        feature_dic["zh"]=sen[i]+'*'
        feature_dic["qh"]='*'+'*'
        feature_dic["q"]='*'
        feature_dic["z"]=sen[i]
        feature_dic["h"]='*'
        return feature_dic
        

def CRF_train(file):
    x_train=[]
    y_train=[]

    train_file=open(file,"r")
    lines=train_file.readlines()
    train_file.close()
    it=0
    for line in lines:
        it+=1
        if it%1000==0:
            print it
        line=line.decode("utf8")
        line = line.replace(' \n','')
        line = line.replace('\n','')
        words=line.split(" ")

        total_statestr=""
        x_sentence=[]
        for word in words:
            word=word.strip()
            statestr=""
            for i in range(len(word)):
                state=state_affirm(i,len(word))
                statestr+=state
            total_statestr+=statestr#get the state string
        flag=0
        for i in range(real_sen_len(line)):
            tmp=character2features(i,line)
            if real_sen_len(line)!=len(total_statestr):
                flag=1
                print "Warning! len(sen) != len(total_statestr)"
                #set the flag when the length of the state string and sentence are not the same, then discard this sentence
                break
            x_sentence.append(tmp)
        if flag==0:
            x_train.append(x_sentence)
            ss=[stri for stri in total_statestr]
            y_train.append(ss)
    
    #initiate the CRF model
    crf = sklearn_crfsuite.CRF(
        algorithm='lbfgs',
        c1=0.1,#L1 regularization
        c2=0.1,#L2 regularrization
        max_iterations=200,
        all_possible_transitions=True
    )
    print "start training"
    crf.fit(x_train, y_train)
    return crf

def predict_input(sen):
    '''the return is the list of features dictionaries
    '''
    sen=sen.decode("utf8")
    res=[character2features(i,sen) for i in range(len(sen))]
    return res

def partition(sen,crf):
    sen = sen.replace(' \n','')
    sen = sen.replace('\n','')
    sen = sen.replace(' ','')
    char=predict_input(sen)
    path = crf.predict_single(char)  
    sen=sen.decode("utf8")
    res=[]
    str_=""
    for i in range(len(sen)):
        if path[i]=="B":
            str_=""
            str_+=sen[i]        
        if path[i]=="M":
            str_+=sen[i]       
        if path[i]=="E":
            str_+=sen[i]
            if len(str_)!=0:
                res.append(str_)       
        if path[i]=="S":
            res.append(sen[i])
            str_=""
    return res
