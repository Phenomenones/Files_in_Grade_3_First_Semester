clc;
clear;
o='/Users/apple/Desktop/lab/djh.wav';

fid=fopen(o,'r');                
oa=fread(fid,inf,'uint16');
fclose(fid);

wav=oa;
[a,b]=size(wav);

for i=22:a
    for j =1:9
        wav(i)=bitset(wav(i),j,0);
    end
end

figure;
subplot(2,1,1);plot(oa);title('Original wav');
subplot(2,1,2),plot(wav);title('Cleared wav');
fid = fopen('clear.wav', 'wb');
fwrite(fid,wav,'uint16');
fclose(fid);

[x,Fs]=audioread('clear.wav');
sound(x,11025);