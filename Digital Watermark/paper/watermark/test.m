%Designed by Wang Ao, 15300240004

clc;
clear;
path=pwd;
userpath(path);

a=3;    %Arnold shuffle coefficient
b=5;    %Arnold shuffle coefficient
n=9;    %if n=12, the Arnold shuffle will go back to the start
k=7;    
initial_value=0.87; %Chebyshev chaos coefficient
%the alphas should be above 5 to avoid noise interference
alpha1=5.1;
alpha2=5.11;
alpha3=5.12;


[image_with_mark,encrypt_mat,U_mat,V_mat] = hide(a,b,n,'Lenna.bmp','watermark.bmp',k,initial_value,alpha1,alpha2,alpha3);
%image_with_mark=imnoise(image_with_mark,'gaussian',0.01);

%image_with_mark=filter2(fspecial('average',2),image_with_mark);

imwrite(image_with_mark,'watermarked_Lenna.bmp','bmp');
%imwrite(image_with_mark,'watermarked_Lenna.jpg','jpg','quality',90);

[LL,HL,LH,HH] = extract('Lenna.bmp','watermarked_Lenna.bmp',encrypt_mat,a,b,n,alpha1,alpha2,alpha3,U_mat,V_mat);
%choose the one with the biggest NC value as the extracted watermark
original_watermark=imread('watermark.bmp');
NC1=nc(original_watermark,LL);
NC2=nc(original_watermark,HL);
NC3=nc(original_watermark,LH);
NC4=nc(original_watermark,HH);
NC=[NC1,NC2,NC3,NC4];
[m,i] = max(NC);
if i==1
    watermark=LL;
end
if i==2
    watermark=HL;
end
if i==3
    watermark=LH;
end
if i==4
    watermark=HH;
end
imshow(watermark);

imwrite(watermark,'extracted_watermark.bmp','bmp');

aaa=imread('watermark.bmp');
bbb=imread('extracted_watermark.bmp');
c=nc(aaa,bbb)

