%% Initialize everything
% this is the stuff that will only get made once.

n = 17;
legend = ['~';'a';'b';'c';'d';'e';'f';'g';'h';'i';'j';'k';'l';'m';'n';'o';'p';'q';'r';'s';'t';'u';'v';'w';'x';'y';'z'];
legendString = '~abcdefghijklmnopqrstuvwxyz';
legendMatrix = {};
for row = 1:n+2
    for col = 1:n+2
        legendMatrix(row,col) = {[legendString(row),legendString(col)]};
    end
end
Walls = generateWalls(n);
G = graph();
for row = 1:n+2
    for col = 1:1:n
        G.addnode(row+col);
    end
end

snakeHead = [5 5];
snakeBody  = [5 4; 6 4; 6 3; 7 3];
food = [8 3];
barriers = [3 4; 3 7; 8 4];
dead = 0;
flag = 1;
turns = 1;
pic = figure(1);
pic2 = figure(2);



%% Looping time
while flag
    %getSnakeData();
    %getBarrierData();
    %getFoodData();
    currentFrame = addBarriers(Walls,barriers);
    currentFrame = addBarriers(currentFrame,snakeBody);
    
    
        figure(1);
        hold on;
        imagesc(currentFrame);
        set(gca,'YLim',[1,n+2],'YTick', (1:n+2),'XLim',[1,n+2],'XTick', (1:n+2));
        %set(gca,'YLim',[1,n+2],'YTick', (1:n+2),'YTickLabel',legend,'XLim',[1,n+2],'XTick', (1:n+2),'XTickLabel',legend);
        xlabel('Columns');
        ylabel('Rows');
        %used like imagesc(col, row, value)
        imagesc(snakeHead(2),snakeHead(1),2);
        imagesc(food(2),food(1),3);
        hold off;
        drawnow();
    
    
    weights = generateDanger(currentFrame,Walls,n);
    figure(2);
    imagesc(weights);
    moves = generateMovesetV1(currentFrame,weights,n,legendMatrix,G);
    [path,direction] = makeDecision(moves,snakeHead,food,legend);
    disp(direction);
    
%     p = plot(moves,'Layout','subspace');
%     highlight(p,(strcat(legend(snakeHead(1)),legend(snakeHead(2)))),'NodeColor','r');
%     highlight(p,(strcat(legend(food(1)),legend(food(2)))),'NodeColor','g');
%     highlight(p,path,'EdgeColor','r');
%     drawnow();
    
    
    [dead,snakeHead,snakeBody,food,barriers] = localTest(currentFrame,direction,snakeHead,snakeBody,barriers,food,n,turns);
    if dead
        flag = 0;
    end
    turns = turns+1;
end


