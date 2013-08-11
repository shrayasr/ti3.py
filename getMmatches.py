import urllib2
import sys
from BeautifulSoup import BeautifulSoup

def dumpMatchLinks(url,dumpFile):

    f = open(dumpFile,'w')

    page = urllib2.urlopen(url)
    soup = BeautifulSoup(page.read())

    games = soup.findAll('div',{'class':'scheduleGameRow'})

    totalNoOfGames =  len(games)

    matchProcessing = 0

    for game in games:

        p1 = game.find('div',{'class':'sgrTeamAName'}).text
        p2 = game.find('div',{'class':'sgrTeamBName'}).text
        matchLink = game.find('div',{'class':'sgrMatch'}).find('a')['href']
        matchLinkEnglish = ""
        matchCasters=""

        matchProcessing = matchProcessing + 1

        print "Processing " + str(matchProcessing) + " of "+ str(totalNoOfGames)

        page = urllib2.urlopen(matchLink)
        soup = BeautifulSoup(page)

        iframe = soup.find('iframe')

        if (iframe == None):
           continue 

        iframeHref = iframe['src']

        watchId = iframeHref[iframeHref.rfind('/')+1:]

        dumpLine = "##"+p1+" vs "+p2+"\n"+"[Link](http://youtube.com/watch?v="+watchId+")\n\n"
        f.write(dumpLine)


matchFile = sys.argv[1]

with open(matchFile) as f:
    matches = f.readlines()

for match in matches:
    matchURL = match.split(" ")[0].rstrip()
    matchDumpFile = match.split(" ")[1].rstrip()

    dumpMatchLinks(matchURL,matchDumpFile)
