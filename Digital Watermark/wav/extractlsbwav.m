function watermark_image = extractlsbwav(a,b,wav_with_mark,bit)

num=2^(bit-1);  %being used to set the changed bit of the byte
watermark_image=zeros(a,b);

for i =1:a
   for j =1:b
      watermark_image(i,j)= num;    %initialized to num
   end
end

for i=0:a-1
    for j=1:b
        iter=num;
        iter=bitand(iter,wav_with_mark(i*b+j+44));  %get the required bit in the wav file
        watermark_image(i*b+j)= bitand(watermark_image(i*b+j),iter);    %put the bit in the image
    end
end

imwrite(watermark_image,'watermark_image.bmp','bmp');