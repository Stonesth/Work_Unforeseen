from Tools import tools_v000 as tools
from Topdesk import topdesk as t
from Jira import jira as j
from MyHours import myhours as m
import os
from os.path import dirname
import time


# -15 for the name of this project Work_Unforeseen
save_path = dirname(__file__)[ : -15]
propertiesFolder_path = save_path + "Properties"

test = True # If False, start the clock else if True We are in test mode => not start the clock

j.epic_link = tools.readProperty(propertiesFolder_path, 'Work_Unforeseen', 'epic_link=')
j.save_path = tools.readProperty(propertiesFolder_path, 'Work_Unforeseen', 'save_path=')
t.incidentNumber = tools.readProperty(propertiesFolder_path, 'Work_Unforeseen', 'incidentNumber=')
t.sprint = tools.readProperty(propertiesFolder_path, 'Work_Unforeseen', 'sprint=')
j.jira = tools.readProperty(propertiesFolder_path, 'Work_Unforeseen', 'jira=')

# Open Browser
tools.openBrowserChrome()

# Start MyHours
if test != True :
    print ("Start the clock for the ticket")
    m.connectToMyHours()
    m.enterCredentials()
    m.startTrack()
else :
    print ("We are in test mode - no start new time")

# TopDesk part
t.connectViaLink()
t.incidentTitle()

# Jira part
if test != True :
    j.connectToJira(j.jira)
else :
    j.connectToJiraTST(j.jira)

j.recoverJiraInformation()

# # Place a comment into the JIRA and saved it
# # click on the button footer-comment-button
j.commentButton()

# # Place a comment
time.sleep(1)
j.placeTheTextIntoComment(t.incidentNumber, t.incidentTitle)

# # Add the comment
j.addComment() 

# Create folder link to this JIRA
j.createFolderJira(j.jira)
j.createFileInto(j.jira, j.jiraTitle, t.incidentNumber + " - " + t.incidentTitle + "\n" + "https://nnbe.topdesk.net/tas/secure/incident?action=lookup&lookup=naam&lookupValue=" + t.incidentTitle + "\n")

# Start MyHours
if test != True :
    m.connectToMyHours()
    m.enterCredentials()
    m.modifyTrack(j.jira, j.jira + ' - ' + j.jiraTitle, j.epic_link)
else :
    print ("We are in test mode - no start new time")

# 
tools.openFolder(j.save_path + j.jira)
tools.openFile(j.save_path + j.jira + '/' + j.jira + '_Comment_v001.txt')

# Send mail to Menno Spelbos


# Exit Chrome
tools.driver.quit()