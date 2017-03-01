function [ path1,direction ] = makeDecision(G,snakeHead,food,legend )
    %MAKEDECISION Summary of this function goes here
    %   Detailed explanation goes here
    
    [path1,~] = shortestpath(G,(strcat(legend(snakeHead(1)),legend(snakeHead(2)))),(strcat(legend(food(1)),legend(food(2)))));
    %highlight(p,path1,'EdgeColor','g');
    %[path2,d] = shortestpath(G,(strcat(legend(snakeHead(1)),legend(snakeHead(2)))),(strcat(legend(food(1)),legend(food(2)))),'Method','unweighted');
    %highlight(p,path2,'EdgeColor','r');
    
    
    if(~isempty(path1))
        nextMove = char(path1(2));
        if(nextMove == strcat(legend(snakeHead(1)+1),legend(snakeHead(2))))
            direction = 'North';
        elseif(nextMove == strcat(legend(snakeHead(1)-1),legend(snakeHead(2))))
            direction = 'South';
        elseif(nextMove == strcat(legend(snakeHead(1)),legend(snakeHead(2)+1)))
            direction = 'East';
        elseif(nextMove == strcat(legend(snakeHead(1)),legend(snakeHead(2)-1)))
            direction = 'West';
        end
    else
        direction = 'North';
        disp('There was no safe path to food');
    end
    
    
    
end