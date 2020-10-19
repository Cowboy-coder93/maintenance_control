###############################################################################
#                           Initiate Application
############################################################################### 
from temp import (constraints, db_tools, 
excel_tools, admin_tools, text_cannon, troubleshooting)
import ezgmail, os
#Only needed if credentials.json and token.json arent available
#credentials can be accessed via link automate boring stuff
#token.json will be downloaded to directory once you run code below
cx = constraints()
xl = excel_tools()
aw = admin_tools()
dl = db_tools()
tc = text_cannon()
trshoot = troubleshooting()
contact = "Your phone number followed by SMTP gateway"
directive = []
directive_titles = []

os.chdir("Root directory")

ezgmail.init()
zoa_name = "zoarep"; zoa_num = 4
dis_name = "dispatch"; dis_num = 5
ser_name = "services"; ser_num = 6
alert_categories = ["ZOAREP", "DISPATCH", "SERVICES"]

dir_list = []
dir_uic_list = []
m_list = []
root_source = "Your root source; for linux type PWD"

unreadThreads = ezgmail.unread()

attachment_titles = ""

for email in unreadThreads:
    #email.markAsRead()
    email.messages[0].downloadAllAttachments(downloadFolder='.', overwrite=True)
    attachment_titles = email.messages[0].attachments

###############################################################################
#                           CREATE ALERTS
###############################################################################     
msg_arr = []
master_ser_list = []
service_titles = ['alpha.XLSX', 'bravo.XLSX', 'charlie.XLSX', 'delta.XLSX', 'echo.XLSX', 'hhb.XLSX']
for title in attachment_titles:
    #
    #Check services
    #
    if title in service_titles:
       ser_data = xl.open_excel(root_source+title, "Sheet1") 
       ser_list = aw.calculate_service_days(ser_data, 7)
       if len(ser_list) != 0:
           master_ser_list.append(ser_list)
       msg_block = aw.service_msg_creator(master_ser_list)
       if len(msg_block) > 0:
           msg_arr.append(msg_block)
           master_ser_list = []
    #
    #Dispatches
    #
    if title == "Overdue Dispatch.XLSX":
        msg_block = ''
        dis_data = xl.open_excel(root_source+title, "Sheet1")
        dis_list = aw.calculate_dispatch_days(dis_data, dis_name); dis_list = aw.reverse_sort_dates(dis_list, 2)
        msg_block = aw.dispatch_msg_creator(dis_list)
        directive_titles.append("Overdue Dispatches")
        directive.append(msg_block)
    #
    #ZOAREP
    #
    if title == "ZOAREP.XLSX":
        msg_block = ''
        zoa_data = xl.open_excel(root_source+title, "Sheet1")
        zoa_list = aw.calculate_zoarep_days(zoa_data, 3)
        uic_list = aw.grab_unique_uics(zoa_list, 0)
        msg_block = aw.zoarep_msg_creator(zoa_list)
        directive_titles.append("ZOAREP")
        directive.append(msg_block)

for msg in msg_arr:
    directive_titles.append("Overdue Services")
    directive.append(msg)


###############################################################################
#                          TEXT CANNON
###############################################################################
for index, msg in enumerate(directive):
    ezgmail.send(contact, directive_titles[index], msg)
    
#(1.) Ensure the raspberry pi has full compliance with the required libraries
#(2.) Create a folder on desktop that will hold all of our scripts.
#(3.) Learn how to create a cron job, call the sh script which points to our python script. 

