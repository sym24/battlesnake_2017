# -*- coding: utf-8 -*-
"""
Created on Fri Feb 10 21:07:29 2017

@author: joell
"""
import numpy as np
import networkx as nx
import matplotlib.pyplot as plt
import time
import sys


class Snake(object):
   
    def __init__(self,newName,n,unique,method = 'a_star',a = 0.5,b = 0.5,c = 0.25):
        self.legendString = '~abcdefghijklmnopqrstuvwxyz'
        self.legendMatrix = []
        self.n = n
        self.id = unique
        self.orignalID = unique
        self.method = method
        self.name = newName
        self.hunger = 100
        self.a = a
        self.b = b
        self.c = c
        for row in range(n+2):
            for col in range(n+2):
                self.legendMatrix.append(self.legendString[row]+self.legendString[col])
        self.legendMatrix = np.asarray(self.legendMatrix)
        self.Walls = generateWalls(self.n)
        self.G = nx.Graph()
        self.G.add_nodes_from(self.legendMatrix)
        self.legendMatrix = self.legendMatrix.reshape((n+2,n+2))

    def addBarriers(self,beforeFrame,toAdd):
        localFrame = np.copy(beforeFrame)
        for snake in range(len(toAdd)):
            for i in range(len(toAdd[snake])):
                localFrame[toAdd[snake][i][0],toAdd[snake][i][1]] = 1
        #localFrame
        return localFrame
        
    
    def makeDecision(self):
        try:
            if(self.path==''):
                return 'North'
            if(len(self.path)==1):
                return 'North'
            if(self.path[1]==self.legendMatrix[self.snakeHead[0]+1,self.snakeHead[1]]):
                return 'North'
            if(self.path[1]==self.legendMatrix[self.snakeHead[0]-1,self.snakeHead[1]]):
                return 'South'
            if(self.path[1]==self.legendMatrix[self.snakeHead[0],self.snakeHead[1]+1]):
                return 'East'
            if(self.path[1]==self.legendMatrix[self.snakeHead[0],self.snakeHead[1]-1]):
                return 'West'
        except Exception as e:
            print 'DECISION ERROR: '+ e.message
            print 'snakeHead: '
            print self.snakeHead
            print 'Path:%s'%(self.path)
            print 'Path Length:%d'%(len(self.path))
         
            x = 1/0
            
    
    def generateDanger(self):
        self.weights = np.zeros((self.n+2,self.n+2))
        for row in range(1,self.n+1):
            for col in range(1,self.n+1):
                self.weights[row,col] = self.currentFrame[row,col]*self.b+self.c + self.currentFrame[row+1,col]*self.b+self.currentFrame[row-1,col]*self.b+self.currentFrame[row,col+1]*self.b+self.currentFrame[row,col-1]*self.b
        self.weights = self.weights+self.Walls
        
    def generateMoveset(self):
        for row in range(1,self.n+1):
            for col in range (1,self.n+1):
                
                if(self.currentFrame[row,col]==0 and self.currentFrame[row+1,col]==0):
                    self.G.add_edge(self.legendMatrix[row,col],self.legendMatrix[row+1,col], weight = (self.weights[row,col]*self.a + self.weights[row+1,col]*self.b))
                        
                if(self.currentFrame[row,col]==0and self.currentFrame[row-1,col]==0):
                    self.G.add_edge(self.legendMatrix[row,col],self.legendMatrix[row-1,col], weight = (self.weights[row,col]*self.a + self.weights[row-1,col]*self.b))
    
                if(self.currentFrame[row,col]==0 and self.currentFrame[row,col+1]==0):
                    self.G.add_edge(self.legendMatrix[row,col],self.legendMatrix[row,col+1], weight = (self.weights[row,col]*self.a + self.weights[row,col+1]*self.b))
    
                if(self.currentFrame[row,col]==0 and self.currentFrame[row,col-1]==0):
                    self.G.add_edge(self.legendMatrix[row,col],self.legendMatrix[row,col-1], weight = (self.weights[row,col]*self.a + self.weights[row,col-1]*self.b))
                if(self.currentFrame[row,col]!=0):
                    try:
                        self.G.remove_edge(self.legendMatrix[row,col],self.legendMatrix[row+1,col])
                    except Exception:
                        pass
                    try:
                        self.G.remove_edge(self.legendMatrix[row,col],self.legendMatrix[row-1,col])
                    except Exception:
                        pass
                    try:
                        self.G.remove_edge(self.legendMatrix[row,col],self.legendMatrix[row,col+1])
                    except Exception:
                        pass
                    try:
                        self.G.remove_edge(self.legendMatrix[row,col],self.legendMatrix[row,col-1])
                    except Exception:
                        pass
        
    def feed(self):
        self.hunger = 100
        
    def getHunger(self):
        return self.hunger
    
    def setID(self,newValue):
        self.id = newValue
        
    def getOrignalID(self):
        return self.orignalID
    
    def dist(self,start,finish):
        deltaX = np.linalg.norm([start[0],finish[0]])
        deltaY = np.linalg.norm([start[1],finish[1]])
        return np.linalg.norm([deltaX,deltaY])
        
    def calcDist(self,unsorted):
        ans= np.array([])
        for uns in unsorted: 
            #print uns
            dx = uns[0]-self.snakeHead[0]
            dy = uns[1]-self.snakeHead[1]
            temp = [pow(pow(dx,2)+pow(dy,2),0.5)]
            ans=np.append(ans,temp)
        return ans
        
    def turn(self,frame,snakes,food):
        unsortedFood = np.copy(food)
        self.food = np.copy(food)
        self.hunger -=1                 # loose a hunger, cause a turn has passed
        self.a = self.hunger/100.0
        self.b = self.hunger/100.0
        localSnakes = np.copy(snakes)   # make sure we dont change the orignal
        snake = localSnakes[self.id]    # isolate just our snake from all the snakes
        self.currentFrame = self.addBarriers(np.copy(frame),localSnakes)     #add all of the snakes to the current frame
        localSnakes = np.delete(localSnakes,self.id,0)              # remove our snake from the local snakes (why, IDK?!)
        self.snakeHead = snake[0]                                   # set the snake head to the first thing in the snake array
        self.currentFrame[self.snakeHead[0],self.snakeHead[1]]=0    # make sure the head is not 1! EXTREMEMLY IMPORTANT
        snake = np.roll(snake,-1,0)     # circular shift, put the head at the back of the array
        snakeBody = snake[:-1]          # copy everything but the head
        self.generateDanger()           # generate the danger matrix
        self.generateMoveset()          # generate the moveset
        self.path = ''
        
        
        
        
        #if(self.orignalID==0): #focus on snake 1
        #    plt.figure(self.name)
        #    plt.clf()
        #    plt.cla()
        #    plt.xticks(np.array(range(self.n+2)), self.legendString[:])
        #    plt.yticks(np.array(range(self.n+2)), self.legendString[:])
        #    plt.imshow(self.currentFrame,interpolation='none')
        #    plt.gca().invert_yaxis()
        #    #nx.draw(self.G)
        #    
        #    plt.pause(0.00000001)
        
        index = 0
        while len(unsortedFood)!=0:
            distanceFood = self.calcDist(unsortedFood)
            maxFood = np.argmin(distanceFood)
            self.food[index]=unsortedFood[maxFood]
            unsortedFood = np.delete(unsortedFood,maxFood,0)
            index+=1
            #print len(unsortedFood)
            
                
        
        
        
        points = np.array(self.food.tolist())
        if(len(points)!=0):
            points = np.append(points,[[snakeBody[-1,0],snakeBody[-1,1]]],0)
        else:
            points = np.array([[snakeBody[-1,0],snakeBody[-1,1]]])
        points = np.append(points,[[snakeBody[-1,0]+1,snakeBody[-1,1]]],0)
        points = np.append(points,[[snakeBody[-1,0]-1,snakeBody[-1,1]]],0)
        points = np.append(points,[[snakeBody[-1,0],snakeBody[-1,1]+1]],0)
        points = np.append(points,[[snakeBody[-1,0],snakeBody[-1,1]-1]],0)
        
        for point in points:
            if self.method == 'a_star':
                try:
                    self.path =  nx.astar_path(self.G,self.legendMatrix[self.snakeHead[0],self.snakeHead[1]],self.legendMatrix[point[0],point[1]])
                    return self.makeDecision()
                    break
                except Exception as e:
                    #print self.name + '-> Tail Exception: '+ e.message
                    pass
            if self.method =='dijkstra_path':
                try:
                    self.path =  nx.dijkstra_path(self.G,self.legendMatrix[self.snakeHead[0],self.snakeHead[1]],self.legendMatrix[point[0],point[1]])
                    return self.makeDecision()
                    break
                except Exception as e:
                    #print self.name + '-> Tail Exception: '+ e.message
                    pass
           
            
            
            
        return self.makeDecision()
    
            
        
        


def addBarriers(beforeFrame,toAdd,value =1):
    localFrame = np.copy(beforeFrame)
    for i in range(len(toAdd)):
        localFrame[toAdd[i][0],toAdd[i][1]] = value
    return localFrame


    
def generateWalls(n):
    output_args = np.ones((n+2,n+2))
    output_args[1:n+1,1:n+1] = np.zeros((n,n))
    
    return output_args

lastFood = 0
lastBarrier = 0
def localTest(currentFrame,barriers,direction,snakeBody,snake,food,n,legendMatrix,turn):
    global lastFood,lastBarrier
    dead = 0
    forceFood = False
    
    if (direction == 'North'):
        newSnakeHeadLocation = [snake.snakeHead[0]+1, snake.snakeHead[1]]
    elif(direction =='South'):
        newSnakeHeadLocation = [snake.snakeHead[0]-1, snake.snakeHead[1]]
    elif(direction == 'East'):
        newSnakeHeadLocation = [snake.snakeHead[0], snake.snakeHead[1]+1]
    elif(direction == 'West'):
        newSnakeHeadLocation = [snake.snakeHead[0], snake.snakeHead[1]-1]
        direction = 'West '
    else:
        print 'I got a bad switch case'
            
    
    
    #print 'Name: %s \tHead:[%s]\tFood:[%s]\tDirection: %s\t length: %d Sum Frame: %d'%(snake.name,legendMatrix[snakeBody[0,0],snakeBody[0,1]],legendMatrix[food[0,0],food[0,1]],direction,len(snakeBody),np.sum(currentFrame))
    
    if(currentFrame[newSnakeHeadLocation[0],newSnakeHeadLocation[1]] in [1,2,3,4,5,6,7,8,9]):
        dead = 1
        print '%s just ran into a block on turn %d'%(snake.name,turn)
        
    if(snake.getHunger()<1):
        dead = 1
        print '%s just died of starvation'%(snake.name)
    
   
  
  # this is the condition that we have not eaten food
    if(newSnakeHeadLocation[0] not in food[:][:,0] or newSnakeHeadLocation[1] not in food[:][:,1]):
        snakeBody = snakeBody[:-1]                                      # trim one off the end
        snakeBody = np.insert(snakeBody,0,newSnakeHeadLocation,axis=0)  # add one on the top
        
    # this is the condition that I have eaten some food
    else:
        snake.feed()
        snakeBody = np.insert(snakeBody,0,newSnakeHeadLocation,axis = 0)
        for fud in range(len(food)):
            if(newSnakeHeadLocation[0]==food[fud][0] and newSnakeHeadLocation[1]==food[fud][1]):
                food = np.delete(food,fud,0)
                break
        forceFood = True
        
        
    if(turn%7==0 and turn-lastFood>3):
        lastFood = turn
        #print'APPENDING FOOD!'
        while True:
            newfood = np.array([np.random.random_integers(1,n+1,2)])
            if(currentFrame[newfood[0][0],newfood[0][1]]== 0):
                food = np.append(food,newfood,axis =0)
                #print "new Food at [%d,%d]"%(newfood[0][0],newfood[0][1])
                break

    #if(turn%10==0 and turn-lastBarrier>5 ):
    #    lastBarrier = turn
    #    while True:
    #        newBarrier = np.array([np.random.random_integers(1,n+1,2)])
    #        if(currentFrame[newBarrier[0][0],newBarrier[0][1]]!= 1):
    #            barriers = np.insert(barriers,0,newBarrier,axis = 0)
    #            break

    return(dead,snakeBody,food,barriers)




def mainLoop():
    drawing =True
    n = 20
    legendString = '~abcdefghijklmnopqrstuvwxyz'
    legendMatrix = []
    for row in range(n+2):
        for col in range(n+2):
            legendMatrix.append(legendString[row]+legendString[col])
    legendMatrix = np.asarray(legendMatrix)
    legendMatrix = np.reshape(legendMatrix,(n+2,n+2))
    
    Walls = generateWalls(n)
    
    
    snekBodies = np.array([[[1,5],[1 ,4],[1 ,3],[0,0]], #snake 1
                            [[3,9],[3 ,8], [3 ,7]],     #snake 2
                            [[5,7],[5 ,8], [5 ,9]]])    #snake 3
                            
    snekBodies[0] = np.delete(snekBodies[0],3,0)
    #snekBodies = np.resize(snekBodies,(2,))
    sneks = np.array([Snake("snake 1",n,1,),
                      Snake("snake 3",n,3),
                      Snake("snake 5",n,5)
                     ],dtype = np.object)
    #sneks = np.append(sneks,Snake("Other snake",n,1),axis=0)

    food = np.array([[8 ,3],
                     [10,10]],copy=True)
                     
    barriers = np.array([[2, 4]])
    
    
    
    turns = 0
    
    while len(sneks)>1:
        alive = np.array([[]])
        
        currentFrame =np.zeros((n+2,n+2))
        currentFrame = addBarriers(Walls,barriers)
        currentFrameWithoutSnakes = np.copy(currentFrame)
        currentFrame = addBarriers(currentFrame,food,10)
        currentFrame = addBarriers(currentFrame,[[0,0]],10)
        
            
    
        #currentFrame[food[0,0],food[0,1]]=3
        turns +=1
        for snek in range(len(sneks)):
            currentFrame = addBarriers(currentFrame,snekBodies[snek],sneks[snek].getOrignalID())
            currentFrame[snekBodies[snek][0][0],snekBodies[snek][0][1]]=7
            sneks[snek].setID(snek)
            localDis = sneks[snek].turn(currentFrameWithoutSnakes,snekBodies,food)

            
            (dead,newBody,food,barriers)=localTest(currentFrame,barriers,localDis,np.asarray(snekBodies[snek]),sneks[snek],food,n,legendMatrix,turns)
            
            snekBodies[snek] = newBody
            if(dead==1):
                alive = np.append(alive,snek)
                
        if(len(alive)!=0):
            snekBodies = np.delete(snekBodies,alive,0)
            sneks = np.delete(sneks,alive,0)
        sys.stdout.flush()
        if drawing:
            plt.figure("main arena")
            plt.clf()
            plt.cla()
            plt.xticks(np.array(range(n+2)), legendString[:])
            plt.yticks(np.array(range(n+2)), legendString[:])
            plt.imshow(currentFrame,interpolation='none')
            
            plt.gca().invert_yaxis()
            #plt.colorbar()
            plt.pause(0.00000001)
        #(dead,snakeHead,snakeBody,food,barriers) = localTest(currentFrame,direction,snakeHead,snakeBody,barriers,food,n,turns)
        #print 'Turn: %d'%turns
    print 'WE HAVE A WINNER!!!'
    print 'the winner was %s'%(sneks[0].name)
    print 'Lasted %d turns!'%(turns)

mainLoop()

