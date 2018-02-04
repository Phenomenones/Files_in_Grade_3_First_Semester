function[count,msg,result,aa,bb] = hidedctadv(image,msg,alpha)

msg=imread(msg);    %input secret image
[aa,bb]=size(msg);
count=aa*bb;

message=msg;
msg=[];
for i =1:aa
    msg=[msg,message(i,:)]; %turn the image to bit array
end

msg=reshape(msg,count,1);

data0=imread(image);
data0=double(data0)/255;
data=data0(:,:,1);  %take out the first layer

T=dctmtx(8);    %DCT
DCTrgb=blkproc(data,[8 8],'P1 * x * P2',T,T');  %partition the image to 8*8 blocks

[row,col]=size(DCTrgb);
row=floor(row/8);
col=floor(col/8);

k1=[];
k2=[];

for i=1:row
    k1=[k1,i];
end
for i =1:col
    k2=[k2,i];
end

for i=1:row
    k1(1,i)=(k1(1,i)-1)*8+1;
end
for i =1:col
    k2(1,i)=(k2(1,i)-1)*8+1;
end

%start embedding

%use (5,2) and (4,3)
for i=1:row
    for j=1:col
        if msg((i-1)*col+j,1)==0
            if DCTrgb(k1(i)+5,k2(j)+2)>DCTrgb(k1(i)+4,k2(j)+3)  %exchange if the relationship is not satisfied
                temp=DCTrgb(k1(i)+4,k2(j)+3);
                DCTrgb(k1(i)+4,k2(j)+3)=DCTrgb(k1(i)+5,k2(j)+2);
                DCTrgb(k1(i)+5,k2(j)+2)=temp;
            end
        else
            if DCTrgb(k1(i)+5,k2(j)+2)<DCTrgb(k1(i)+4,k2(j)+3)
                temp=DCTrgb(k1(i)+4,k2(j)+3);
                DCTrgb(k1(i)+4,k2(j)+3)=DCTrgb(k1(i)+5,k2(j)+2);
                DCTrgb(k1(i)+5,k2(j)+2)=temp;
            end
        end
        if DCTrgb(k1(i)+5,k2(j)+2)>DCTrgb(k1(i)+4,k2(j)+3)  %use the robust coefficent: alpha
            DCTrgb(k1(i)+4,k2(j)+3)=DCTrgb(k1(i)+4,k2(j)+3)-alpha;
        else
            DCTrgb(k1(i)+5,k2(j)+2)=DCTrgb(k1(i)+5,k2(j)+2)-alpha;
        end
    end
end

data=blkproc(DCTrgb,[8 8],'P1 * x * P2',T',T);  %inverse DCT
result=data0;
result(:,:,1)=data; %put the changed layer back

%subplot(1,1,1),imshow(result);title('image with watermark');

imwrite(result,'15300240004_hiddenimage.bmp','bmp');

