import pandas as pd
import datetime
import sys
import pymysql
import copy
import os

###############################################################################
#                           Constraints by Admin Area
###############################################################################
class constraints():
    
    def __init__(self):
        return None
    
    days_for_alert = ["Monday", "Tuesday", "Saturday"]
    alert_times = [800]
    
    #SQL withdrawing rules for a unit to update admin area
    def withdraw_awards_constraints(self):
        return None
    def withdraw_evals_constraints(self):
        return None
    #FUTURE CHANGES Stage two of project will be to draw the admin_area with rules from a DB
###############################################################################
#                                 DATABASE TOOLS
###############################################################################  
class db_tools():
    def __init__(self):
        self.db_user = "DB USERNAME"
        self.db_pass = "DB PASS"
        self.db_name = "DB NAME"
        self.host = "127.0.0.1"
        self.port = 3306
        self.db_payload = {"user": self.db_user, 
                           "pass": self.db_pass, 
                           "name": self.db_name, 
                           "host": self.host,
                           "port": self.port}
        
    def query_db(self, action, db_payload):
        # Connect to the database.
        connection = pymysql.connect(host=db_payload["host"],
                             user=db_payload["user"],
                             password=db_payload["pass"],                             
                             db=db_payload["name"],
                             port=db_payload["port"])
        try:
            with connection.cursor() as cursor:
                sql = action
                cursor.execute(sql)
                connection.commit()
                return cursor
        finally:
            connection.close()
        
###############################################################################
#                                 EXCEL TOOLS
###############################################################################
class excel_tools():
    #Each admin_area will also have a constraints function detailing the logic which will be packaged within the dictionary
    #Each excel tool will have an admin wrapper in charge of extracting data from each worksheet
    def __init__(self):
        return None
    
    def open_excel(self, link, sheet):
        #implement try statement
        df = pd.read_excel(io=link, sheet_name=sheet)
        return df
    
    def make_updates(self, old_tracker, new_tracker, match_word, changeable_categories, file, sheet):
        for index, row in new_tracker.iterrows():
            #WALKER, AARON MATTHEW
            if len(old_tracker.loc[old_tracker[match_word] == row[match_word]]) > 0:
                for column in changeable_categories:
                    #Locate new name in old tracker
                    if (old_tracker.loc[old_tracker[match_word] == 
                        row[match_word], column].values[0] != row[column]):
                        #Update old tracker with new value
                        old_tracker.loc[old_tracker[match_word] == row[match_word], column] = row[column]
            else:
                #Convert row into dataframe from series and transpose it to match old_tracker
                row = pd.DataFrame(row); row = row.T
                old_tracker = pd.concat([old_tracker, row], ignore_index=True, sort=False)
        old_tracker.to_excel(file, sheet_name=sheet, index=False)
        #Figure out how to have the tracker stick with the original column format
        #Figure out how to restore the color format


###############################################################################
#                                  Admin
###############################################################################   
class admin_tools():
    
    def __init__(self):
        return None
    

    dl = db_tools()
    directive = {}
    uic_directive = {}
    directive_list = []
    
    select_relevant_contacts_query = """SELECT contact_info.email, contact_info.phone_number, contact_info.smtp_gateway,
                                     pax.rank, pax.last_name, uic.uic, uic.nomenclature, contact_info.pax_id
                                     FROM contact_info 
                                     INNER JOIN pax ON pax.id = contact_info.pax_id 
                                     INNER JOIN pax_to_uic ON pax_to_uic.pax_id = pax.id 
                                     INNER JOIN uic ON uic.id = pax_to_uic.uic_id"""
    select_alert_preferences = """SELECT * FROM pax_to_alerts"""
    select_day_preferences = """SELECT * FROM days_to_pax_alerts"""
    #WHERE uic.uic="WAWYEO" OR uic.uic="WAWYTO" 
    
    def awards_constraints(self):
        admin_area = {
            "function": "awards",
            #Time to begin notification
            "starting_count": 175,
            #Where the link is on the computer, our program will NOT hold the file
            "document_link": "../../Downloads/awards.",
            #Word that should be in the excel spreadsheet to assume its done and ignore for further alerts
            "complete_keyword": ["Court Martial- ETS complete", "COMPLETE", "Complete- Pending Presentation", "PENDING CHAPTER", "Pending Chapter", "INVESTIGATION", "Flagged", "Complete", 
                                 "Pending Cert", "Pending Presentation- PAST REPORT DATE", 
                                 "Pending Presentation", "Complete, pending presenation", "638 signed; pending cert"],
            #columns array
            "timestamp_col_name": "PROJ LOSS",
            #Data that the loop will go and pick and store in admin awards array
            "descriptive_arr": ["UNIT", "RANK", "NAME", "STATUS"],
            #award status
            "remarks_name": "STATUS",
            
            "uic_name": "UNIT"
        }
        return admin_area
    
    def eval_constraints(self):
        admin_area = {
            "function": "evals",
            #Time to begin notification
            "starting_count": 45,
            #Where the link is on the computer, our program will NOT hold the file
            "document_link": "../../Downloads/evals.",
            #Word that should be in the excel spreadsheet to assume its done and ignore for further alerts
            "complete_keyword": ["Submitted to HQDA", "SUBMITTED TO HQDA", "submitted to hqda", "COMPLETE", "Complete", "W/ EXAMINER", "w/ examiner", "W/ Examiner", "complete"],
            #columns array
            "timestamp_col_name": "NEXT THRU DATE",
            #Data that the loop will go and pick and store in admin awards array
            "descriptive_arr": ["UNIT", "Rank", "Name", "REMARKS"],
            #award status
            "remarks_name": "REMARKS",
            
            "uic_name": "UNIT"
        }
        return admin_area
    
    def appointment_constraints(self):
        admin_area = {
            "function": "appointments",
            #Time to begin notification
            "starting_count": 7,
            #Where the link is on the computer, our program will NOT hold the file
            "document_link": "../../Downloads/evals.",
            #Word that should be in the excel spreadsheet to assume its done and ignore for further alerts
            "complete_keyword": ["Complete", "COMPLETE"],
            #columns array
            "timestamp_col_name": "APPOINTMENT DATE/TIME",
            #Data that the loop will go and pick and store in admin awards array
            "descriptive_arr": ["UIC", "RANK", "PATIENT", "STATUS"],
            #award status
            "remarks_name": "STATUS",
            
            "uic_name": "UIC"
        }
        return admin_area
    
    def zoarep_constraints(self):
        admin_area = {
            "function": "zoarep",
            #Time to begin notification
            "starting_count": 2,
            #Where the link is on the computer, our program will NOT hold the file
            "document_link": "../../Downloads/evals.",
            #Word that should be in the excel spreadsheet to assume its done and ignore for further alerts
            "complete_keyword": ["Complete", "COMPLETE"],
            #columns array
            "timestamp_col_name": "Net days",
            #Data that the loop will go and pick and store in admin awards array
            "descriptive_arr": ["Issuing Storage Loc.", "Net days", "Description", "UdQty"],
            #award status
            "remarks_name": "Description",
            
            "uic_name": "Issuing Storage Loc."              
        }
        return admin_area
    
    def dispatch_constraints(self):
        admin_area = {
            "function": "dispatch",
            #Time to begin notification
            "starting_count": 5,
            #Where the link is on the computer, our program will NOT hold the file
            "document_link": "../../Downloads/evals.",
            #Word that should be in the excel spreadsheet to assume its done and ignore for further alerts
            "complete_keyword": ["Complete", "COMPLETE"],
            #columns array
            "timestamp_col_name": "Created on",
            #Data that the loop will go and pick and store in admin awards array
            "descriptive_arr": ["Admin No.", "Description of technical object"],
            #award status
            "remarks_name": "Description of technical object",
            
            "uic_name": "Issuing Storage Loc."              
        }
        return admin_area
    
    def services_constraints(self):
        admin_area = {
            "function": "services",
            #Time to begin notification
            "starting_count": 7,
            #Where the link is on the computer, our program will NOT hold the file
            "document_link": "../../Downloads/evals.",
            #Word that should be in the excel spreadsheet to assume its done and ignore for further alerts
            "complete_keyword": ["Complete", "COMPLETE", "Completed", "COMPLETED"],
            #columns array
            "timestamp_col_name": "Late Date",
            #Data that the loop will go and pick and store in admin awards array
            "descriptive_arr": ["Admin No.", "Description of technical object", "Maintenance item description"],
            #award status
            "remarks_name": "Description of technical object",
            
            "uic_name": "Main work center"              
        }
        return admin_area

    def grab_unique_uics(self, admin_list, uic_pos): #position of uic in row; always 0
        uic_list = []
        for row in admin_list:
            if row[uic_pos] not in uic_list:
                uic_list.append(row[uic_pos])
        return uic_list
        
    
    #Filter out complete, investigation, pending cert keywords 
    def exists_complete_entries(self, entries, admin_type):
        if admin_type == "award":
            admin_area = self.awards_constraints()
        if admin_type == "evaluation":
            admin_area = self.eval_constraints()
        if admin_type == "appointment":
            admin_area = self.appointment_constraints()
        if admin_type == "zoa":
            admin_area = self.zoarep_constraints()
        for keyword in admin_area["complete_keyword"]:
            if keyword in entries:
                return True
            else:
                return False

    def filter_contacts_by_uic(self, uic_list, admin_list, action, admin_type):
        action += ' WHERE'
        for uic in uic_list:
            action += ' uic.uic='+"'"+uic+"'"+' OR'
        action = action[:-2] #Get rid of last OR
        filtered_contacts = list(self.dl.query_db(action, dl.db_payload))
        return filtered_contacts
    
    def filter_contacts_by_alert_preference(self, contact_list, alert_preference, action):
        tmp_contact_list = []
        for index, row in enumerate(contact_list):
            action_tmp = action
            action_ammendment = ' WHERE pax_to_alerts.alert_id='+"'"+alert_preference+"'"+' AND pax_to_alerts.pax_id ='+"'"+str(row[7])+"'"
            action_tmp += action_ammendment
            filtered_contacts = list(self.dl.query_db(action_tmp, dl.db_payload))
            action_tmp = ''; action_ammendment = ''
            if len(filtered_contacts) > 0:
                return tmp_contact_list
    
    def filter_contacts_by_day_preference(self, contact_list, alert_preference, action):
        days_list = ["Monday", "Tuesday", "Wednesday", 
                     "Thursday", "Friday", "Saturday", 
                     "Sunday"]
        from datetime import datetime as date
        hoy = date.today().strftime("%A")
        tmp_contact_list = []
        day_id = str(days_list.index(hoy)+1)
        for index, contact_row in enumerate(contact_list):
            action_tmp = action
            pax_id = str(contact_list[index][-1:][0])
            action_ammendment = ' WHERE day_id ='+"'"+day_id+"'"+' AND pax_id='+"'"+pax_id+"'"+' AND alert_id='+"'"+alert_preference+"'"
            action_tmp += action_ammendment
            filtered_contacts = list(self.dl.query_db(action_tmp, dl.db_payload))
            action_tmp = ''; action_ammendment = ''
            if len(filtered_contacts) > 0:
                tmp_contact_list.append(contact_row)
        return tmp_contact_list
                
    #Going further: add a function, filter_alerts_by_platoon
    def filter_alerts_by_uic(self, uic_list, admin_list, contact_list, admin_type):
        uic_dict = {}
        #Check which admin file it is
        if admin_type == "award":
            admin_area = self.awards_constraints()
        if admin_type == "evaluation":
            admin_area = self.eval_constraints()
        if admin_type == "appointment":
            admin_area = self.appointment_constraints()
        avail_uic = []
        #Check the UICs in your contact list and see which ones are in uic_list
        avail_uic = [entry for contact in contact_list
                     for entry in contact if entry in uic_list]
        uniq_uic = [] #Having multiple same UICs causes same message to be stored that many times
        for uic in avail_uic:
            if uic not in uniq_uic:
                uniq_uic.append(uic)       
        avail_uic = uniq_uic #unique list of UICs
        #Check which rows in admin_list have the uic's from contact_list
        for index, admin_row in enumerate(admin_list):
            for uic in avail_uic:
                if uic in admin_row:
                    uic_dict.setdefault(uic, []).append(admin_row)
        return uic_dict
    
    #Sort the upcoming admin dates by hottest, day_pos_arr is the index where the day is located in arr
    def sort_closest_dates(self, admin_list, day_pos_arr):
        admin_list.sort(key=lambda x: x[day_pos_arr])
        return admin_list
    
    def reverse_sort_dates(self, admin_list, day_pos_arr):
        admin_list.sort(key=lambda x: x[day_pos_arr], reverse=True)
        return admin_list
    
    def zoarep_msg_creator(self, zoa_list):
        msg = ""
        for index, item in enumerate(zoa_list):
            msg += item[0]+" - Day "+str(item[1])+" - "+item[2]+" - Qty: "+str(round(item[3],0))+"\n\n"
            
        return msg
    
    def dispatch_msg_creator(self, dis_list):
        msg = ""
        for index, item in enumerate(dis_list):
            msg += item[0]+" - Day: "+str(item[2])+" - Desc: "+item[1]+"\n\n"
        return msg
    
    def service_msg_creator(self, ser_list):
        msg = ""
        for index, row in enumerate(ser_list):
            for item in row:
                msg += item[0]+" - Day: "+str(item[3])+" - Desc: "+item[1]+" -Type: "+item[2]+"\n\n"
        return msg
        
    def determine_num_days(self, today, date_cell):
        from datetime import date
        try:
            date_cell = pd.Timestamp(date_cell) #In case date_cell is str & not pd.timestamp
        except ValueError:
            print("This date is bad:" + date_cell)
            raise
        d2 = date_cell.to_pydatetime(date_cell)
        d2 = date(d2.year, d2.month, d2.day)
        num_days = (today-d2).days
        return num_days
    
    def determine_num_days_reverse(self, today, date_cell):
        from datetime import date
        try:
            date_cell = pd.Timestamp(date_cell) #In case date_cell is str & not pd.timestamp
        except ValueError:
            print("This date is bad:" + date_cell)
            raise
        d2 = date_cell.to_pydatetime(date_cell)
        d2 = date(d2.year, d2.month, d2.day)
        num_days = (d2-today).days
        return num_days
    ##########################################################################
    ########################   AWARDS WRAPPER   ##############################
    ##########################################################################
    def calculate_due_dates(self, frame_data, admin_type):
        admin_list = []
        admin_area = ''
        from datetime import datetime, date
        if admin_type == "award":
            admin_area = self.awards_constraints()
        if admin_type == "evaluation":
            admin_area = self.eval_constraints()
        if admin_type == "appointment":
            admin_area = self.appointment_constraints()
        today = date.today()
        #Find which dates meet "starting_count" criteria
        for index, date_cell in enumerate(frame_data[admin_area["timestamp_col_name"]]):
            #If there is no date available
            if pd.isnull(date_cell):
                continue
            #If data avail, subtract from todays date to see if it meets "starting_count"
            else:
                num_days = self.determine_num_days(today, date_cell)
                col_collect = []
                #Find out who is within day range and who does not have a complete keyword
                if num_days <= admin_area["starting_count"] and frame_data[admin_area["remarks_name"]][index] not in admin_area["complete_keyword"]:
                    for col in frame_data[admin_area["descriptive_arr"]]:
                        #If an award is complete or investigation, keep going
                        col_collect.append(frame_data[col][index])
                    col_collect.append(num_days)
                    admin_list.append(col_collect)
                    col_collect = []
        return admin_list
    
    def calculate_dispatch_days(self, frame_data, admin_type):
        admin_list = []
        admin_area = ''
        if admin_type == "dispatch":
            admin_area = self.dispatch_constraints()
        from datetime import datetime, date
        today = date.today()
        #Find which dates meet "starting_count" criteria
        for index, date_cell in enumerate(frame_data["Created on"]):
            #If there is no date available
            if pd.isnull(date_cell):
                continue
            #If data avail, subtract from todays date to see if it meets "starting_count"
            else:
                num_days = self.determine_num_days(today, date_cell)
                col_collect = []
                #Find out who is within day range and who does not have a complete keyword
                if num_days > 3:
                    for col in frame_data[admin_area["descriptive_arr"]]:
                        #If an award is complete or investigation, keep going
                        col_collect.append(frame_data[col][index])
                    col_collect.append(num_days)
                    admin_list.append(col_collect)
                    col_collect = []
        return admin_list
    
    def calculate_zoarep_days(self, frame_data, days_notif):
        admin_list = []
        admin_area = ''
        admin_area = self.zoarep_constraints()
        for index, date_cell in enumerate(frame_data[admin_area["timestamp_col_name"]]):
            if pd.isnull(date_cell):
                continue
            else:
                col_collect = []
                if date_cell > days_notif:
                    for col in frame_data[admin_area["descriptive_arr"]]:
                        if pd.isna(frame_data[col][index]):
                            break
                        else:
                            col_collect.append(frame_data[col][index])
                    admin_list.append(col_collect)
                    col_collect = []
        admin_list = [x for x in admin_list if len(x) > 0]

        return admin_list
    
    def calculate_service_days(self, frame_data, days_notif):
        admin_list = []
        admin_area = ''
        admin_area = self.services_constraints()
        from datetime import datetime, date
        today = date.today()
        for index, date_cell in enumerate(frame_data[admin_area["timestamp_col_name"]]):
            if pd.isnull(date_cell):
                continue
            else:
                col_collect = []
                num_days = self.determine_num_days_reverse(today, date_cell)
                if num_days < 7:
                    for col in frame_data[admin_area["descriptive_arr"]]:
                        if pd.isna(frame_data[col][index]):
                            break
                        else:
                            col_collect.append(frame_data[col][index])
                    col_collect.append(num_days)
                    admin_list.append(col_collect)
                    col_collect = []
                    
        admin_list = [x for x in admin_list if len(x) > 0]

        return admin_list

    #convert contact_list into easy to use recipient list dictionaried by UICs
    def contact_to_recipient_list(self, contact_list):
        #If you acquire your own SMTP server, you may have to redo this code to eliminate SMTP gateways
        contact_dict = {}
        for contact in contact_list:
            if contact[0] != '0':
                contact_dict.setdefault(contact[5], []).append(contact[0]) #email
            if contact[1] != '0':
                contact_dict.setdefault(contact[5], []).append(contact[1]+contact[2]) #phone, possible changes in future
        return contact_dict
    
    def alert_to_message_list(self, alert_list, admin_type):
        message_list = {}
        msg = ''
        for uic in alert_list:
            for row in alert_list[uic]:
                if admin_type == "award" or admin_type == "evaluation":
                    msg = self.message_creator(row, admin_type)
                if admin_type == "appointment":
                    msg = self.appt_message_creator(row, admin_type)
                if len(msg) > 0: #In case messages are empty such as appts that are no longer relevant
                    message_list.setdefault(uic, []).append(msg)
        return message_list
        
            
    #This function will format our awards message for the text
    def message_creator(self, alert_list_row, admin_type):
        #Feed a row into this function, so []
        award_msg = ''
        alr = alert_list_row
        if int(alr[4]) == 0:
            award_msg = alr[1]+" "+alr[2]+ " " + admin_type +" is due today."
        elif int(alr[4]) == 1:
            award_msg = alr[1]+" "+alr[2]+ " " + admin_type +" is due in "+str(alr[4])+" day."
        elif int(alr[4]) == -1:
            award_msg = alr[1]+" "+alr[2]+ " " + admin_type +" is past due "+str(abs(alr[4]))+" day."
        elif int(alr[4]) > -1:
            award_msg = alr[1]+" "+alr[2]+ " " + admin_type +" is due in "+str(alr[4])+" days."
        else:
            award_msg = alr[1]+" "+alr[2]+ " " + admin_type +" is past due "+str(abs(alr[4]))+" days."
        return award_msg
    
    def appt_message_creator(self, alert_list_row, admin_type):
        appt_msg = ''
        alr = alert_list_row
        if int(alr[4]) == 0:
            appt_msg = alr[1]+" "+alr[2]+ " has an appointment today."
        return appt_msg

    #Tags contacts with their respective alert message
    def prepare_contact_directive(self, recipients, message_list):
        #If phone number and char limit is nearing 160 characters
        msg_compiled = ''
        msg_compiled_arr = []
        char_count = 0
        for uic in recipients:
            for contact in recipients[uic]:
                identifier = contact.split('@')[0] #Grab everything before @ symbol
                if identifier.isdecimal():
                    for row in message_list[uic]:
                        char_count += len(row)
                        #if text exceeds this amount
                        if char_count > 1599:
                            msg_compiled_arr.append(msg_compiled)
                            msg_compiled = ''
                            msg_compiled += row + ' \n'
                            msg_compiled += ' \n'
                            char_count = 0
                        else:     
                            msg_compiled += row + ' \n'
                            msg_compiled += ' \n'
                    msg_compiled_arr.append(msg_compiled)
                    msg_compiled = ''
                    self.directive.setdefault(contact, []).append(msg_compiled_arr)
                    self.uic_directive.setdefault(contact, []).append([uic])
                    msg_compiled_arr = []
                else:
                    for row in message_list[uic]:
                        msg_compiled += row + ' \n'
                        msg_compiled += ' \n'
                    msg_compiled_arr.append(msg_compiled)
                    msg_compiled = ''
                    self.directive.setdefault(contact, []).append(msg_compiled_arr)
                    self.uic_directive.setdefault(contact, []).append([uic])
                    msg_compiled_arr = []
                    
    def pad_contact_directive(self, contacts_msgs, dir_uic_list):
        final_msg = []
        #final_msg = np.concatenate(final_msg, msg)
        for index, msg in enumerate(contacts_msgs):
            new_msg = dir_uic_list[index][0]+" \n" + msg[0]
            final_msg.extend([new_msg])
        return final_msg
    
    def delete_recipients_not_in_msg_list(self, recipients, message_list):
        tmp_recipients = {}
        tmp_recipients = recipients.copy()
        for uic in tmp_recipients:
            if uic not in message_list:
                del recipients[uic]
    
###############################################################################
#                                  Text Cannon
###############################################################################
class text_cannon():
    
    def __init__(self):
        return None
    
    def establish_connection(self, smtp_addr, port, user, passw):
        import smtplib
        smtpObj = smtplib.SMTP('smtp.gmail.com', 587)
        smtpObj.ehlo()
        smtpObj.starttls()
        smtpObj.login('email', 'Login')
        return smtpObj
    
    def build_message(self, mail_content, sender_addr, receiver_addr, sub):
        from email.mime.multipart import MIMEMultipart
        from email.mime.text import MIMEText
        message = MIMEMultipart()
        message['From'] = sender_addr
        message['To'] = receiver_addr
        message['Subject'] = sub
        message.attach(MIMEText(mail_content, 'plain'))
        text = message.as_string()
        return text
    
    def send_email(self, connection, built_message, sender_addr, receiver_addr):
        connection.sendmail(sender_addr, receiver_addr, built_message)
        print("Mail Sent")
    
    def kill_connection(self, connection):
        connection.quit()
        #This is the code; break it up into functions
        
###############################################################################
#                                  Troubleshooting
###############################################################################
class troubleshooting():
    
    def __init__(self):
        return None
    
    dl = db_tools()
    
    def initiate_directive_test_mode(self, test_contacts, directive):
        key_list = []
        alt_directive = {}
        alt_directive = directive.copy() #Must copy or you will change original
        counter = 0
        #Collect Keys
        for index, directive_row in enumerate(directive):
            for contact_name in directive_row:
                key_list.append(contact_name)
            counter = index
        for key in key_list:
            if key not in test_contacts:
                for num in range(counter+1):
                    if key in alt_directive[num]:
                        alt_directive[num].pop(key)
        return alt_directive
    
    def insert_alert_preferences(self, pax_id, alert_id):
        select_action = 'SELECT * FROM pax_to_alerts WHERE alert_id='+"'"+alert_id+"'"+" AND pax_id="+"'"+pax_id+"'"
        insert_action = 'INSERT INTO `pax_to_alerts`(`alert_id`, `pax_id`) VALUES ('+"'"+alert_id+"'"+','+"'"+pax_id+"'"+')'
        select_res = len(list(self.dl.query_db(select_action, dl.db_payload)))
        if select_res == 0:
            self.dl.query_db(insert_action, dl.db_payload)
            print("New Alert Added")
        else:
            print("This User Already Has This Alert")
            
    def insert_days_preference(self, pax_id, alert_id, day_id):
        select_action = 'SELECT * FROM days_to_pax_alerts WHERE alert_id='+"'"+alert_id+"'"+" AND pax_id="+"'"+pax_id+"'"+" AND day_id="+"'"+day_id+"'"
        insert_action = 'INSERT INTO `days_to_pax_alerts`(`day_id`, `pax_id`, `alert_id`) VALUES ('+"'"+day_id+"'"+','+"'"+pax_id+"'"+','+"'"+alert_id+"'"+')'
        select_res = len(list(self.dl.query_db(select_action, dl.db_payload)))
        if select_res == 0:
            self.dl.query_db(insert_action, dl.db_payload)
            print("New Day Preference Added")
        else:
            print("This User Already Has This Day Preference Set") 
    
    def delete_days_preference(self, pax_id, alert_id, day_id):
        select_action = 'SELECT * FROM days_to_pax_alerts WHERE alert_id='+"'"+alert_id+"'"+" AND pax_id="+"'"+pax_id+"'"+" AND day_id="+"'"+day_id+"'"
        delete_action = 'DELETE FROM `days_to_pax_alerts` WHERE `day_id`='+"'"+day_id+"'"+ ' AND `pax_id`='+"'"+pax_id+"'"+ ' AND `alert_id`='+"'"+alert_id+"'"
        select_res = len(list(self.dl.query_db(select_action, dl.db_payload)))
        if select_res == 0:
            self.dl.query_db(delete_action, dl.db_payload)
            print("Delete Successful Added")
        else:
            print("No Preference Set to Delete") 
            

        

    
#Execute classes
cx = constraints()
xl = excel_tools()
aw = admin_tools()
dl = db_tools()
tc = text_cannon()
trshoot = troubleshooting()
#Admin_type names
awards_name = "award"; awards_num = 1
eval_name = "evaluation"; eval_num = 2
appt_name = "appointment"; appt_num = 3
alert_categories = ["AWARD", "EVALUATION", "APPOINTMENT"]

dir_list = []
dir_uic_list = []
m_list = []
#TROUBLESHOOT
#pax, alert
#trshoot.insert_alert_preferences("10", "2")
#trshoot.insert_alert_preferences("6", "2")
#trshoot.insert_alert_preferences("9", "3")
"""
for i in range(1, 6):
    #pax, alert, day
    trshoot.insert_days_preference(pax_id="30", alert_id="3", day_id=str(i))
"""
#pax, alert, day
"""
for i in range(1, 6):
    trshoot.insert_days_preference(pax_id="1", alert_id="4", day_id=str(i))
"""
###############################################################################
#                          EXECUTE AWARDS DIRECTIVE
###############################################################################

awards_data = xl.open_excel("Awards Tracker Location", "Awards Tracker Title")
award_list = aw.calculate_due_dates(awards_data, awards_name); award_list = aw.sort_closest_dates(award_list, 4)
uic_list = aw.grab_unique_uics(award_list, 0)
contact_list = aw.filter_contacts_by_uic(uic_list, awards_data, aw.select_relevant_contacts_query, awards_name)
contact_list = aw.filter_contacts_by_alert_preference(contact_list, str(awards_num), aw.select_alert_preferences)
contact_list = aw.filter_contacts_by_day_preference(contact_list, str(awards_num), aw.select_day_preferences)
alert_list = aw.filter_alerts_by_uic(uic_list, award_list, contact_list, awards_name)
recipients = aw.contact_to_recipient_list(contact_list)
message_list = aw.alert_to_message_list(alert_list, awards_name) 
m_list.append(copy.deepcopy(message_list))
aw.delete_recipients_not_in_msg_list(recipients, message_list)
if len(message_list) == 0:
    print("No messages to send for "+awards_name)
else:
    aw.prepare_contact_directive(recipients, message_list) #Will store to class var directives
    dir_list.append(copy.deepcopy(aw.directive))
    dir_uic_list.append(copy.deepcopy(aw.uic_directive))
    aw.directive.clear()
    aw.uic_directive.clear()

###############################################################################
#                          EXECUTE EVALUATION DIRECTIVE
###############################################################################

eval_data = xl.open_excel("Rating Scheme Location", "Rating Scheme Title")
eval_list = aw.calculate_due_dates(eval_data, eval_name); eval_list = aw.sort_closest_dates(eval_list, 4)
uic_list = aw.grab_unique_uics(eval_list, 0) #row position of where UIC is located
contact_list = aw.filter_contacts_by_uic(uic_list, eval_data, aw.select_relevant_contacts_query, eval_name)
contact_list = aw.filter_contacts_by_alert_preference(contact_list, str(eval_num), aw.select_alert_preferences)
contact_list = aw.filter_contacts_by_day_preference(contact_list, str(eval_num), aw.select_day_preferences)
alert_list = aw.filter_alerts_by_uic(uic_list, eval_list, contact_list, eval_name)
recipients = aw.contact_to_recipient_list(contact_list)
message_list = aw.alert_to_message_list(alert_list, eval_name)
m_list.append(copy.deepcopy(message_list))
aw.delete_recipients_not_in_msg_list(recipients, message_list)
if len(message_list) == 0:
    print("No messages to send for "+eval_name)
else:
    aw.prepare_contact_directive(recipients, message_list) #Will store to class var directives
    dir_list.append(copy.deepcopy(aw.directive))
    dir_uic_list.append(copy.deepcopy(aw.uic_directive))
    aw.directive.clear()
    aw.uic_directive.clear()

###############################################################################
#                           EXECUTE APPOINTMENTS DIRECTIVE
###############################################################################

appt_data = xl.open_excel("Appointment file location", "Appointment File Title")
appt_list = aw.calculate_due_dates(appt_data, appt_name); appt_list = aw.sort_closest_dates(appt_list, 4)
uic_list = aw.grab_unique_uics(appt_list, 0) #row position of where UIC is located
contact_list = aw.filter_contacts_by_uic(uic_list, appt_data, aw.select_relevant_contacts_query, appt_name)
contact_list = aw.filter_contacts_by_alert_preference(contact_list, str(appt_num), aw.select_alert_preferences)
contact_list = aw.filter_contacts_by_day_preference(contact_list, str(appt_num), aw.select_day_preferences)
alert_list = aw.filter_alerts_by_uic(uic_list, appt_list, contact_list, appt_name)
recipients = aw.contact_to_recipient_list(contact_list)
message_list = aw.alert_to_message_list(alert_list, appt_name)
m_list.append(copy.deepcopy(message_list))
aw.delete_recipients_not_in_msg_list(recipients, message_list)

if len(message_list) == 0:
    print("No messages to send for "+appt_name)
else:
    aw.prepare_contact_directive(recipients, message_list) #Will store to class var directives
    dir_list.append(copy.deepcopy(aw.directive))
    dir_uic_list.append(copy.deepcopy(aw.uic_directive))
    aw.directive.clear()
    aw.uic_directive.clear()

###############################################################################
#                           TEST ON SELECT CONTACTS
###############################################################################

#test_contacts = ["Insert your email here"]
dir_list = trshoot.initiate_directive_test_mode(test_contacts, dir_list)
dir_uic_list = trshoot.initiate_directive_test_mode(test_contacts, dir_uic_list)


###############################################################################
#                           **LAUNCH TEXT CANNON**
###############################################################################
#import sys
#sys.exit()
import time
con = tc.establish_connection('smtp.gmail.com', 587, 
                              'Email', 
                              'Password')
for index, directive in enumerate(dir_list):
    for msg_info, contact in enumerate(dir_list[index]):
        #If this is a master account
        msg_holder = ''
        if len(dir_list[index][contact]) > 1:
            final_message = ''
            message = aw.pad_contact_directive(dir_list[index][contact], dir_uic_list[index][contact])
            for msg in message:
                msg_holder += msg
            msg = tc.build_message(msg_holder, #this is the message
                             "Email",
                             contact,
                             alert_categories[index]+" ALERT")
        #If this is a single account
        else:
            msg = tc.build_message(dir_list[index][contact][0][0], #this is the message
                                   "Email",
                                   contact,
                                   alert_categories[index]+" ALERT")
        tc.send_email(con, msg, "Email", contact)
        time.sleep(1)
tc.kill_connection(con) 


###############################################################################
#                           UPDATE ORIGINAL
###############################################################################
original_file = "#Link to Awards Tracker"
original_sheet = "1-43 ADA"
amended_file = ""
amended_sheet = "1-43 ADA"
original_data = xl.open_excel(original_file, original_sheet)
amended_data = xl.open_excel(amended_file, amended_sheet)

change_arr = ["RANK", "PROJ LOSS", "AWARD", "STATUS"]
identifier_col = "NAME"
xl.make_updates(original_data, amended_data, 
               identifier_col, change_arr, 
               original_file, original_sheet)

#2. Make function that checks for faulty dates and scales the date back till conditon satisfied
#3. Make a UI that can change peoples alert preferences, add people, and a log in
#4. Begin NLP model
#SGT Guerrero evals is past due 1 days is wrong
