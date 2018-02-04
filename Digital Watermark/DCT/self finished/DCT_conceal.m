%Designed by Ao Wang, 15300240004

clc;
clear;
alpha=3;%use to control the robustness of the watermark
RGB=imread('Lenna.bmp');
gray_image=RGB(:,:,1);%turn the chromatic image to gray
DCT_image=dct2(gray_image);%implement the DCT conversion

%DCT watermark hidding
hide_info=fopen('hidefile.txt','r','n','utf8');
[hide_matrix,count]=fread(hide_info);%read the secret info to hide_matrix
fclose(hide_info);
[sizex,sizey] = size(hide_matrix);
hide_matrix_length = sizex *sizey;%record the length of hide_matrix

[sizea,sizeb] = size(DCT_image);
block_num=(sizea/8)*(sizeb/8);%record the number of 8*8 blocks

row_array=[];
for i=1:(sizea/8)
    row_array(i)=8;
end

colum_array=[];
for i=1:(sizeb/8)
    colum_array(i)=8;
end

block_matrix = mat2cell(DCT_image,row_array,colum_array);
%partitioning the image to 8*8 blocks

%use every 8*8 block to conceal a byte(8 bits)
res=[];
for i=(sizea/8):-1:1
    row=[];
    for j=(sizeb/8):-1:1
        if (sizea/8-i)*(sizeb/8)+sizeb/8-j+1<=hide_matrix_length
            iter=(sizea/8-i)*(sizeb/8)+sizeb/8-j+1;
            num=hide_matrix(iter);
            temp_mat=block_matrix{i,j};
            
            %the first bit: (8,7)>(5,7)when 1, exchange if not satisfied;
            %0 otherwise
            if bitget(num,1)==1
                if temp_mat(8,7)<temp_mat(5,7)
                    [temp_mat(8,7) temp_mat(5,7)] = deal(temp_mat(5,7),temp_mat(8,7));
                end
            else
                if temp_mat(8,7)>temp_mat(5,7)
                    [temp_mat(8,7) temp_mat(5,7)] = deal(temp_mat(5,7),temp_mat(8,7));
                end
            end
            %to make the small one smaller
            if temp_mat(8,7)>temp_mat(5,7)
                temp_mat(5,7)=temp_mat(5,7)-alpha;
            else
                temp_mat(8,7)=temp_mat(8,7)-alpha;
            end
                
            
            %the second bit: (7,6)>(7,7)when 1, exchange if not satisfied;
            %0 otherwise
            if bitget(num,2)==1
                if temp_mat(7,6)<temp_mat(7,7)
                    [temp_mat(7,6) temp_mat(7,7)] = deal(temp_mat(7,7),temp_mat(7,6));
                end
            else
                if temp_mat(7,6)>temp_mat(7,7)
                    [temp_mat(7,6) temp_mat(7,7)] = deal(temp_mat(7,7),temp_mat(7,6));
                end
            end
            %to make the small one smaller
            if temp_mat(7,6)>temp_mat(7,7)
                temp_mat(7,7)=temp_mat(7,7)-alpha;
            else
                temp_mat(7,6)=temp_mat(7,6)-alpha;
            end
            
            %the third bit: (8,6)>(8,8)when 1, exchange if not satisfied;
            %0 otherwise
            if bitget(num,3)==1
                if temp_mat(8,6)<temp_mat(8,8)
                    [temp_mat(8,6) temp_mat(8,8)] = deal(temp_mat(8,8),temp_mat(8,6));
                end
            else
                if temp_mat(8,6)>temp_mat(8,8)
                    [temp_mat(8,6) temp_mat(8,8)] = deal(temp_mat(8,8),temp_mat(8,6));
                end
            end
            %to make the small one smaller
            if temp_mat(8,6)>temp_mat(8,8)
                temp_mat(8,8)=temp_mat(8,8)-alpha;
            else
                temp_mat(8,6)=temp_mat(8,6)-alpha;
            end
            
            %the fourth bit: (6,3)>(5,4)when 1, exchange if not satisfied;
            %0 otherwise
            if bitget(num,4)==1
                if temp_mat(6,3)<temp_mat(5,4)
                    [temp_mat(6,3) temp_mat(5,4)] = deal(temp_mat(5,4),temp_mat(6,3));
                end
            else
                if temp_mat(6,3)>temp_mat(5,4)
                    [temp_mat(6,3) temp_mat(5,4)] = deal(temp_mat(5,4),temp_mat(6,3));
                end
            end
            %to make the small one smaller
            if temp_mat(6,3)>temp_mat(5,4)
                temp_mat(5,4)=temp_mat(5,4)-alpha;
            else
                temp_mat(6,3)=temp_mat(6,3)-alpha;
            end
            
            %the fifth bit: (5,2)>(4,3)when 1, exchange if not satisfied;
            %0 otherwise
            if bitget(num,5)==1
                if temp_mat(5,2)<temp_mat(4,3)
                    [temp_mat(5,2) temp_mat(4,3)] = deal(temp_mat(4,3),temp_mat(5,2));
                end
            else
                if temp_mat(5,2)>temp_mat(4,3)
                    [temp_mat(5,2) temp_mat(4,3)] = deal(temp_mat(4,3),temp_mat(5,2));
                end
            end
            %to make the small one smaller
            if temp_mat(5,2)>temp_mat(4,3)
                temp_mat(4,3)=temp_mat(4,3)-alpha;
            else
                temp_mat(5,2)=temp_mat(5,2)-alpha;
            end
            
            %the sixth bit: (3,4)>(1,5)when 1, exchange if not satisfied;
            %0 otherwise
            if bitget(num,6)==1
                if temp_mat(3,4)<temp_mat(1,5)
                    [temp_mat(3,4) temp_mat(1,5)] = deal(temp_mat(1,5),temp_mat(3,4));
                end
            else
                if temp_mat(3,4)>temp_mat(1,5)
                    [temp_mat(3,4) temp_mat(1,5)] = deal(temp_mat(1,5),temp_mat(3,4));
                end
            end
            %to make the small one smaller
            if temp_mat(3,4)>temp_mat(1,5)
                temp_mat(1,5)=temp_mat(1,5)-alpha;
            else
                temp_mat(3,4)=temp_mat(3,4)-alpha;
            end
            
            %the seventh bit: (3,1)>(4,1)when 1, exchange if not satisfied;
            %0 otherwise
            if bitget(num,7)==1
                if temp_mat(3,1)<temp_mat(4,1)
                    [temp_mat(3,1) temp_mat(4,1)] = deal(temp_mat(4,1),temp_mat(3,1));
                end
            else
                if temp_mat(3,1)>temp_mat(4,1)
                    [temp_mat(3,1) temp_mat(4,1)] = deal(temp_mat(4,1),temp_mat(3,1));
                end
            end
            %to make the small one smaller
            if temp_mat(3,1)>temp_mat(4,1)
                temp_mat(4,1)=temp_mat(4,1)-alpha;
            else
                temp_mat(3,1)=temp_mat(3,1)-alpha;
            end
            
            %the eighth bit: (2,1)>(2,2)when 1, exchange if not satisfied;
            %0 otherwise
            if bitget(num,8)==1
                if temp_mat(2,1)<temp_mat(2,2)
                    [temp_mat(2,1) temp_mat(2,2)] = deal(temp_mat(2,2),temp_mat(2,1));
                end
            else
                if temp_mat(2,1)>temp_mat(2,2)
                    [temp_mat(2,1) temp_mat(2,2)] = deal(temp_mat(2,2),temp_mat(2,1));
                end
            end
            %to make the small one smaller
            if temp_mat(2,1)>temp_mat(2,2)
                temp_mat(2,2)=temp_mat(2,2)-alpha;
            else
                temp_mat(2,1)=temp_mat(2,1)-alpha;
            end
                        
            row=[temp_mat,row];
        else
            row=[block_matrix{i,j},row];
        end
    end
    res=[row;res];
end

hidden_image=idct2(res);
%use the inverse DCT conversion to get the image with watermark
res_image=DCT_image;
res_image(:,:,1)=hidden_image/256;
res_image(:,:,2)=RGB(:,:,2);
res_image(:,:,2)=res_image(:,:,2)/256;
res_image(:,:,3)=RGB(:,:,3);
res_image(:,:,3)=res_image(:,:,3)/256;
%manipulate the RGB of result image to get it correct

subplot(2,2,1),imshow(RGB);title('original image');
subplot(2,2,2),imshow(res_image);title('image with watermark');
%don't forget to divide 256!!!!!!!!!!
subplot(2,2,3),imshow(DCT_image);title('original DCT image');
subplot(2,2,4),imshow(res);title('DCT image with watermark');

imwrite(res_image,'15300240004_hiddenimage.bmp','bmp');
%save the image

