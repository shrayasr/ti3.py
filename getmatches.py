import urllib2
from BeautifulSoup import BeautifulSoup

def getMatchLinks(url,dumpFile):

    f = open(dumpFile,'w')

    gamesData = []

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

        print "Processing " + matchProcessing + " of "+totalNoOfGames

        page = urllib2.urlopen(matchLink)
        soup = BeautifulSoup(page)

        castLinks = soup.findAll('a',{'class':'lgbCasterLink'})

        for castLink in castLinks:

            castLinkText = castLink.text.lower().strip()

            if "english" in castLinkText:
                matchLinkEnglish = castLink['href']
                matchCasters = castLinkText.split(":")[1]

        gameData = {
                "p1":p1,
                "p2":p2,
                "match_link":matchLinkEnglish
        };

        dumpLine = "##"+p1+" vs "+p2+"\n"+"["+matchCasters+"]("+matchLinkEnglish+")\n\n"
        f.write(dumpLine)

        gamesData.append(gameData)

getMatchLinks('http://www.dota2.com/international/prelims/schedule/saturday/','saturday.md')
