function [ out ] = generateMovesetV1( currentFrame,weights,n,legendMatrix,G)
%GENERATEMOVESET Summary of this function goes here
%   Detailed explanation goes here



largeN = n+2;
for row = (1:largeN)
    for col= (1:n+1)
        disp "Row " + 
        G = rmedge(G,row+col,(row+largeN)+col);
        G = rmedge(G,row+col,(row-largeN)+col);
        G = rmedge(G,row+col,(row)+col+1);
        G = rmedge(G,row+col,(row)+col-1);
    end
end


for row = (1:largeN)
    for col= (1:n+1)
        if(currentFrame(row,col)==0 && currentFrame(row+1,col)==0)
            G = addedge(G,row*100+col,(row+1)*100+col,weights(row,col)*.5+weights(row+1,col));
            %G = addedge(G,strcat(legend(int16(row)),legend(int16(col))),strcat(legend(int16(row+1)),legend(int16(col))),weights(row,col)*.5 + weights(row+1,col)*.5);
        end
        
        if(currentFrame(row,col)==0 && currentFrame(row-1,col)==0)
            G = addedge(G,row*100+col,(row-1)*100+col,weights(row,col)*.5+weights(row-1,col));
            %G = addedge(G,strcat(legend(int16(row)),legend(int16(col))),strcat(legend(int16(row-1)),legend(int16(col))),weights(row,col)*.5 + weights(row-1,col)*.5);
        end
        
        
        if(currentFrame(row,col)==0 && currentFrame(row,col+1)==0)
            G = addedge(G,row*100+col,row*100+col+1,weights(row,col)*.5+weights(row,col+1));
            %a(index) = legendMatrix(row,col);
            %b(index) = legendMatrix(row,col+1);
            %w(index) = 0.5*(weights(row,col)+ weights(row+1,col));
            %index = index + 1;
            %G = addedge(G,strcat(legend(int16(row)),legend(int16(col))),strcat(legend(int16(row)),legend(int16(col+1))),weights(row,col)*.5 + weights(row,col+1)*.5);
        end
        
        
        if(currentFrame(row,col)==0 && currentFrame(row,col-1)==0)
            G = addedge(G,row*100+col,row*100+col-1,weights(row,col)*.5+weights(row,col-1));
            %a(index) = legendMatrix(row,col-1);
            %b(index) = legendMatrix(row,col);
            %w(index) = 0.5*(weights(row,col)+ weights(row+1,col));
            %index = index + 1;
            %G = addedge(G,strcat(legend(int16(row)),legend(int16(col))),strcat(legend(int16(row)),legend(int16(col-1))),weights(row,col)*.5 + weights(row,col-1)*.5);
        end
        
    end
end
out = G;

end