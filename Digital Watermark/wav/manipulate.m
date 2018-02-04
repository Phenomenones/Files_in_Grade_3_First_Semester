clc;
clear;

path=pwd;
userpath(path); %change to current directory

wav='djh.wav';
image='fudan.bmp';
pic_data=imread(image);

bit=1;  %choose which bit of the byte to hide, 1 is the lowest, 8 is the highest

[a,b,wav_with_mark,bit] = hidelsbwav(wav,image,bit);

watermark_image = extractlsbwav(a,b,wav_with_mark,bit);

nc_coef=nc(pic_data,watermark_image)

[x,Fs]=audioread('watermarked.wav');
sound(x,11025);
