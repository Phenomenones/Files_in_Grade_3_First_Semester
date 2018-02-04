%Designed by Ao Wang, 15300240004

clc;
clear;

%DCT watermark extraction

RGB=imread('15300240004_hiddenimage.bmp');
hidden_image=RGB(:,:,1);
new_dct=dct2(hidden_image);%get the DCT image of the image with watermark

hide_matrix_length=55;%change when needed

[sizea,sizeb] = size(hidden_image);
block_num=(sizea/8)*(sizeb/8);%record the number of 8*8 blocks


row_array=[];
for i=1:(sizea/8)
    row_array(i)=8;
end

colum_array=[];
for i=1:(sizeb/8)
    colum_array(i)=8;
end

new_block_matrix = mat2cell(new_dct,row_array,colum_array);

%just like hiding
list=[];
for i=(sizea/8):-1:1
    for j=(sizeb/8):-1:1
        num=0;
        if (sizea/8-i)*(sizeb/8)+sizeb/8-j+1<=hide_matrix_length
            iter=(sizea/8-i)*(sizeb/8)+sizeb/8-j+1;
            temp_mat=new_block_matrix{i,j};
            
            if temp_mat(8,7)>temp_mat(5,7)
                num=bitor(num,1);
            end
            
            if temp_mat(7,6)>temp_mat(7,7)
                num=bitor(num,2);
            end
            
            if temp_mat(8,6)>temp_mat(8,8)
                num=bitor(num,4);
            end
            
            if temp_mat(6,3)>temp_mat(5,4)
                num=bitor(num,8);
            end
            
            if temp_mat(5,2)>temp_mat(4,3)
                num=bitor(num,16);
            end
            
            if temp_mat(3,4)>temp_mat(1,5)
                num=bitor(num,32);
            end
            
            if temp_mat(3,1)>temp_mat(4,1)
                num=bitor(num,64);
            end
            
            if temp_mat(2,1)>temp_mat(2,2)
                num=bitor(num,128);
            end
            list=[list;num];
        end 
    end
end

filename = 'output.txt';
fid = fopen(filename,'w');
fwrite(fid, list, 'uchar');
%save the extracted watermark to output.txt
fclose(fid);

            