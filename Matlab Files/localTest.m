function [dead,snakeHead,snakeBody,food, barriers ] = localTest( currentFrame,direction,snakeHead,snakeBody,barriers,food,n,turn)
    %LOCALTEST Summary of this function goes here
    %   Detailed explanation goes here
    % https://www.mathworks.com/help/matlab/ref/circshift.html
    %
    %[snakeHead,snakeBody,food,barriers] = localTest(currentFrame,direction,snakeHead,snakeBody,food,barriers);
    % snakehead[row,col]
    dead = 0;
    
    switch direction
        case 'North'
            newSnakeHeadLocation = [snakeHead(1)+1, snakeHead(2)];
        case 'South'
            newSnakeHeadLocation = [snakeHead(1)-1, snakeHead(2)];
        case 'East'
            newSnakeHeadLocation = [snakeHead(1), snakeHead(2)+1];
        case 'West'
            newSnakeHeadLocation = [snakeHead(1), snakeHead(2)-1];
        otherwise
            fprintf('I got a bad switch case');
            
    end
    %snakeHead = newSnakeHeadLocation;
    fprintf('Head:[%d,%d]\n',newSnakeHeadLocation(1),newSnakeHeadLocation(2));
    fprintf('Food:[%d,%d]\n',food(1),food(2));
    
    if(currentFrame(newSnakeHeadLocation(1),newSnakeHeadLocation(2))==1)
        dead = 1;
    end
    
    if(newSnakeHeadLocation(1)~=food(1) || newSnakeHeadLocation(2)~=food(2))
        snakeBody = snakeBody(1:end-1,:);     % trim one off the end
        snakeBody=cat(1,snakeHead,snakeBody); % add one on the top
        snakeHead = newSnakeHeadLocation;     % move the head
    else
        fprintf('Apperently the newHeadLocation is the same as the food\n');
        fprintf('->Head:[%d,%d]\n',newSnakeHeadLocation(1),newSnakeHeadLocation(2));
        fprintf('->Food:[%d,%d]\n',food(1),food(2));
        snakeBody=cat(1,snakeHead,snakeBody);
        snakeHead = newSnakeHeadLocation;
        oldFood = food;
        flag = 1;
        watchdog = 0;
        while flag
            watchdog = watchdog+1;
           food = randi(n+2,1,2);
           if(currentFrame(food(1),food(2))~=1 && food(1)~=oldFood(1) &&food(2)~=oldFood(2)&&snakeHead(1)~=food(1)&&snakeHead(2)~=food(2))
               disp('there is a new food at')
               disp(food)
               flag = 0;
           end
           if watchdog>100
               flag = 0;
               dead = 1;
               disp('There is no more room to put food')
           end
           
        end
    end
    watchdog = 0;
    if(mod(turn,9)==0 && watchdog<100)
        newBarrier = randi(n+2,1,2);
        if(currentFrame(newBarrier(1),newBarrier(2))~= 1 && snakeHead(1)~=newBarrier(1) && snakeHead(2)~=newBarrier(2))
         barriers = cat(1,newBarrier,barriers);
        end
         
    end
    
        
    
    
end