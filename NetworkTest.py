# -*- coding: utf-8 -*-
"""
Created on Fri Feb 10 21:07:29 2017

@author: joell
"""
import numpy as np
import networkx as nx
import matplotlib.pyplot as plt


def addBarriers(beforeFrame,toAdd):
    localFrame = np.copy(beforeFrame)
    for i in range(len(toAdd)):
        localFrame[toAdd[i][0],toAdd[i][1]] = 1
    return localFrame

def makeDecision(path,snakeHead,food,legendMatrix):
    if(path[1]==legendMatrix[snakeHead[0]+1,snakeHead[1]]):
        return 'North'
    if(path[1]==legendMatrix[snakeHead[0]-1,snakeHead[1]]):
        return 'South'
    if(path[1]==legendMatrix[snakeHead[0],snakeHead[1]+1]):
        return 'East'
    if(path[1]==legendMatrix[snakeHead[0],snakeHead[1]-1]):
        return 'West'
    
def generateDanger(currentFrame,Walls,n):
    weights = np.zeros((n+2,n+2))
    for row in range(1,n+1):
        for col in range(1,n+1):
            weights[row,col] = currentFrame[row,col]*.5+.25 + currentFrame[row+1,col]*.5+currentFrame[row-1,col]*.5+currentFrame[row,col+1]*.5+currentFrame[row,col-1]*.5
    weights = weights+Walls
    return weights
    
def generateWalls(n):
    output_args = np.ones((n+2,n+2))
    output_args[1:n+1,1:n+1] = np.zeros((n,n))
    
    return output_args

def localTest( currentFrame,direction,snakeHead,snakeBody,barriers,food,n,turn):
    
    #[snakeHead,snakeBody,food,barriers] = localTest(currentFrame,direction,snakeHead,snakeBody,food,barriers);
    # snakehead[row,col]
    dead = 0;
    
    if (direction == 'North'):
        newSnakeHeadLocation = [snakeHead[0]+1, snakeHead[1]]
    elif(direction =='South'):
        newSnakeHeadLocation = [snakeHead[0]-1, snakeHead[1]]
    elif(direction == 'East'):
        newSnakeHeadLocation = [snakeHead[0], snakeHead[1]+1]
    elif(direction == 'West'):
        newSnakeHeadLocation = [snakeHead[0], snakeHead[1]-1]
    else:
        print 'I got a bad switch case'
            
    
    #snakeHead = newSnakeHeadLocation;
    print 'Head:[%d,%d]\tFood:[%d,%d]\tDirection: %s\t length: %d Sum Frame: %d'%(newSnakeHeadLocation[0],newSnakeHeadLocation[1],food[0],food[1],direction,len(snakeBody),np.sum(currentFrame))
    
    if(currentFrame[newSnakeHeadLocation[0],newSnakeHeadLocation[1]]==1):
        dead = 1
        print 'I just ran into a block'
    
    if(newSnakeHeadLocation[0]!=food[0] or newSnakeHeadLocation[1]!=food[1]):
        snakeBody = snakeBody[:-1]    # trim one off the end
        snakeBody = np.insert(snakeBody,0,snakeHead,axis=0) # add one on the top
        
        snakeHead = newSnakeHeadLocation     # move the head
    else:
        print 'Apperently the newHeadLocation is the same as the food'
        print '->Head:[%d,%d]'%(newSnakeHeadLocation[0],newSnakeHeadLocation[1])
        print '->Food:[%d,%d]'%(food[0],food[1])
        snakeBody = np.insert(snakeBody,0,snakeHead,axis = 0)
        snakeHead = newSnakeHeadLocation
        oldFood = food
        flag = 1
        watchdog = 0
        while flag:
            watchdog = watchdog+1
            food = np.random.random_integers(1,n+1,2)
            if(currentFrame[food[0],food[1]]!=1 and food[0]!=oldFood[0] and food[1]!=oldFood[1] and snakeHead[0]!=food[0] and snakeHead[1]!=food[1]):
                print'there is a new food at'
                print food
                flag = 0
            if (watchdog>100):
                flag = 0
                dead = 1
                print 'There is no more room to put food'

    watchdog = 0
    if(turn%9==0 and watchdog<100):
        newBarrier = np.random.random_integers(1,n+1,2)
        if(currentFrame[newBarrier[0],newBarrier[1]]!= 1 and snakeHead[0]!=newBarrier[0] and snakeHead[1]!=newBarrier[1]):
            barriers = np.insert(barriers,0,newBarrier,axis = 0)
    return(dead,snakeHead,snakeBody,food,barriers)

def generateMoveset( Glocal, currentFrame,weights,n,legendMatrix):
    #Glocal.clear() # this clears all things
    
    for row in range(1,n+1):
        for col in range (1,n+1):
            
            if(currentFrame[row,col]==0 and currentFrame[row+1,col]==0):
                Glocal.add_edge(legendMatrix[row,col],legendMatrix[row+1,col], weight = (weights[row,col]*.5 + weights[row+1,col]*.5))
                    
            if(currentFrame[row,col]==0and currentFrame[row-1,col]==0):
                Glocal.add_edge(legendMatrix[row,col],legendMatrix[row-1,col], weight = (weights[row,col]*.5 + weights[row-1,col]*.5))

            if(currentFrame[row,col]==0 and currentFrame[row,col+1]==0):
                Glocal.add_edge(legendMatrix[row,col],legendMatrix[row,col+1], weight = (weights[row,col]*.5 + weights[row,col+1]*.5))

            if(currentFrame[row,col]==0 and currentFrame[row,col-1]==0):
                Glocal.add_edge(legendMatrix[row,col],legendMatrix[row,col-1], weight = (weights[row,col]*.5 + weights[row,col-1]*.5))
            if(currentFrame[row,col]!=0):
                try:
                    Glocal.remove_edge(legendMatrix[row,col],legendMatrix[row+1,col])
                except Exception:
                    pass
                try:
                    Glocal.remove_edge(legendMatrix[row,col],legendMatrix[row-1,col])
                except Exception:
                    pass
                try:
                    Glocal.remove_edge(legendMatrix[row,col],legendMatrix[row,col+1])
                except Exception:
                    pass
                try:
                    Glocal.remove_edge(legendMatrix[row,col],legendMatrix[row,col-1])
                except Exception:
                    pass
    return Glocal


def mainLoop():
    drawing =  True
    drawGraph = not True
    n = 258
    #legend = ['~','a','b','c','d','e','f','g','h','i','j','k','l','m','n','o','p','q','r','s','t','u','v','w','x','y','z']
    legendString = '~abcdefghijklmnopqrstuvwxyz'
    legendMatrix = []
    for row in range(n+2):
        for col in range(n+2):
            legendMatrix.append(legendString[row]+legendString[col])
    legendMatrix = np.asarray(legendMatrix)
    
    Walls = generateWalls(n)
    G = nx.Graph()
    G.add_nodes_from(legendMatrix)
    legendMatrix = legendMatrix.reshape((n+2,n+2))
    
    
    snakeHead = [5 ,5]
    snakeBody  = np.array([[5 ,4], [6 ,4],[ 6, 3],[ 7, 3]])
    food = [8 ,3]
    barriers = [[3, 4],[3 ,7],[ 8 ,4]]
    dead = 0
    turns = 0
    
    while dead==0:
        turns +=1
        currentFrame =np.zeros((n+2,n+2))
        currentFrame = addBarriers(Walls,barriers)
        currentFrame = addBarriers(currentFrame,snakeBody)
        weights = generateDanger(currentFrame,Walls,n)
        weights = generateDanger(weights,Walls,n)
        
        G = generateMoveset(G,currentFrame,weights,n,legendMatrix)
        try:
            path =  nx.astar_path(G,legendMatrix[snakeHead[0],snakeHead[1]],legendMatrix[food[0],food[1]])
        except Exception:
            print 'I HAVE NO WHERE TO GO!!!'
            break
        #print path
        direction =  makeDecision(path,snakeHead,food,legendMatrix)
        if drawing:
            if drawGraph:
                pos = nx.spring_layout(G,weight ='none',iterations=100)
                
                plt.cla()        
                nx.draw_networkx_nodes(G,pos,node_color='r',alpha=0.1)
                nx.draw_networkx_nodes(G,pos,nodelist=[legendMatrix[snakeHead[0],snakeHead[1]]],node_color='b')
                nx.draw_networkx_nodes(G,pos,nodelist=[legendMatrix[food[0],food[1]]],node_color='g')
                nx.draw_networkx_nodes(G,pos,nodelist=path,node_color='y',alpha = 0.3)
                #nx.draw_networkx_nodes(G,pos,nodelist=path,node_color='y',alpha = 0.3)
                nx.draw_networkx_edges(G,pos,alpha=0.5)
                plt.pause(0.00000001)
            else:
                plt.clf()
                plt.cla()
                currentFrame[snakeHead[0],snakeHead[1]]=2
                currentFrame[food[0],food[1]]=3
                plt.imshow(currentFrame,interpolation='none')
                plt.pause(0.00000001)
        (dead,snakeHead,snakeBody,food,barriers) = localTest(currentFrame,direction,snakeHead,snakeBody,barriers,food,n,turns)
        print 'Turn: %d'%turns
    print 'I died'
    print barriers
    print snakeBody

mainLoop()

