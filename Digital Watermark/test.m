clc;
% watermark conceal
carrier=imread('Lenna.bmp'); %input carrier
watermark=imread('woman.bmp'); %input watermark

c_tmp=bitand(carrier,240); % 240==(2)11110000
%set the last 4 bits of carrier to 0
w_tmp=bitshift(watermark,-4); 
%shift the first 4 bits of watermark to the right

res=bitor(c_tmp,w_tmp); %overlay two pictures
imwrite(res,'res.bmp','bmp');  

%watermark extraction
wm_extract=bitand(res,15);% 15=(2)00001111
wm_extract=bitshift(wm_extract,4);
%shift the last 4 bits of the picture to the left

subplot(2,2,1),imshow(carrier),title('carrier image');
subplot(2,2,2),imshow(watermark),title('watermark image');
subplot(2,2,3),imshow(res),title('carrier with hidden watermark');
subplot(2,2,4),imshow(wm_extract),title('extracted watermark');
