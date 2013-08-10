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

        castLinks = soup.findAll('a',{'class':'lgbCasterLink'})

        for castLink in castLinks:

            castLinkText = castLink.text.lower().strip()

            if "english" in castLinkText:
                matchLinkEnglish = castLink['href']
                matchCasters = castLinkText.split(":")[1]

        dumpLine = "##"+p1+" vs "+p2+"\n"+"["+matchCasters+"]("+matchLinkEnglish+")\n\n"
        f.write(dumpLine)

matchFile = sys.argv[1]

with open(matchFile) as f:
    matches = f.readlines()

for match in matches:
    matchURL = match.split(" ")[0]
    matchDumpFile = match.split(" ")[1]

    dumpMatchLinks(matchURL,matchDumpFile)
