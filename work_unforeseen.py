#!/usr/bin/python
# -*- coding:utf-8 -*-
from Tools import tools_v000 as tools
from Topdesk import topdesk as t
from Jira import jira as j
from MyHours import myhours as m
import os
from os.path import dirname
import time


# -15 for the name of this project Work_Unforeseen
# save_path = dirname(__file__)[ : -15]
save_path = os.path.dirname(os.path.abspath("__file__"))
propertiesFolder_path = save_path + "\\"+ "Properties"

test = False # If False, start the clock else if True We are in test mode => not start the clock

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
time.sleep(1)

# Create folder link to this JIRA
j.createFolderJira(j.jira + '/' + t.incidentNumber)
if (t.incidentNumber.startswith("I")) :
    j.createFileInto(j.jira, j.jiraTitle, t.incidentNumber + " - " + t.incidentTitle + "\n" + "https://nnbe.topdesk.net/tas/secure/incident?action=lookup&lookup=naam&lookupValue=" + t.incidentNumber + "\n", j.jira + '/' + t.incidentNumber, j.jira + '_' + t.incidentNumber + "_Comment_v001")
else :
    j.createFileInto(j.jira, j.jiraTitle, t.incidentNumber + " - " + t.incidentTitle + "\n" + "https://nnbe.topdesk.net/tas/secure/newchange?action=lookup&lookup=number&lookupValue=" + t.incidentNumber + "\n", j.jira + '/' + t.incidentNumber, j.jira + '_' + t.incidentNumber + "_Comment_v001")

# Start MyHours
if test != True :
    print ("Update the clock with the ticket")
    m.connectToMyHours()
    m.modifyTrack(j.jira, j.jira + ' - ' + j.jiraTitle + ' - ' +  t.incidentNumber + ' - ' + t.incidentTitle, j.epic_link)
else :
    print ("We are in test mode - no start new time")

# 
tools.openFolder(j.save_path + j.jira + '\\' + t.incidentNumber)
tools.openFile(j.save_path + j.jira + '/' + t.incidentNumber + '/' + j.jira + '_' +  t.incidentNumber + '_Comment_v001.txt')

# Send mail to Menno Spelbos


# Exit Chrome
tools.driver.quit()