function result=extractdctadv(image,count,aa,bb)
data0=imread(image);
data0=double(data0)/255;
data=data0(:,:,1);

T=dctmtx(8);
DCTcheck=blkproc(data,[8 8],'P1 * x * P2',T,T');
[row,col]=size(DCTcheck);
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

%start extracting

result=zeros(1,count);
for i =1:row
    for j =1:col
        if DCTcheck(k1(i)+5,k2(j)+2)<=DCTcheck(k1(i)+4,k2(j)+3) %use (5,2) and (4,3)
            result(1,(i-1)*col+j)=0;
        else
            result(1,(i-1)*col+j)=1;
        end
    end
end

mark_image=zeros(aa,bb);
for i=1:aa
    for j=1:bb
        mark_image(i,j)=result(1,(i-1)*bb+j);
    end
end

imwrite(mark_image,'watermark.bmp','bmp');


