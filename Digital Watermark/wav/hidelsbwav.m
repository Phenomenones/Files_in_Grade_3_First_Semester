%the wav file is 44144 bytes long, with 44100 bytes usable
%the bmp file is 40000 bits
%hide in the lowest bit of every byte of the wav file

function[a,b,wav_with_mark,bit] = hidelsbwav(wav,image,bit)

fid=fopen(wav,'r');                
oa=fread(fid,inf,'uint8');
fclose(fid);
wav_with_mark=oa;   %oa is the original wav file, wav_with_mark is the changed one

pic_data=imread(image);
[a,b]=size(pic_data);

pic_data=pic_data(:);   %array
[len,tmp]=size(pic_data);

for i=45:45+len-1
   	wav_with_mark(i)=bitset(wav_with_mark(i),bit,pic_data(i-44));
end

figure;
subplot(2,1,1);plot(oa);title('Original wav');
subplot(2,1,2),plot(wav_with_mark);title('wav With Watermark');
fid = fopen('watermarked.wav', 'wb');
fwrite(fid,wav_with_mark,'uint8');
fclose(fid);
