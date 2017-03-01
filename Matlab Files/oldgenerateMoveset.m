function [ G ] = generateMoveset( currentFrame,weights,n,legend)
%GENERATEMOVESET Summary of this function goes here
%   Detailed explanation goes here

G = graph();
for row = (2:n+1)
    for col= (2:n+1)
        try
            if(currentFrame(row,col)==0 && currentFrame(row+1,col)==0)
                G = addedge(G,strcat(legend(int16(row)),legend(int16(col))),strcat(legend(int16(row+1)),legend(int16(col))),weights(row,col)*.5 + weights(row+1,col)*.5);
            end
        end
        try
            if(currentFrame(row,col)==0 && currentFrame(row-1,col)==0)
                G = addedge(G,strcat(legend(int16(row)),legend(int16(col))),strcat(legend(int16(row-1)),legend(int16(col))),weights(row,col)*.5 + weights(row-1,col)*.5);
            end
        end
        try
            if(currentFrame(row,col)==0 && currentFrame(row,col+1)==0)
                G = addedge(G,strcat(legend(int16(row)),legend(int16(col))),strcat(legend(int16(row)),legend(int16(col+1))),weights(row,col)*.5 + weights(row,col+1)*.5);
            end
        end
        try
            if(currentFrame(row,col)==0 && currentFrame(row,col-1)==0)
                G = addedge(G,strcat(legend(int16(row)),legend(int16(col))),strcat(legend(int16(row)),legend(int16(col-1))),weights(row,col)*.5 + weights(row,col-1)*.5);
            end
        end
    end
end

end