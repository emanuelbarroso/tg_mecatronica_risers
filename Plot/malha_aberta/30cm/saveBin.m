load('Dados_exp.mat')
y = real(Y);
%t

fileID = fopen('position.bin','wb');

for i=1:4:size(y,2)
    fwrite(fileID,t(i),'double');
    fwrite(fileID,y(i), 'double');
end

fclose(fileID);