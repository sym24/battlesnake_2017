function [ afterFrame ] = addBarriers(beforeFrame, toAdd )
    %ADDBARRIERS Summary of this function goes here
    %   Detailed explanation goes here
    
    afterFrame = beforeFrame;
    %toAdd = [3 4; 3 7; 8 4];
    %barriers = [];
    for i = (1:length(toAdd))
        afterFrame(toAdd(i,1),toAdd(i,2)) = 1;
    end
end