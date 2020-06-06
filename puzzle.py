# -*- coding: utf-8 -*-
"""
Created on Sat May 16 19:17:40 2020

@author: ASUS
"""

SCREEN_WIDTH=1200
SCREEN_HEIGHT=600
LINE_WIDTH=5
FONT_SIZE=24
CROP_NUMBER=3

import os
import pygame
from PIL import Image
import random
import shutil

def start_page():
    pygame.init()
    StartScreen=pygame.display.set_mode((SCREEN_WIDTH,SCREEN_HEIGHT))
    pygame.display.set_caption('Puzzle-Start Page')
    bgc=(255,250,240)
    toquit=False
    while toquit is not True:
        StartScreen.fill(bgc)
        drawText(StartScreen,'Click anywhere to start',Sm(1,0,2),Sm(0,0,2),90,(0,0,0),bgc)
        drawText(StartScreen,'Puzzle Game',Sm(1,0,2),Sm(0,0,4),50,(0,0,0),bgc)
        for event in pygame.event.get():
            if event.type==pygame.QUIT:
                pygame.quit()
            elif event.type==pygame.MOUSEBUTTONDOWN:
                if event.button==1:
                    toquit=True
        pygame.display.flip()
def run_game():
    pygame.init()
    Screen=pygame.display.set_mode((SCREEN_WIDTH,SCREEN_HEIGHT))
    pygame.display.set_caption("Puzzle")
    bgc=(255,250,240)
    level=1
    a,b,c=NewGame(Screen)
    tem=False
    toquit=False
    clicked=False
    thisRoundMoves=0
    totalMoves=0
    thisRoundRetryTimes=0
    isCheating=False
    totalRetryTimes=0
    musicPlayed=False
    CX,CY=0,0
    while toquit is not True:
        dp=False
        PlayMusic(level,musicPlayed)
        if musicPlayed==False:
            musicPlayed=True
        if CheckFinished(a,b)==True and clicked==True:
            level=level+1
            if level>len(GetPictures())-1:
                toquit=True
                totalMoves=totalMoves+thisRoundMoves
                thisRoundMoves=0
                totalRetryTimes=totalRetryTimes+thisRoundRetryTimes
                thisRoundRetryTimes=0
                pygame.mixer.music.stop()
            else:
                a,b,c=NewRound(GetPictures(),level,Screen)
                clicked=False
                totalMoves=totalMoves+thisRoundMoves
                thisRoundMoves=0
                totalRetryTimes=totalRetryTimes+thisRoundRetryTimes
                thisRoundRetryTimes=0
                musicPlayed=False
                pygame.mixer.music.stop()
        else:
            clicked=False
        for event in pygame.event.get():
            if event.type==pygame.QUIT:
                if os.path.exists('./~cp'):
                    shutil.rmtree('./~cp')
                pygame.quit()
            elif event.type==pygame.MOUSEBUTTONDOWN:
                if event.button==1:
                    clicked=True
                    CX,CY=pygame.mouse.get_pos()
                    print(CX,CY)
            elif event.type==pygame.KEYDOWN:
                if event.key==pygame.K_LEFT or event.key==pygame.K_a:
                    b,dp=MovePuzzle(b,'up')
                    thisRoundMoves=thisRoundMoves+1
                elif event.key==pygame.K_RIGHT or event.key==pygame.K_d:
                    b,dp=MovePuzzle(b,'down')
                    thisRoundMoves=thisRoundMoves+1
                elif event.key==pygame.K_DOWN or event.key==pygame.K_s:
                    b,dp=MovePuzzle(b,'right')
                    thisRoundMoves=thisRoundMoves+1
                elif event.key==pygame.K_UP or event.key==pygame.K_w:
                    b,dp=MovePuzzle(b,'left')
                    thisRoundMoves=thisRoundMoves+1
                elif event.key==pygame.K_r:
                    a,b,c=NewRound(GetPictures(),level,Screen)
                    thisRoundMoves=0
                    thisRoundRetryTimes=thisRoundRetryTimes+1
                elif event.key == pygame.K_LSHIFT:
                    tem=True
                elif event.key==pygame.K_END and tem==True:
                    isCheating=True
                    level=level+1
                    if level>len(GetPictures())-1:
                        level=level-1
                    a,b,c=NewRound(GetPictures(),level,Screen)
                    tem=False
                    musicPlayed=False
                    pygame.mixer.music.stop()
                    #totalMoves=totalMoves+thisRoundMoves
                    #thisRoundMoves=0
                    #totalRetryTimes=totalRetryTimes+thisRoundRetryTimes
                    #thisRoundRetryTimes=0
                elif event.key==pygame.K_HOME and tem==True:
                    isCheating=True
                    level=level-1
                    if level<1:
                        level=level+1
                    a,b,c=NewRound(GetPictures(),level,Screen)
                    tem=False
                    musicPlayed=False
                    pygame.mixer.music.stop()
                elif event.key==pygame.K_p:
                    Cheat()
        if CX>=Sm(1,0,24)*11 and CY>=Sm(0,0,3) and CX<=Sm(1,0,24)*13 and CY<=Sm(0,0,12)*5:
            b,dp=MovePuzzle(b,'left')
            thisRoundMoves=thisRoundMoves+1
            CX,CY=0,0
        elif CX>=Sm(1,0,12)*5 and CY>=Sm(0,0,24)*11 and CX<=Sm(1,0,24)*11 and CY<=Sm(0,0,20)*11:
            b,dp=MovePuzzle(b,'up')
            thisRoundMoves=thisRoundMoves+1
            CX,CY=0,0
        elif CX>=Sm(1,0,24)*11 and CY>=Sm(0,0,12)*7 and CX<=Sm(1,0,24)*13 and CY<=Sm(0,0,3)*2:
            b,dp=MovePuzzle(b,'right')
            thisRoundMoves=thisRoundMoves+1
            CX,CY=0,0
        elif CX>=Sm(1,0,40)*21 and CY>=Sm(0,0,24)*11 and CX<=Sm(1,0,48)*29 and CY<=Sm(0,0,20)*13:
            b,dp=MovePuzzle(b,'down')
            thisRoundMoves=thisRoundMoves+1
            CX,CY=0,0
        draw_bg(Screen,bgc)
        if dp==True:
            thisRoundMoves-=1
        DrawStatus(Screen,bgc,thisRoundMoves,totalMoves,level,len(GetPictures())-1,isCheating)
        for n in range(len(b)):
            b[n].move(n)
            b[n].blitme()
        c.blitme()
        DrawButton(Screen)
        pygame.display.flip()
    return isCheating,totalMoves,totalRetryTimes
def GameOver(isCheating,totalMoveTimes,totalRetryTimes):
    pygame.init()
    StartScreen=pygame.display.set_mode((SCREEN_WIDTH,SCREEN_HEIGHT))
    pygame.display.set_caption('Puzzle-Game Over')
    bgc=(255,250,240)
    toquit=False
    while toquit is not True:
        StartScreen.fill(bgc)
        drawText(StartScreen,'Congratulations! You finished all the puzzles!',Sm(1,0,2),Sm(0,0,2),60,(0,0,0),bgc)
        drawText(StartScreen,'Click anywhere to start again',Sm(1,0,2),Sm(0,0,4),50,(0,0,0),bgc)
        if isCheating is not True:
            drawText(StartScreen,'MoveTimes(Total): '+str(totalMoveTimes),Sm(1,0,4),Sm(0,1,1,-25),25,(0,0,0),bgc)
            drawText(StartScreen,'RetryTimes(Total): '+str(totalRetryTimes),Sm(1,0,2),Sm(0,1,1,-25),25,(0,0,0),bgc)
            drawText(StartScreen,'Time past: -:--',Sm(1,0,4)*3,Sm(0,1,1,-25),25,(0,0,0),bgc)
        for event in pygame.event.get():
            if event.type==pygame.QUIT:
                pygame.quit()
            elif event.type==pygame.MOUSEBUTTONDOWN:
                if event.button==1:
                    toquit=True
        pygame.display.flip()
def PlayMusic(level,stop=False):
    if level>=10:
        bgm='bgm/b'+str(level)+'.mp3'
    else:
        bgm='bgm/'+str(level)+'.mp3'
    if stop==False:
        pygame.mixer.music.load(bgm)
        pygame.mixer.music.play(100)
def Cheat(puzzles):
    print()

def DrawButton(Screen):
    drawText(Screen,'  up  ',Sm(1,0,2),Sm(0,0,8)*3,50,(0,0,0),(255,0,0))
    drawText(Screen,'down',Sm(1,0,2),Sm(0,0,8)*5,50,(0,0,0),(255,0,0))
    drawText(Screen,'left',Sm(1,0,16)*7,Sm(0,0,2),50,(0,0,0),(255,0,0))
    drawText(Screen,'right',Sm(1,0,16)*9,Sm(0,0,2),50,(0,0,0),(255,0,0))
def CheckFinished(a,puzzles):
    b=True
    if puzzles[8].place!='blank.png' and puzzles[8].place!='p':
        return False
    for i in range(len(puzzles)-1):
        if puzzles[i].place[6]=='-':
            if puzzles[i].placenum!=int(puzzles[i].place[7]):
                b=False
        else:
            if puzzles[i].placenum!=int(puzzles[i].place[6]):
                b=False
    return b
def MovePuzzle(cps,direction):
    for i in range(len(cps)):
        if cps[i].place=='blank.png':
            blankpartnum=i+1
    if blankpartnum==1:
        tmp=cps[0]
        if direction=='up':    
            cps[0]=cps[3]
            cps[3]=tmp
        elif direction=='left':
            cps[0]=cps[1]
            cps[1]=tmp
        else:
            return cps,True
    elif blankpartnum==2:
        tmp=cps[1]
        if direction=='up':
            cps[1]=cps[4]
            cps[4]=tmp
        elif direction=='left':
            cps[1]=cps[2]
            cps[2]=tmp
        elif direction=='right':
            cps[1]=cps[0]
            cps[0]=tmp
        else:
            return cps,True
    elif blankpartnum==3:
        tmp=cps[2]
        if direction=='up':
            cps[2]=cps[5]
            cps[5]=tmp
        elif direction=='right':
            cps[2]=cps[1]
            cps[1]=tmp
        else:
            return cps,True
    elif blankpartnum==4:
        tmp=cps[3]
        if direction=='up':
            cps[3]=cps[6]
            cps[6]=tmp
        elif direction=='left':
            cps[3]=cps[4]
            cps[4]=tmp
        elif direction=='down':
            cps[3]=cps[0]
            cps[0]=tmp
        else:
            return cps,True
    elif blankpartnum==5:
        tmp=cps[4]
        if direction=='up':
            cps[4]=cps[7]
            cps[7]=tmp
        elif direction=='left':
            cps[4]=cps[5]
            cps[5]=tmp
        elif direction=='right':
            cps[4]=cps[3]
            cps[3]=tmp
        else:
            cps[4]=cps[1]
            cps[1]=tmp
    elif blankpartnum==6:
        tmp=cps[5]
        if direction=='up':
            cps[5]=cps[8]
            cps[8]=tmp
        elif direction=='down':
            cps[5]=cps[2]
            cps[2]=tmp
        elif direction=='right':
            cps[5]=cps[4]
            cps[4]=tmp
        else:
            return cps,True
    elif blankpartnum==7:
        tmp=cps[6]
        if direction=='down':
            cps[6]=cps[3]
            cps[3]=tmp
        elif direction=='left':
            cps[6]=cps[7]
            cps[7]=tmp
        else:
            return cps,True
    elif blankpartnum==8:
        tmp=cps[7]
        if direction=='down':
            cps[7]=cps[4]
            cps[4]=tmp
        elif direction=='left':
            cps[7]=cps[8]
            cps[8]=tmp
        elif direction=='right':
            cps[7]=cps[6]
            cps[6]=tmp
        else:
            return cps,True
    else:
        tmp=cps[8]
        if direction=='down':
            cps[8]=cps[5]
            cps[5]=tmp
        elif direction=='right':
            cps[8]=cps[7]
            cps[7]=tmp
        else:
            return cps,True
    return cps,False
def MixPictures(pics,num=3):
    t=True
    for i in range(random.randint(100,150)):
        a=random.randint(1,4)
        if a == 1:
            di='up'
        elif a == 2:
            di='down'
        elif a == 3:
            di='right'
        elif a == 4:
            di='left'
        pics,t=MovePuzzle(pics,di)
    #for j in range(len(pics)):
     #   pics[j].move(j+1)
    return pics

def NewGame(Screen):
    a,b,c=NewRound(GetPictures(),1,Screen)
    return a,b,c
    
def NewRound(pictures,level,Screen):
    a=CutPicture(pictures[level-1],level)
    b=[]
    c=OriginalPicture(Screen,pictures[level-1])
    for m in range(len(a)-1):
        b.append(APieceOfPicture(Screen,a[m],m+1))
    b.append(APieceOfPicture(Screen,'blank.png',9))
    a=b
    b=MixPictures(b)
    return a,b,c
    
def draw_bg(Screen,bgc):
    # 背景色
    Screen.fill(bgc)  # 看到我了嗎，報錯了是不是壓
    # 拼圖邊框
    draw_frame(Screen,Sm(1,0,8),Sm(0,0,4),Sm(1,0,4),Sm(0,0,2),(255,0,0),LINE_WIDTH)
    draw_frame(Screen,Sm(1,0,8)*5,Sm(0,0,4),Sm(1,0,4),Sm(0,0,2),(0,255,0),LINE_WIDTH)
    # 邊框上方註釋
    draw_frame(Screen,Sm(1,0,8),Sm(0,0,6),Sm(1,0,4),Sm(0,0,12,-(LINE_WIDTH+1)),(0,0,255),LINE_WIDTH)
    draw_frame(Screen,Sm(1,0,8)*5,Sm(0,0,6),Sm(1,0,4),Sm(0,0,12,-(LINE_WIDTH+1)),(0,0,255),LINE_WIDTH)
    drawText(Screen,'Original puzzle',Sm(1,0,4)*3,Sm(0,0,5),FONT_SIZE,(0,0,0),bgc)
    drawText(Screen,'Your puzzle',Sm(1,0,4),Sm(0,0,5),FONT_SIZE,(0,0,0),bgc)
    drawText(Screen,'Use WASD or arrows to control your puzzle. Press R to restart.',Sm(1,0,2),25,25,(0,0,0),bgc)
    drawText(Screen,'If you finished this level, click anywhere to start the next one.',Sm(1,0,2),Sm(0,0,8),FONT_SIZE,(0,0,0),bgc)
     

def draw_frame(Screen,x,y,width,height,color,line_width=0):
    pygame.draw.rect(Screen,color,(x,y,width,height),line_width)
    
def drawText(self,text,posx,posy,textHeight,fontColor=(0,0,0),backgroudColor=(255,255,255)):
        fontObj = pygame.font.Font('Calibri.ttf', textHeight)  
        textSurfaceObj = fontObj.render(text, True,fontColor,backgroudColor)  
        textRectObj = textSurfaceObj.get_rect()  
        textRectObj.center = (posx, posy)  
        self.blit(textSurfaceObj, textRectObj)  

def Sm(wh,ts,num,plus=0):
    if wh:
        if ts:
            n=SCREEN_WIDTH*num+plus
        else:
            n=SCREEN_WIDTH/num+plus
    else:
        if ts:
            n=SCREEN_HEIGHT*num+plus
        else:
            n=SCREEN_HEIGHT/num+plus
    return n

def DrawStatus(Screen,bgc,thisRoundMoves,totalMoves,level,numOfLevels,isCheating):
    if isCheating==False:
        drawText(Screen,'Moved times(This round): '+str(thisRoundMoves),Sm(1,0,4),Sm(0,1,1,-25),25,(0,0,0),bgc)
        drawText(Screen,'Moved times(Total): '+str(totalMoves),Sm(1,0,2),Sm(0,1,1,-25),25,(0,0,0),bgc)
        drawText(Screen,'Level: '+str(level)+' / '+str(numOfLevels),Sm(1,0,4)*3,Sm(0,1,1,-25),25,(0,0,0),bgc)
    else:
        drawText(Screen,'You are now in Cheating Mode. Status board is not available',Sm(1,0,2),Sm(0,1,1,-50),40,(255,0,0),bgc)
        #drawText(Screen,'Moved times(This round): '+str(thisRoundMoves),Sm(1,0,4),Sm(0,1,1,-25),25,(0,0,0),bgc)
        #drawText(Screen,'Moved times(Total): '+str(totalMoves),Sm(1,0,2),Sm(0,1,1,-25),25,(0,0,0),bgc)
        #drawText(Screen,'Level: '+str(level)+' / '+str(numOfLevels),Sm(1,0,4)*3,Sm(0,1,1,-25),25,(0,0,0),bgc)
    
def CutPicture(Pic,picnum,num=3):
    pic=Image.open(Pic)
    croppedPictures=[]
    pics=[]
    pic=pic.resize((int(Sm(1,0,4)),int(Sm(0,0,2))))
    w,h=pic.size
    for i in range(num):
        for j in range(num):
            croppedPictures.append(pic.crop((w/num*i,h/num*j,w/num*(i+1),h/num*(j+1))))
    for k in range(len(croppedPictures)):
        if not os.path.exists('./~cp'):
            os.makedirs('./~cp')
        croppedPictures[k].save('~cp/'+str(picnum)+'-'+str(k+1)+'.jpg')
        pics.append('~cp/'+str(picnum)+'-'+str(k+1)+'.jpg')
    return pics

def GetPictures():
    pics=[]
    for filename in os.listdir('.'):
        if not (filename.endswith('.png') or filename.endswith('.jpg')):
            continue
        else:
            pics.append(str(filename))
    return pics
    
class OriginalPicture():
    def __init__(self,screen,pic):
        self.screen=screen
        self.place=pic
        Image.open(pic).resize((int(Sm(1,0,4)),int(Sm(0,0,2)))).save('~cp/resized_'+pic)
        picc='~cp/resized_'+pic
        self.image=pygame.image.load(picc)
        self.rect=self.image.get_rect()
        self.rect.left=Sm(1,0,8)*5
        self.rect.top=Sm(0,0,4)
    
    def blitme(self):
        self.screen.blit(self.image,self.rect)
class APieceOfPicture():
    def __init__(self,screen,pic,placenum):
        self.screen=screen
        self.place=pic
        self.image=pygame.image.load(pic)
        self.rect=self.image.get_rect()
        self.placenum=placenum
        if self.placenum<=3:
            self.rect.left=Sm(1,0,8)
            if self.placenum==1:
                self.rect.top=Sm(0,0,4)
            elif self.placenum==2:
                self.rect.top=Sm(0,0,4)+Sm(0,0,6)
            else:
                self.rect.top=Sm(0,0,4)+Sm(0,0,3)
        elif self.placenum<=6:
            self.rect.left=Sm(1,0,8)+Sm(1,0,12)
            if self.placenum==4:
                self.rect.top=Sm(0,0,4)
            elif self.placenum==5:
                self.rect.top=Sm(0,0,4)+Sm(0,0,6)
            else:
                self.rect.top=Sm(0,0,4)+Sm(0,0,3)
        else:
            self.rect.left=Sm(1,0,8)+Sm(1,0,6)
            if self.placenum==7:
                self.rect.top=Sm(0,0,4)
            elif self.placenum==8:
                self.rect.top=Sm(0,0,4)+Sm(0,0,6)
            else:
                self.rect.top=Sm(0,0,4)+Sm(0,0,3)
    def move(self,npn):
        self.placenum=npn+1
        if self.placenum<=3:
            self.rect.left=Sm(1,0,8)
            if self.placenum==1:
                self.rect.top=Sm(0,0,4)
            elif self.placenum==2:
                self.rect.top=Sm(0,0,4)+Sm(0,0,6)
            else:
                self.rect.top=Sm(0,0,4)+Sm(0,0,3)
        elif self.placenum<=6:
            self.rect.left=Sm(1,0,8)+Sm(1,0,12)
            if self.placenum==4:
                self.rect.top=Sm(0,0,4)
            elif self.placenum==5:
                self.rect.top=Sm(0,0,4)+Sm(0,0,6)
            else:
                self.rect.top=Sm(0,0,4)+Sm(0,0,3)
        else:
            self.rect.left=Sm(1,0,8)+Sm(1,0,6)
            if self.placenum==7:
                self.rect.top=Sm(0,0,4)
            elif self.placenum==8:
                self.rect.top=Sm(0,0,4)+Sm(0,0,6)
            else:
                self.rect.top=Sm(0,0,4)+Sm(0,0,3)
    def blitme(self):
        self.screen.blit(self.image,self.rect)
tq=False
start_page()
while True:
    n1,n2,n3=run_game()
    print(n1,n2,n3)
    GameOver(n1,n2,n3)