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
from selenium.webdriver.common.by import By
import tkinter as tk
from tkinter import messagebox


# -15 for the name of this project Work_Unforeseen
# save_path = dirname(__file__)[ : -15]
save_path = os.path.dirname(os.path.abspath("__file__"))
propertiesFolder_path = save_path + "\\"+ "Properties"

test = False # If False, start the clock else if True We are in test mode => not start the clock

j.epic_link = tools.readProperty(propertiesFolder_path, 'Work_Unforeseen', 'epic_link=')
j.save_path = tools.readProperty(propertiesFolder_path, 'Work_Unforeseen', 'save_path=')
sn.incident_change_id = tools.readProperty(propertiesFolder_path, 'ServiceNow', 'incident_change_id=')
sn.user_name = tools.readProperty(propertiesFolder_path, 'ServiceNow', 'user_name=')

userJira = tools.readProperty(propertiesFolder_path, 'JIRA', 'userJira=')
# passJira = tools.readProperty(propertiesFolder_path, 'JIRA', 'passJira=')
teamName = tools.readProperty(propertiesFolder_path, 'JIRA', 'teamName=')
reporterName = tools.readProperty(propertiesFolder_path, 'JIRA', 'reporterName=')
assigneeName = tools.readProperty(propertiesFolder_path, 'JIRA', 'assigneeName=')
j.sprint = tools.readProperty(propertiesFolder_path, 'Work_Unforeseen', 'sprint=')

# Open Browser
tools.openBrowserChrome()

# MyHours part
m.connectToMyTimeTrack()

# afficher une popup expliquant qu'il faut se connecter une première fois
# Et installer l'extension chrome pour retenir les users et password
def show_popup():
    root = tk.Tk()
    root.withdraw()  # Hide the root window
    messagebox.showinfo("Information", "Please connect for the first time and install the Chrome extension to remember the users and passwords.")
    root.destroy()


print ("Test if we need to wait the page of the user / password")
if tools.waitLoadingPageByID2(5, 'email-label') :
    # show_popup()
    # print ("Need to wait the page of the password")
    # tools.waitLoadingPageByID2(10, 'email-label')
    # time.sleep(30)
    m.enterCredentials2()

# Force refresh the page
tools.driver.refresh()

# Click on the current run
m.startTrack2()
time.sleep(1)

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
    tools.driver.get("https://jira.atlassian.insim.biz/browse/TF-5880")
    # j.connectToJiraInsim('TOS-5454', userJira)
    # j.loginToJira('https://jira.atlassian.insim.biz/login.jsp?nosso', userJira, passJira)
else :
    tools.driver.get("https://jira-test.atlassian.insim.biz/browse/TF-5880")
    # j.connectToJiraInsim('TOS-5454', userJira)
    # j.loginToJira('https://jira-test.atlassian.insim.biz/login.jsp?nosso', userJira, passJira)
    
# Create a new JIRA
j.createJira("RUN - " + sn.incident_change_id + " - " + sn.incidentTitle, sn.description_text, sn.incident_change_id, teamName, reporterName, assigneeName)

# Need to open the JIRA just created
j.openJira("RUN - " + sn.incident_change_id + " - " + sn.incidentTitle)

# Need to recovered the identifier of the jira
tools.waitLoadingPageByID("key-val")
j.jira = tools.driver.find_element(By.ID, "key-val").get_attribute('data-issue-key').encode('utf-8').decode()

print("JIRA = " + j.jira)

# Need to recovered Information
j.recoverJiraInformation()

# Create folder link to this JIRA
j.createFolderJira(j.jira)
j.createFileInto(j.jira, j.jiraTitle, j.description_text, j.jira, j.jira + "_Comment_v001")

# Update MyHours
m.connectToMyTimeTrack()

print ("Test if we need to wait the page of the user / password")
if tools.waitLoadingPageByID2(5, 'email-label') :
    # show_popup()
    # print ("Need to wait the page of the password")
    # tools.waitLoadingPageByID2(10, 'email-label')
    # time.sleep(30)
    m.enterCredentials2()

# Force refresh the page
tools.driver.refresh()
# Click on the current run
m.startTrack2()

print ("Click on the current run")     
m.startTrackWithDescription2(j.jira, j.jira + ' - ' + j.jiraTitle, j.epic_link)
time.sleep(1)

# 
tools.openFolder(j.save_path + j.jira)
tools.openFile(j.save_path + j.jira + '/' + j.jira + '_Comment_v001.txt')

# Exit Chrome
tools.driver.quit()