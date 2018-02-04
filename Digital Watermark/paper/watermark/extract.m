%Designed by Wang Ao, 15300240004

function [LL,HL,LH,HH] = extract(original_container,container,encrypt_mat,a,b,n,alpha1,alpha2,alpha3,U_mat,V_mat)

original_image=imread(original_container);
image=imread(container);

%3-DWT decomposition, original container
[C,L]=wavedec2(original_image,3,'db1');
[HL3,LH3,HH3]=detcoef2('all',C,L,3);
LL3=appcoef2(C,L,'db1',3);

%3-DWT decomposition, container with watermark
[Cw,Lw]=wavedec2(image,3,'db1');
[HL3w,LH3w,HH3w]=detcoef2('all',Cw,Lw,3);
LL3w=appcoef2(Cw,Lw,'db1',3);

%transpose
HL3=HL3';
LH3=LH3';
LL3=LL3';
HL3w=HL3w';
LH3w=LH3w';
LL3w=LL3w';

%partition
[sizea,sizeb] = size(LL3);
row_array=[];
for i=1:(sizea/8)
    row_array(i)=8;
end
colum_array=[];
for i=1:(sizeb/8)
    colum_array(i)=8;
end

HL3_block_matrix = mat2cell(HL3,row_array,colum_array);
LH3_block_matrix = mat2cell(LH3,row_array,colum_array);
LL3_block_matrix = mat2cell(LL3,row_array,colum_array);

HL3w_block_matrix = mat2cell(HL3w,row_array,colum_array);
LH3w_block_matrix = mat2cell(LH3w,row_array,colum_array);
LL3w_block_matrix = mat2cell(LL3w,row_array,colum_array);

%use SVD to extract watermarks
%using U matrix and V matrix recorded in hide procedure
HLmat=SVD_inverse_manipulate(HL3w_block_matrix,HL3_block_matrix,alpha1,U_mat,V_mat);
LHmat=SVD_inverse_manipulate(LH3w_block_matrix,LH3_block_matrix,alpha2,U_mat,V_mat);
LLmat=SVD_inverse_manipulate(LL3w_block_matrix,LL3_block_matrix,alpha3,U_mat,V_mat);

%transfer float to interger
HLmat=im2bw(HLmat,0.5);
LHmat=im2bw(LHmat,0.5);
LLmat=im2bw(LLmat,0.5);

%use xor to decrypt
HL=bitxor(HLmat,encrypt_mat);
LH=bitxor(LHmat,encrypt_mat);
LL=bitxor(LLmat,encrypt_mat);

%inverse Arnold shuffle
%take out the watermarks in LL, HL and LH
[h,w]=size(LL);
N=h;
imgn=HL;
img=imgn;
for i=1:n
    for y=1:h
        for x=1:w            
            xx=mod((a*b+1)*(x-1)-b*(y-1),N)+1;
            yy=mod(-a*(x-1)+(y-1),N)+1  ;        
            imgn(yy,xx)=img(y,x);                   
        end
    end
    img=imgn;
end
HL=imgn;
%imshow(HL,[]);

imgn=LH;
img=imgn;
for i=1:n
    for y=1:h
        for x=1:w            
            xx=mod((a*b+1)*(x-1)-b*(y-1),N)+1;
            yy=mod(-a*(x-1)+(y-1),N)+1  ;        
            imgn(yy,xx)=img(y,x);                   
        end
    end
    img=imgn;
end
LH=imgn;
%imshow(LH,[]);

imgn=LL;
img=imgn;
for i=1:n
    for y=1:h
        for x=1:w            
            xx=mod((a*b+1)*(x-1)-b*(y-1),N)+1;
            yy=mod(-a*(x-1)+(y-1),N)+1  ;        
            imgn(yy,xx)=img(y,x);                   
        end
    end
    img=imgn;
end
LL=imgn;
%imshow(LL,[]);

%use the three watermarks to calcuate the forth
%if two of the three bits are 1, then the forth has the bit 1
HH=zeros(size(LL));
%[sizea,sizeb] = size(LL3);
for i =1:sizea
    for j =1:sizeb
        tmp=LL(i,j)+LH(i,j)+HL(i,j);
        if tmp>=2
            HH(i,j)=1;
        end
    end
end
%imshow(HH);
%return the four watermarks
