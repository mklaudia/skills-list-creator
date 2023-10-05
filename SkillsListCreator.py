#import queue
import logging

#0-5
minimumStars = 0
#0-x, 0 means no filtering
maxListLength = 50

inputFileName = "lists/skillsListShortExample.txt"
resultFileName = "result.txt"

class Skill:
    def __init__(self, item):
        self.topic = None
        self.subtopic = None
        self.item = item
        self.stars = 0
        self.priority = 0
        self.hidden = 0
        self.bfAdd = 0
        self.half = 0
    
    def __str__(self):
        t = str(self.topic)
        t += " - " + str(self.subtopic)
        t += " - " + self.item
        t += " -- stars: " + str(self.stars)
        t += " / " + getStarChars(self.stars)
        t += " priority: " + str(self.priority)
        t += " hidden: " + str(self.hidden)
        t += " bfAdd: " + str(self.bfAdd)
        t += " half: " + str(self.bfAdd)
        return t
        
    def getFormattedText(self):
        return getStarChars(self.stars, self.half) + " " + self.item
        
def getStarChars(numStars, half = 0):
#    print((b'\x2BE8\xa9').decode("utf-16"))
#    print((b'\x2BE8').decode("utf-8"))
#    print((b'\x2605').decode("utf-8"))
#    print((b'black star: \xE2\x98\x85').decode("utf-8"))
#    print((b'black star: \x05\x26').decode("utf-16"))
#    print((b'half black star: \xE2\xAF\xA8').decode("utf-8"))
#   # print((b'half black star: \xE8\x2B').decode("utf-16"))
#    print((b'love: \xF0\x9F\x92\x93').decode("utf-8"))
    
    if numStars > 5 : numStars = 5
    elif numStars < 0: numStars = 0
    if half == 1 & numStars > 0 :
        return((numStars-1)*"★" + (b'\xE2\xAF\xA8').decode("utf-8") + (5-numStars) * "☆")
    return(numStars * "★" + (5-numStars) * "☆")
    
def getSkillsListFromFile(fileName):
    skillsList = list()
    with open(fileName) as file:
        for line in file:
            print(line)
            s = line.rstrip().partition(":")
            if s[0] == '' : continue
            #print(s[0])
            topic = s[0]
            s = s[2].partition(":")
            subtopic = None
            if s[2] != '':
                s = list(s)
                subtopic = s[0]
                logging.debug(subtopic)
                s[0] = s[2]
            s = s[0].split(";")
            logging.debug(s)
            #print(s)
            item = s[0]
            skill = Skill(s[0])
            
            def toNumber(x):
                if x == '':
                    return 0
                return int(x)
            
            print(s)
            s = list(map(lambda x: toNumber(x) , s[1:]))
            
            print(s)
            stars, priority, hidden, bfAdd, half, *_ = s + [0, 0, 0, 0, 0]
#            print(half)
            
            print(topic + '-' +str(subtopic) + '-' + item + str(stars) + str(priority) + str(hidden) + str(bfAdd) + str(half))
            
            
            skill.topic = topic
            skill.subtopic = subtopic
            skill.stars = stars
            skill.priority = priority
            skill.hidden = hidden
            skill.bfAdd = bfAdd
            skill.half = half
            skillsList.append(skill)
            print(skill)
            print(skill.getFormattedText())
        
        print("-----------------------------")
        for i in skillsList: print(i)
    return skillsList       

        
        #//stars (0-5), prirority (0-...), hidden(0: no, 1: yes), brute-force-add(0: no, 1: yes) when empty: 0
        #print(topic + "  -  " + stars)


skillsList = getSkillsListFromFile(inputFileName)

#sort by priority
skillsList.sort(key=lambda x: -x.priority)

#Filter by hidden
#warn if hidden and brute-force-add are both set to 1        
i =0
while i < len(skillsList):
    if skillsList[i].hidden == 1:
        if skillsList[i].bfAdd == 1:
            logging.warn("Warning, skill --" + str(skillsList[i]) + "-- is set to hidden AND brute-force-add at the same time! It will be ADDED to the final list.")
            i+=1
            continue
        del skillsList[i]
        i-=1
    i += 1       
    
#Filter by minimum stars but keep brute-force-adds
if minimumStars > 0:
    i =0
    while i < len(skillsList):
        if skillsList[i].stars < minimumStars:
            if skillsList[i].bfAdd == 1:
                logging.warn("Warning, skill --" + str(skillsList[i]) + "-- has less then " + str(minimumStars) + " stars but it is brute forced.")
                i+=1
                continue
            del skillsList[i]
            i-=1
        i += 1 
    
#Filter by max number but keep brute-force-adds
i = len(skillsList)
while i >= 0 & len(skillsList) > maxListLength:
    if skillsList[i].bfAdd ==1:
        logging.warn("Warning, skill --" + str(skillsList[i]) + "-- would be normally removed due to list max length but it is brute forced. The max length can be still ok.")
        i+=1
        continue
    del skillsList[i]
        
    i -= 1 

if len(skillsList) > maxListLength:
    logging.warn("The result list is longer (" + str(len(skillsList)) + ") then the desired length (" + str(maxListLength) + ") but all brute forced items are added.") 


print("-------********-----")
for i in skillsList: print(i)

#write to file
with open(resultFileName, 'w', encoding="utf-8") as file:
 #   for i in skillsList:
  #      file.writelines(getStarChars(i.stars) + " " + i.item)
    file.writelines(i.getFormattedText() + '\n' for i in skillsList)



input("Press Enter to continue...")
