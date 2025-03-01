import tkinter as tk
from tkinter import Text
from tkinter import ttk
from tkinter.messagebox import showinfo
import time
import os
import random

bg_color = '#756b69' #color code for background, it's a medium grey
buttonPress = False #condition to see if button was pressed for input
inputText = '' #variable to take in text input string
inputLoc = ''
mansion = [] # list of objects for rooms in the mansion 
items = [] # list for items to be added to itemStatus
check=0
place=100

#creating the window for the GUI
root = tk.Tk()
root.geometry('1600x800')
root.title('Main Platform')
root.resizable(width=None, height=None) #canvas acts oddly when you resize the window, so I made it locked in size
root.configure(background=bg_color)

#create the status image canvas
status = tk.Canvas(root, width=500, height=300, bg='white')
status.pack(anchor=tk.CENTER, expand=True)
status.place(x=50, y=50)

#create the text box where the story output will be
output = tk.Text(root, width=128, height=15, bg='white', font = 'Arial 16', fg = 'black') #the sizing is based off character length, where everything else is by pixel count
output.place(x=50, y=400)
# add scrollbar
scrollbar = ttk.Scrollbar(output, orient='vertical', command=output.yview)
output['yscrollcommand'] = scrollbar.set

#create health status text box and the label for it
healthLabel = tk.Label(root, text='Health', font='Arial 16', fg='white', bg=bg_color)
healthLabel.place(x=600, y=50)
healthStatus = tk.Text(root, width=20, height=1, bg='white', fg='black')
healthStatus.pack(anchor=tk.CENTER, expand=True)
healthStatus.place(x=600, y=75)
healthStatus['state'] = 'disabled' #locks the text so you can't edit it

#create list of collected items and the label for it
itemLabel = tk.Label(root, text='Items', font='Arial 16', fg='white', bg=bg_color)
itemLabel.place(x=600, y=120)
itemStatus = tk.Text(root, width=20, height=13, bg='white', fg='black')
itemStatus.pack(anchor=tk.CENTER, expand=True)
itemStatus.place(x=600,y=145)
itemStatus['state'] = 'disabled'

#create text box and button for inserting choices
inputLabel = tk.Label(root, text='Input', font='Arial 16', fg='white', bg=bg_color)
inputLabel.place(x=600, y=325)
#inputBox = tk.Text(root, width=15, height=1, bg='white', fg='black', textvariable=textGrab)
#inputBox.pack(anchor=tk.CENTER, expand=True)
#inputBox['state']= 'normal'

textGrab = tk.StringVar() #tkinter varaible to grab from the input text
inputStyle = ttk.Style()
inputStyle.configure("inputStyle.TEntry", width=1, bg='white',fg='black')
inputBox = ttk.Entry(root, textvariable=textGrab, style='inputStyle.TEntry')
inputBox.place(x=600, y=350)

#create canvas for mini map
miniMap = tk.Canvas(root, width=400, height=300, bg='white')
miniMap.pack(anchor=tk.CENTER, expand=True)
miniMap.place(x=800,y=50)

#add mini map to canvas
mapImage = tk.PhotoImage(file='map.png')
miniMap.create_image((210,155), image=mapImage)

#create placement dot for mini map and points that will correlate to it
pointsMR = ((200,260),(215,275))
pointsKI = ((115,260),(130,275))
pointsB1 = ((202,210),(217,225))
pointsG1 = ((252,210),(267,225))
pointsLR = ((300,260),(315,275))
pointsSF = ((145,130),(160,145))
pointsMB = ((115,130),(130,145))
pointsBB = ((70,110),(85,125))
pointsBC = ((110,60),(125,75))
pointsG2 = ((230,130),(245,145))
pointsB2 = ((300,130),(315,145))
pointsG3 = ((300,70),(315,85))
pointsAS = ((230,60),(245,75))
location = miniMap.create_oval(*pointsMR, fill ='#C05957', outline='black')
#create points for each room on the mini map

#create command to clear the text in a text box
def clearText(block):
    block['state'] = 'normal'
    block.delete("1.0",tk.END)
    block['state'] = 'disabled'
    
#create command to insert text to a text box
def insertText(block, text):
    text += '\n'
    block['state'] = 'normal'
    block.insert(tk.END,text)
    block['state'] = 'disabled'
    
#clearText and insertTest put together
def clearAndInsertText(block, text):
    block['state'] = 'normal'
    block.delete("1.0",tk.END)
    text += '\n'
    block.insert(tk.END,text)
    block['state'] = 'disabled'
    
# used as a 'Help' function for a player who doesn't know the full command list    
def commandList():
    insertText(output, "\nCommand List:\nenter [ROOM]: enters specified room\nenter: enter with no argument brings you back to the main room if you're in an room that's joined to it\ncheck [OBJECT]: checks object in current room you're in\nheal: if you have painkillers, it heals you (uses 1)\nup: if you're in the main room of the floor, allows you raise up a level in the mansion\ndown: if you're in the main room of the floor, allows you descend a level\nhelp: display command list\nfguide: display command list for fighting")
    
# display seperate command list related to fighting
def fightCommands(weapon):
    insertText(output, "You have one of these options, and you'll continue to do it until either you or the enemy dies:\n")
    if (weapon == True):
        insertText(output,"\nFight Commands:\npunch: punches enemy, can do 10, 20 or 30 damage, 20% chance of missing\nkick: kicks enemy, can do 30, 40 or 50 damage but has a 50% chance of missing\nshove: does 10 damage, with 0% chance of missing\nslash: slashes enemy, can do 20, 30, or 40 damage, with 10% chance of missing\n\nSYNTAX: fight [CHOICE]")
    else:
        insertText(output,"\nFight Commands:\npunch: punches enemy, can do 10, 20 or 30 damage, 20% chance of missing\nkick: kicks enemy, can do 30, 40 or 50 damage but has a 50% chance of missing\nshove: does 10 damage, with 0% chance of missing")

#create class for player
class Player:
    def __init__(self, health, meds, level, location, kitchen_key, attic_key, closet_key, stairs_key, knife, lost):
        self.health = health
        self.meds = meds
        self.level = level
        self.location = location
        self.kitchen_key = kitchen_key
        self.attic_key = attic_key
        self.closet_key = closet_key
        self.stairs_key = stairs_key
        self.knife = knife
        self.lost = lost
        
    def heal(self):
        if (self.meds >= 1):
            self.health = 100
            self.meds -= 1
        else:
            clearAndInsertText(output, "You don't have enough medication to heal")
    
    def up(self):
        match (self.level):
            case self.level if self.level == 1:
                if (self.stairs_key == True):
                    self.level = 2
                    miniMap.coords(location, *pointsSF)
                    clearAndInsertText(output, "You open the door to the second floor and go in. There are more closed doors all around")
                else:
                    clearAndInsertText(output, "You cannot enter the second floor without a key")
            case self.level if self.level == 2:
                if (self.attic_key == True):
                    self.level = 3
                    clearAndInsertText(output, "You open the door to the attic, and there's a zombie! this creature looks stronger than the rest, you have no other option but to fight it off")
                    zombieHealth = 150
                else:
                    clearAndInsertText(output, "You cannot enter the attic without a key")
                    #enter fight function for mini boss battle
                    
    def down(floor):
        if (floor == 1):
            clearAndInsertText(output, "You are on the first floor, you cannot go down")
        else:
            floor -= 1
            miniMap.coords(location, *pointsMR)
            
    def check(self, room, kitchen):
        match room:
            case 0:
                clearAndInsertText(output, "There isn't one in this room")
                return 0
            case 1:
                clearAndInsertText(output, "You check, but it's empty")
                return 8
            case 2:
                clearAndInsertText(output, "You check, and there's a key labeled 'Stairs'. You put it in your pocket")
                self.stairs_key = True
                insertText(itemStatus,"Stairs Key")
                return 8
            case 3:
                clearAndInsertText(output, "You check, and you find a key labeled 'Closet'. You put it in your pocket")
                self.closet_key = True
                insertText(itemStatus, "Closet Key")
                return 8
            case 4:
                clearAndInsertText(output, "You check, and there's a key labeled 'Attic'. You put it in your pocket")
                self.attic_key = True
                inserText(itemStatus, "Attic Key")
                return 8
            case 5:
                clearAndInsertText(output, "You check, and there's a key labeled 'Kitchen'. You put it in your pocket")
                self.kitchen_key = True
                insertText(itemStatus, "Kitchen Key")
                return 8
            case 6:
                if kitchen == True:
                    clearAndInsertText(output, "You check, and you find a knife. You sense you may need it, so you bring it with you")
                    self.knife = True
                    insertText(itemStatus, "Knife")
                    return 8
                else:
                    clearAndInsertText(output, "You try to open it, but it's locked. Perhaps there's a key for it lying around")
                    return 6
            case 7:
                clearAndInsertText(output, "You check, and there's some painkillers. You sense you may need it, so you bring it with you")
                if (self.meds > 0):
                    self.meds += 1
                else:
                    insertText(itemStatus, "Medication")
                    self.meds += 1
                return 8
            case _:
                clearAndInsertText(output, "You've already checked this, and it's empty now")
                return 8

        
#create the class for the mansion rooms        
class Room:
    def __init__(self, command, locked, floor, ratio, drawer1, drawer2, bed, cabinet1, cabinet2, cabinet3, oven, couch, storage, entertainment, closet, dresser1, dresser2):
        self.command = command
        self.locked = locked
        self.floor = floor
        self.ratio = ratio
        self.drawer1 = drawer1
        self.drawer2 = drawer2
        self.bed = bed
        self.cabinet1 = cabinet1
        self.cabinet2 = cabinet2
        self.cabinet3 = cabinet3
        self.oven = oven
        self.couch = couch
        self.storage = storage
        self.entertainment = entertainment
        self.closet = closet
        self.dresser1 = dresser1
        self.dresser2 = dresser2
        
                    
                    
#create main player
#main = Player(100, 0, 1, False, False, False, False, False)
main = Player(100, 0, 1, "MR", True, True, True, True, True, False)
                    
#create list for all the rooms in the mansion
mansion.append(Room("MR", False, 1, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0)) # main room
mansion.append(Room("B1", False, 1, 10, 7, 0, 0, 1, 0, 0, 0, 0, 1, 0, 0, 0, 0)) # bathroom 1
mansion.append(Room("G1", False, 1, 3, 0, 0, 1, 0, 0, 0, 0, 0, 0, 0, 1, 3, 1)) # guest room 1
mansion.append(Room("LR", False, 1, 4, 0, 0, 0, 0, 0, 0, 0, 5, 2, 0, 0, 0, 0)) # living room
mansion.append(Room("KI", False, 1, 4, 1, 1, 0, 1, 1, 6, 1, 0, 0, 0, 0, 0, 0))
#find out if second floor stairs are going to be declared as a room or not
mansion.append(Room("MB", True, 2, 1, 1, 1, 1, 0, 0, 0, 0, 0, 0, 0, 1, 1, 1)) # master bedroom
mansion.append(Room("G2", False, 2, 3, 0, 0, 1, 0, 0, 0, 0, 0, 0, 0, 1, 1, 1)) # guest room 2
mansion.append(Room("G3", False, 2, 3, 0, 0, 1, 0, 0, 0, 0, 0, 0, 0, 1, 1, 1)) # guest room 3
mansion.append(Room("B2", False, 3, 10, 7, 0, 0, 1, 0, 0, 0, 0, 1, 0, 0, 0, 0)) # bathroom 2. it's on the "third floor" as a flag for having it be connected to G2 and G3. can't be accessed through SF
mansion.append(Room("SF", False, 2, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0)) # second floor main room
#find out if attic stairs are going to be declared as a room or not
mansion.append(Room("BB", False, 4, 10, 7, 0, 0, 1, 0, 0, 0, 0, 4, 0, 0, 0, 0)) # master bedroom bathroom. it's on the "fourth floor" as a flag for having it be connected to MB. it can't be accessed through SF

clearAndInsertText(healthStatus, str(main.health))

#initial prompt
insertText(output, "You wake up in a strange mansion. You try to leave, but the front door is locked. The knob, strangely, has a key hole. Perhaps you can explore the mansion to find the key.")
commandList()
place=0
#test text wrapping
#insertText(output, "TestTestTestTestTestTestTestTestTestTestTestTestTestTestTestTestTestTestTestTestTestTestTestTestTestTestTestTestTestTestTestTestTestTestTestTestTestTestTestTestTestTestTestTestTestTestTestTestTestTestTestTestTestTestTestTestTestTestTestTestTestTestTestTestTestTestTestTest")   
def locToInt(command, place):
    match (command):
        case "MR":
            place=0
        case "B1":
            place=1
        case "G1":
            place=2
        case "LR":
            place=3
        case "KI":
            place=4
        case "MB":
            place=5
        case "G2":
            place=6
        case "G3":
            place=7
        case "B2":
            place=8
        case "SF":
            place=9
        case "BB":
            place=10

def checkFight (chance):
    chanceFight = random.randint(1, chance)
    
    if chanceFight == 1:
        return 50
    else:
        return 0

#function for pressing button, it checks the input string and funnels it into the repsective command function
zombieHealth=0
def pressChoose():
    if main.health <= 0:
        showinfo(title='Player Lost!', message='You lost! Restart the game to try again')
    inputText = textGrab.get().upper() # upper cased the input statement in case a certain function is case sensitive
    print(inputText)
    global place
    global zombieHealth
    
    if zombieHealth > 0 and not "FIGHT" in inputText:
        clearAndInsertText(output, "You need to fight the zombie before you do anything else! Use 'fight [MOVE]' to fight the zombie!")
        fightCommands(main.knife)
        return
            
    match (inputText):
        case inputText if "ENTER" in inputText:
            match (inputText):
                #add floor check to know if you could enter the room or not
                case inputText if "MR" in inputText:
                    place=0
                    move=pointsMR
                case inputText if "B1" in inputText:
                    place=1
                    move=pointsB1
                    zombieHealth = checkFight(mansion[1].ratio)
                case inputText if "G1" in inputText:
                    place=2
                    move=pointsG1
                    zombieHealth = checkFight(mansion[2].ratio)
                    #zombieHealth = 50
                case inputText if "LR" in inputText:
                    place=3
                    move=pointsLR
                    zombieHealth = checkFight(mansion[3].ratio)
                case inputText if "KI" in inputText:
                    place=4
                    move=pointsKI
                    zombieHealth = checkFight(mansion[4].ratio)
                case inputText if "MB" in inputText:
                    place=5
                    move=pointsMB
                    zombieHealth = checkFight(mansion[5].ratio)
                case inputText if "G2" in inputText:
                    place=6
                    move=pointsG2
                    zombieHealth = checkFight(mansion[6].ratio)
                case inputText if "G3" in inputText:
                    place=7
                    move=pointsG3
                    zombieHealth = checkFight(mansion[7].ratio)
                case inputText if "B2" in inputText:
                    place=8
                    move=pointsB2
                    zombieHealth = checkFight(mansion[8].ratio)
                case inputText if "SF" in inputText:
                    place=9
                    move=pointsSF
                    zombieHealth = checkFight(mansion[9].ratio)
                case inputText if "BB" in inputText:
                    place=10
                    move=pointsBB
                    zombieHealth = checkFight(mansion[10].ratio)
                case _:
                    place=100
            if (place == 100):
                clearAndInsertText(output, "You either did not specify a room or did not specify a room correctly.\nPlease use the following syntax: enter [ROOM] (for example: enter G1)")
            else:
                main.location = mansion[place].command
                miniMap.coords(location, *move)
                if (place == 0):
                    clearAndInsertText(output, "You make it back to the Main Room. There are a number of closed doors ahead of you")
                    commandList()
                elif (place == 1 or place == 8 or place == 10):
                    clearAndInsertText(output, "You make it into a bathroom. There is a drawer (drawer1), cabinet (cabinet1), and a storage closet (storage)")
                    commandList()
                elif (place == 2 or place == 6 or place == 7):
                    clearAndInsertText(output, "You make it into a guest room. There are two dressers (dresser1, dresser2), a bed (bed), and a closet (closet)")
                    commandList()
                elif (place == 9):
                    clearAndInsertText(output, "You make it back to the main room. There are a number of closed doors ahead of you")
                    commandList()
                elif (place == 3):
                    clearAndInsertText(output, "You make it to the living room. There is a couch (couch) and entertainment center (entertainment)")
                    commandList()
                elif (place == 5):
                    clearAndInsertText(output, "You make it to the master bedroom. There are two dressers (dresser1, dresser2), a bed (bed), a bathroom (enter BB), and a closet (closet)")#find a way to lock this closet
                    commandList()
                elif (place == 4):
                    clearAndInsertText(output, "You make it to the kitchen. There are 2 drawers (drawer1, drawer2), 3 cabinets (cabinet1, cabinet2, cabinet3), and an oven (oven)")
                
        case inputText if "CHECK" in inputText:
            clearAndInsertText(output, f"You chose to check an object")
            locToInt(main.location, place)
            if "DRESSER1" in inputText:
                mansion[place].dresser1 = main.check(mansion[place].dresser1, main.kitchen_key)
            elif "DRESSER2" in inputText:
                mansion[place].dresser2 = main.check(mansion[place].dresser2, main.kitchen_key)
            elif "DRAWER1" in inputText:
                mansion[place].drawer1 = main.check(mansion[place].drawer1, main.kitchen_key)
            elif "DRAWER2" in inputText:
                mansion[place].drawer2 = main.check(mansion[place].drawer2, main.kitchen_key)
            elif "BED" in inputText:
                mansion[place].bed = main.check(mansion[place].bed, main.kitchen_key)
            elif "CABINET1" in inputText:
                mansion[place].cabinet1 = main.check(mansion[place].cabinet1, main.kitchen_key)
            elif "CABINET2" in inputText:
                mansion[place].cabinet2 = main.check(mansion[place].cabinet2, main.kitchen_key)
            elif "CABINET3" in inputText:
                mansion[place].cabinet3 = main.check(mansion[place].cabinet3, main.kitchen_key)
            elif "STORAGE" in inputText:
                mansion[place].storage = main.check(mansion[place].storage, main.kitchen_key)
            elif "OVEN" in inputText:
                mansion[place].oven = main.check(mansion[place].oven, main.kitchen_key)
            elif "COUCH" in inputText:
                mansion[place].couch = main.check(mansion[place].couch, main.kitchen_key)
            elif "ENTERTAINMENT" in inputText:
                mansion[place].entertainment = main.check(mansion[place].entertainment, main.kitchen_key)
            elif "CLOSET" in inputText:
                mansion[place].closet = main.check(mansion[place].closet, main.kitchen_key)
        case inputText if "HEAL" in inputText:
            clearAndInsertText(output, "You chose to heal")
            main.heal()
        case inputText if "UP" in inputText:
            main.up()
        case inputText if "DOWN" in inputText:
            down(main.level)
        case inputText if "HELP" in inputText:
            commandList()
        case inputText if "FGUIDE" in inputText:
            fightCommands(main.knife)
        case inputText if "FIGHT" in inputText:
            while zombieHealth > 0 and main.health > 0:
                if "PUNCH" in inputText:
                    hitChance = random.randint(1,5)
                    if hitChance != 1:
                        damage = random.randint(1,3) * 10
                        zombieHealth -= damage
                    else:
                        insertText(output, "You missed!")
                elif "KICK" in inputText:
                    hitChance = random.randint(1,2)
                    if hitChance != 1:
                        damage = random.randint(3,5) * 10
                        zombieHealth -= damage
                    else:
                        insertText(output, "You missed!")
                elif "SHOVE" in inputText:
                    zombiehealth -= 10
                elif "SLASH" in inputText and main.knife == True:
                    hitChance = random.randint(1,10)
                    if hitChance != 1:
                        damage = random.randint(2,4) * 10
                        zombieHealth -= damage
                        
                else:
                    clearAndInsertText(output, "You did not input it correctly!")
                    break
                
                main.health -= 5
                
                insertText(output, "Your health: " + str(main.health) + " zombie health: " + str(zombieHealth))
                    
        case _:
            clearAndInsertText(output, "Your input wasn't understood. Make sure you have the right syntax")
    
    if (zombieHealth > 0):
        clearAndInsertText(output, "You ran into a zombie! Choose one of the options below:\n")
        fightCommands(main.knife)
    elif main.health <= 0:
        clearAndInsertText(output, "You died! Thanks for playing")
    
    clearAndInsertText(healthStatus, str(main.health))
    
    
    inputText = ""
    

    
            

# input button. it's at the bottom because the command it calls has to be declared before it
buttonStyle = ttk.Style()
buttonStyle.configure("buttonStyle.TButton", background=bg_color, bd=0, highlightthickness=0)
inputButton = ttk.Button(root, text='', command=pressChoose, style='buttonStyle.TButton')
inputButton.place(x=570, y=350, height=20, width=30)

root.mainloop()