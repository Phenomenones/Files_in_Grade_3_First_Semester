function result=jpgandalpha(test,msg)

quality=0:10:100;   %different compress ratio
alpha=0:0.1:1;  %different robust coefficent
result=zeros([max(size(alpha)) max(size(quality))]);

resultr=0;
resultc=0;

for a = alpha
    resultr=resultr+1;
    [count,message,hideresult,aa,bb] = hidedctadv(test,msg,a);
    resultc=0;
    different=0;
    for q=quality
        resultc=resultc+1;
        imwrite(hideresult,'temp.jpg','jpg','quality',q);
        msgextract = extractdctadv('temp.jpg',count,aa,bb);
        for i=1:count
            if message(i,1) ~= msgextract(1,i); %recording how many bits are different from the original image
                different =different+1;
            end
        end
        result(resultr,resultc)=different/count;    %get the different ratio
        different=0;
    end
    
    disp(['Finished ',int2str(resultr),' test, please wait...']);
end

for i=1:11%change
    plot(quality,result(i,:));
    hold on;
end

xlabel('Compression Rate');
ylabel('Differential Rate');

title('The test on the impact of alpha');










