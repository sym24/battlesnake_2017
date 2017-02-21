function [ weights ] = generateDanger( currentFrame,Walls,n)
%GENERATEDANGER Summary of this function goes here
%   Detailed explanation goes here

weights = zeros(size(currentFrame));
for row = (2:n+1)
    for col = (2:n+1)
        weights(row,col) = currentFrame(row,col)*.5+.25+ currentFrame(row+1,col)*.5+currentFrame(row-1,col)*.5+currentFrame(row,col+1)*.5+currentFrame(row,col-1)*.5;
    end
end
weights = weights+Walls;

end