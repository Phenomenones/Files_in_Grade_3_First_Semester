%Designed by Wang Ao, 15300240004

function[image_with_mark,encrypt_mat,U_mat,V_mat] = hide(a,b,n,container,watermark,k,initial_value,alpha1,alpha2,alpha3)
%a and b are the coefficients of Arnold disorganise
%n is the iteration times to Arnold disorganise
%initial_value is to start the Chebyshev chaos
%k is the starting key of encryption
%alphas are the robust coefficients of the enbedding in the SVD decomposition

image=imread(container);
img=imread(watermark);

%start Arnold disorganise,imgn is th result
[h,w]=size(img);

N=h;
imgn=zeros(h,w);
for i=1:n
    for y=1:h
        for x=1:w           
            xx=mod((x-1)+b*(y-1),N)+1;
            yy=mod(a*(x-1)+(a*b+1)*(y-1),N)+1;        
            imgn(yy,xx)=img(y,x);                
        end
    end
    img=imgn;
end
%imshow(imgn);

len=(h*w)/4+k;

%start transfering chaos array to 2 dimension matrix
chaos_lis=chaos(1,initial_value,len);
[tmp, chaos_lis_len]=size(chaos_lis);

lis=[];
for i = 1:chaos_lis_len
    if 0.875<= chaos_lis(i) && chaos_lis(i)<=1.0
        lis=[lis 1 1 1 1];
        continue;
    end
    if 0.75<= chaos_lis(i) && chaos_lis(i)<=0.875
        lis=[lis 1 1 1 0];
        continue;
    end
    if 0.625<= chaos_lis(i) && chaos_lis(i)<=0.75
        lis=[lis 1 1 0 1];
        continue;
    end
    if 0.5<= chaos_lis(i) && chaos_lis(i)<=0.625
        lis=[lis 1 1 0 0];
        continue;
    end
    if 0.375<= chaos_lis(i) && chaos_lis(i)<=0.5
        lis=[lis 1 0 1 1];
        continue;
    end
    if 0.25<= chaos_lis(i) && chaos_lis(i)<=0.375
        lis=[lis 1 0 1 0];
        continue;
    end
    if 0.125<= chaos_lis(i) && chaos_lis(i)<=0.25
        lis=[lis 1 0 0 1];
        continue;
    end
    if 0.0<= chaos_lis(i) && chaos_lis(i)<=0.125
        lis=[lis 1 0 0 0];
        continue;
    end
    if -0.125<= chaos_lis(i) && chaos_lis(i)<=0.0
        lis=[lis 0 1 1 1];
    end
    if -0.25<= chaos_lis(i) && chaos_lis(i)<=-0.125
        lis=[lis 0 1 1 0];
        continue;
    end
    if -0.375<= chaos_lis(i) && chaos_lis(i)<=-0.25
        lis=[lis 0 1 0 1];
        continue;
    end
    if -0.5<= chaos_lis(i) && chaos_lis(i)<=-0.375
        lis=[lis 0 1 0 0];
        continue;
    end
    if -0.625<= chaos_lis(i) && chaos_lis(i)<=-0.5
        lis=[lis 0 0 1 1];
        continue;
    end
    if -0.75<= chaos_lis(i) && chaos_lis(i)<=-0.625
        lis=[lis 0 0 1 0];
        continue;
    end
    if -0.875<= chaos_lis(i) && chaos_lis(i)<=-0.75
        lis=[lis 0 0 0 1];
        continue;
    end
    if -1.0<= chaos_lis(i) && chaos_lis(i)<=-0.875
        lis=[lis 0 0 0 0];
        continue;
    end
end

lis=lis(1:h*w);
encrypt_mat=reshape(lis,h,w);
encrypt_mark=bitxor(imgn,encrypt_mat);
%imshow(encrypt_mark);

%start embedding
%3-DWT
image_with_mark=[];
[C,L]=wavedec2(image,3,'db1');
[HL3,LH3,HH3]=detcoef2('all',C,L,3);
LL3=appcoef2(C,L,'db1',3);

%partition
[sizea,sizeb] = size(encrypt_mark);
row_array=[];
for i=1:(sizea/8)
    row_array(i)=8;
end
colum_array=[];
for i=1:(sizeb/8)
    colum_array(i)=8;
end

encrypt_mark_block_matrix = mat2cell(encrypt_mark,row_array,colum_array);
HL3_block_matrix = mat2cell(HL3,row_array,colum_array);
LH3_block_matrix = mat2cell(LH3,row_array,colum_array);
LL3_block_matrix = mat2cell(LL3,row_array,colum_array);

%SVD decomposition and embedding
[HLmat,U_mat,V_mat]=SVD_manipulate(encrypt_mark_block_matrix,HL3_block_matrix,alpha1);
[LHmat,U_mat,V_mat]=SVD_manipulate(encrypt_mark_block_matrix,LH3_block_matrix,alpha2);
[LLmat,U_mat,V_mat]=SVD_manipulate(encrypt_mark_block_matrix,LL3_block_matrix,alpha3);

[p,q]=size(LLmat);

%transpose to fit in inverse DWT
HLmat=HLmat';
LHmat=LHmat';
LLmat=LLmat';

%transfer from matrix to array to change C
ll_lis=[];
for i =1:p
    tmp=LLmat(i,:);
    ll_lis=[ll_lis,tmp];
end
hl_lis=[];
for i =1:p
    tmp=HLmat(i,:);
    hl_lis=[hl_lis,tmp];
end
lh_lis=[];
for i =1:p
    tmp=LHmat(i,:);
    lh_lis=[lh_lis,tmp];
end

size_c=size(C);
tmplis1=[ll_lis,hl_lis,lh_lis];
tmplis2=C(1,12289:size_c(2));%take part of C out
tmplis=[tmplis1,tmplis2];

%inverse DWT
image_with_mark=waverec2(tmplis,L,'db1');

image_with_mark=image_with_mark/255;
%imshow(image_with_mark);
