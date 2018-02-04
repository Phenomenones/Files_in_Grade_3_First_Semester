function result=extractdctadv(image,msg,key,count)
data0=imread(image);
data0=double(data0)/255;
data=data0(:,:,1);

T=dctmtx(8);
DCTcheck=blkproc(data,[8 8],'P1 * x * P2',T,T');
[row,col]=size(DCTcheck);
row=floor(row/8);
col=floor(col/8);
a=zeros([row col]);


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

%start extracting

list=[];
result=[];
for i =1:count
    if DCTcheck(k1(i)+6,k2(i)+3)<=DCTcheck(k1(i)+3,k2(i)+5)
        result(1,i)=0;
    else
        result(1,i)=1;
    end
end

res=[];
for i=1:8:count
    num=0;
    for j=0:7
        if result(i+j)==1
            num=bitor(num,2^(j));
        end
    end
    res=[res;num];
end

fid=fopen(msg,'a');

fwrite(fid, res, 'uchar');

fclose(fid);



