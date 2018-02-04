

clc;
clear;

path=pwd;
userpath(path);


%result=jpgandalpha('fudan.bmp','test.bmp');
a='fudan.bmp';
b='test.bmp';

alpha=0.1;

[count,msg,result,aa,bb]= hidedctadv(a,b,alpha);

c='15300240004_hiddenimage.bmp';
result=extractdctadv(c,count,aa,bb);
