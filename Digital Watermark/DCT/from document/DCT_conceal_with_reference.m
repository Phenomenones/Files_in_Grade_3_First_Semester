clc;
clear;

alpha=0.3;%use to control the robustness of the watermark
key=233;%as the random seed to choose block

RGB=imread('Lenna.bmp');
RGB=double(RGB)/255;
gray_image=RGB(:,:,1);%turn the chromatic image to gray
T=dctmtx(8);
DCTrgb=blkproc(gray_image,[8 8],'P1 * x * P2',T,T');

%DCT watermark hidding
hide_info=fopen('hidefile.txt','r');
[msg,count]=fread(hide_info,'ubit1');%read the secret info to hide_matrix
fclose(hide_info);

[row,col]=size(DCTrgb);
row=floor(row/8);
col=floor(col/8);
a=zeros([row col]);



%[k1,k2]=randinterval(a,count,key);

[m, n] = size(a);
interval1 = floor(m * n/count) + 1;
interval2 = interval1 - 2;
%if interval2 == 0
    %error('Carrier is too small');
%end
rand('seed',key);
a = rand(1, count);
row = zeros([1 count]);
col = zeros([1 count]);
r = 1;
c = 1;
row(1,1) = r;
col(1,1) = c;
for i =2:count
    if a(i) >= 0.5
        c = c + interval1;
    else
        c = c + interval2;
    end
    if c > n
        r = r + 1;
        %if r > m
            %error('Carrier is too small');
        %end
        c = mod(c, n);
        if c == 0
            c = 1;
        end
    end
    row(1, i) = r;
    col(1, i) = c;
end

k1=row;
k2=col;

for i = 1:count
    k1(1,i)=(k1(1,i)-1)*8+1;
    k2(1,i)=(k2(1,i)-1)*8+1;
end

%start embedding
temp=0;

%use (6,3) and (3,5)
for i=1:count
    if msg(i,1)==0
        if DCTrgb(k1(i)+6,k2(i)+3)>DCTrgb(k1(i)+3,k2(i)+5)
            temp=DCTrgb(k1(i)+3,k2(i)+5);
            DCTrgb(k1(i)+3,k2(i)+5)=DCTrgb(k1(i)+6,k2(i)+3);
            DCTrgb(k1(i)+6,k2(i)+3)=temp;
        end
    else
        if DCTrgb(k1(i)+6,k2(i)+3)<DCTrgb(k1(i)+3,k2(i)+5)
            temp=DCTrgb(k1(i)+3,k2(i)+5);
            DCTrgb(k1(i)+3,k2(i)+5)=DCTrgb(k1(i)+6,k2(i)+3);
            DCTrgb(k1(i)+6,k2(i)+3)=temp;
        end
    end
    if DCTrgb(k1(i)+6,k2(i)+3)>DCTrgb(k1(i)+3,k2(i)+5)
        DCTrgb(k1(i)+3,k2(i)+5)=DCTrgb(k1(i)+3,k2(i)+5)-alpha;
    else
        DCTrgb(k1(i)+6,k2(i)+3)=DCTrgb(k1(i)+6,k2(i)+3)-alpha;
    end
end

DCTrgb1=DCTrgb;
res=blkproc(DCTrgb,[8 8],'P1 * x * P2',T',T);
result=RGB;
result(:,:,1)=res;

subplot(1,1,1),imshow(result);title('image with watermark');

imwrite(result,'15300240004_hiddenimage.bmp','bmp');

