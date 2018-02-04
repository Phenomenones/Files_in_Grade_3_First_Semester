function result=jpgandalpha(test,msg)

quality=0:10:100;
alpha=0:0.3:3;%change
result=zeros([max(size(alpha)) max(size(quality))]);

resultr=0;
resultc=0;

for a = alpha
    resultr=resultr+1;
    [count,message,hideresult] = hidedctadv(test,'temp.jpg',msg,2333,a);
    resultc=0;
    different=0;
    for q=quality
        resultc=resultc+1;
        imwrite(hideresult,'temp.jpg','jpg','quality',q);
        msgextract = extractdctadv('temp.jpg','temp.txt',2333,count);
        for i=1:count
            if message(i,1) ~= msgextract(1,i);
                different =different+1;
            end
        end
        result(resultr,resultc)=different/count;
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










