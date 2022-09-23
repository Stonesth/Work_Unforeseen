#!/usr/bin/python
# -*- coding:utf-8 -*-
from Tools import tools_v000 as tools
# from Topdesk import topdesk as t
from Jira import jira as j
from MyHours import myhours as m
from ServiceNow import servicenow as sn
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
sn.user_name = tools.readProperty(propertiesFolder_path, 'ServiceNow', 'user_name=')
sn.incident_change_id = tools.readProperty(propertiesFolder_path, 'ServiceNow', 'incident_change_id=')

userJira = tools.readProperty(propertiesFolder_path, 'JIRA', 'userJira=')
passJira = tools.readProperty(propertiesFolder_path, 'JIRA', 'passJira=')
teamName = tools.readProperty(propertiesFolder_path, 'JIRA', 'teamName=')
reporterName = tools.readProperty(propertiesFolder_path, 'JIRA', 'reporterName=')
assigneeName = tools.readProperty(propertiesFolder_path, 'JIRA', 'assigneeName=')

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

# ServiceNow part
sn.connectToServiceNow(sn.user_name)
time.sleep(1)
sn.connectToServiceNowIncidentChange(sn.incident_change_id)
sn.collectData()

print("Caller = ", sn.caller)
print("incidentTitle = ", sn.incidentTitle )
print("description_text = ", sn.description_text )

# Jira part
if test != True :
    j.loginToJira('https://jira.atlassian.insim.biz/login.jsp?nosso', userJira, passJira)
else :
    j.loginToJira('https://jira-test.atlassian.insim.biz/login.jsp?nosso', userJira, passJira)
    
# Create a new JIRA
j.createJira("RUN - " + sn.incident_change_id + " - " + sn.incidentTitle, sn.description_text, sn.incident_change_id, teamName, reporterName, assigneeName)

# Need to open the JIRA just created
j.openJira("RUN - " + sn.incident_change_id + " - " + sn.incidentTitle)

# Need to recovered the identifier of the jira
tools.waitLoadingPageByID("key-val")
j.jira = tools.driver.find_element_by_id("key-val").get_attribute('data-issue-key').encode('utf-8')

print("JIRA = " + j.jira)

# Need to recovered Information
j.recoverJiraInformation()

# Create folder link to this JIRA
j.createFolderJira(j.jira)
j.createFileInto(j.jira, j.jiraTitle, j.description_text, j.jira, j.jira + "_Comment_v001")

# Update MyHours
m.connectToMyHours()

# Click on the current run
print ("Click on the current run")                     
timeStep1 = tools.driver.find_element_by_xpath('/html/body/div[1]/div/div/track-page/div/div[5]/div/div[2]')
timeStep1.click()    
time.sleep(2)

m.modifyTrack(j.jira, j.jira + ' - ' + j.jiraTitle, j.epic_link)

# 
tools.openFolder(j.save_path + j.jira)
tools.openFile(j.save_path + j.jira + '/' + j.jira + '_Comment_v001.txt')

# Exit Chrome
tools.driver.quit()