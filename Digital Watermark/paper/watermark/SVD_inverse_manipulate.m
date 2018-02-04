%Designed by Wang Ao, 15300240004

function mat = SVD_inverse_manipulate (mark_cell_mat,container_cell_mat,alpha,U_mat,V_mat)
%mark_cell_mat is the container with watermark
%container_cell_mat is the original container
%alpha is the robust coefficient
[sizea,sizeb]=size(mark_cell_mat);  %8*8
mat=mark_cell_mat;

for i =1:sizea
    for j =1:sizeb
        mark_tmp=mark_cell_mat{i,j};
        container_tmp=container_cell_mat{i,j};
        [U1,S1,V1] = svd(mark_tmp);
        [U2,S2,V2] = svd(container_tmp);
        [a,b]=size(S1);
        for m =1:a
            for n =1:b
               S2(m,n) =  (S1(m,n) - S2(m,n))/alpha;
            end
        end
        tmp=U_mat{i,j}*S2*V_mat{i,j}';
        mat{i,j}=tmp;
    end
end
mat=cell2mat(mat);%transfer to matrix