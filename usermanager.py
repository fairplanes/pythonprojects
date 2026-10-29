users = {
    'admin':{'pass':'admin','level':'admin','notes':{},'messages':{}},
    'headadmin':{'pass':'password','level':'head_admin','notes':{},'messages':{}},
    'basic':{'pass':'password','level':'basic','notes':{},'messages':{}}
}

logs = [

]

messagelogs = [

]

basic_cmds = ['userinfo','logout','userlist','opennote','notelist','addnote','removenote','help','send','viewmessages']
admin_cmds = ['*adduser','*removeuser','*logs','*userlist','*help']
headadmin_cmds = ['**adduser','**removeuser','**changeperms','**messagelogs','**userlist','**help']
    
logged_in = False
admin = False
head_admin = False
currentuser = None

def basiccmds(cmd):
        if cmd == basic_cmds[0]:
            print(f"Username: {currentuser}\nPassword: {users[currentuser]['pass']}\nPermission level: {users[currentuser]['level']}")
        elif cmd == basic_cmds[1]:
            global logged_in
            logged_in = False
            logs.append(f"{currentuser}({users[currentuser]['level']}) logged out.")
        elif cmd == basic_cmds[2]:
            for user in users:
                print(user,'| ', users[user]['level'])
        elif cmd == basic_cmds[3]:
            if users[currentuser]['notes'] == {}:
                print("You don't have any notes.")
            else:
                opennote = str(input("Which note would you like to open?: "))
                if opennote == '':
                    print("You need to open a note.")
                elif opennote not in users[currentuser]['notes']:
                    print("This note does not exist.")
                else:
                    print(f'notename {opennote}\n',users[currentuser]['notes'][opennote])
        elif cmd == basic_cmds[4]:
            print('\n'.join(list(users[currentuser]['notes'].keys())))
        elif cmd == basic_cmds[5]:
            notename = str(input("What would you like to name this note?: "))
            if notename in users[currentuser]['notes'].keys():
                print("There is already a note with this name.")
            elif notename == '':
                print("Your note needs to have a name.")
            else:
                notecontents = str(input("What would you like to put in this note?: "))
                if notecontents == '':
                    print("Your note needs to have contents.")
                else:
                    users[currentuser]['notes'].update({notename:notecontents})
                    logs.append(f'{currentuser} added a note {notename}.')
                    print(f"{notename} created successfully.")
        elif cmd == basic_cmds[6]:
            removenote = str(input("Which note would you like to remove?:"))
            if removenote not in users[currentuser]['notes']:
                print("This note does not exist.")
            elif removenote == '':
                print("You need to remove a note.")
            else:
                del users[currentuser]['notes'][removenote]
                logs.append(f'{currentuser} removed note {removenote}.')
                print(f"{removenote} removed successfully.")
        elif cmd == basic_cmds[7]:
            print('help: your current page.\nuserinfo: gives you your current user information.\nlogout: logs you our of your user.\nuserlist: gives you a list of all current users.')
            print('opennote: opens a given note in your user.\nremovenote: removes a given note from your user.\naddnote: add a new note to your user.\nnotelist: gives you a list of notes.')
            print('send: allows you to send a message to another user.\nviewmessages: views messages sent to you.')
        elif cmd == basic_cmds[8]:
            recipient = str(input("Recipient: "))
            contents = str(input("Contents: "))
            if recipient not in users:
                print("This user doesn't exist.")
            elif recipient == currentuser:
                print("You can't send messages to yourself.")
            else:
                users[recipient]['messages'].update({currentuser:contents})
                print("Message sent!")
                messagelogs.append(f"{currentuser} sent a message to {recipient}: {contents}")
        elif cmd == basic_cmds[9]:
            if len(users[currentuser]['messages']) == 0:
                print("You have no messages.")
            else:
                for sender, message in users[currentuser]['messages'].items():
                    print(f"{sender} sent you a message: {message}")


def admincmds(cmd):
    if cmd == admin_cmds[0]:
        addusername = str(input("Username: "))
        if addusername in users:
            print("This user already exists.")
        else:
            addpass = str(input("Password: "))
            users.update({addusername:{'pass':addpass,'level':'basic','notes':{},'messages':{}}})
            logs.append(f'{currentuser} added user {addusername}.')
    elif cmd == admin_cmds[1]:
        removeuser = str(input("Username: "))
        if removeuser not in users:
            print("This user does not exist.")
        elif removeuser == currentuser:
            print("You cannot remove yourself.")
        elif users[removeuser]['level'] != 'basic':
            print("You can't remove this user.")
        else:
            del users[removeuser]
            logs.append(f"{currentuser} removed {removeuser}.")
    elif cmd == admin_cmds[2]:
        print('\n'.join(logs))
    elif cmd == admin_cmds[3]:
        for user in users:
            if users[user]['level'] == 'basic':
                print(f'{user} | {users[user]['pass']} | basic')
            else:
                print(f"{user} | {users[user]['level']}")
    elif cmd == admincmds[4]:
        print('*help: your current page.\nuserinfo: gives you your current user information.\nlogout: logs you our of your user.\nuserlist: gives you a list of all current users.')
        print('opennote: opens a given note in your user.\nremovenote: removes a given note from your user.\naddnote: add a new note to your user.\nnotelist: gives you a list of notes.')
        print('send: allows you to send a message to another user.\nviewmessages: views messages sent to you.\n*adduser: adds a user of basic permission level.')
        print('*removeuser: removes a user of basic permission level.\n*logs: view login, logout, and user logs.\n*userlist: shows the user list with passwords of basic users visible.')

def headadmincmds(cmd):
    if cmd == headadmin_cmds[0]:
        adduser = str(input('Username: '))
        addpass = str(input("Password: "))
        permlevel = str(input('Permission level: '))
        if adduser in users:
            print("This user already exists.")
        elif permlevel != 'admin' and permlevel != 'basic':
            print("Invalid permission level.")
        else:
            users.update({adduser:{'pass':addpass,'level':permlevel,'notes':{},'messages':{}}})
            print(f"{adduser} added successfully.")
            logs.append(f"{currentuser} added {adduser} ({permlevel}).")
    elif cmd == headadmin_cmds[1]:
        removeuser = str(input("Username: "))
        if removeuser not in users:
            print("This user doesn't exist.")
        elif removeuser == currentuser:
            print("You cannot remove yourself.")
        else:
            del users[removeuser]
            logs.append(f"{removeuser} removed by {currentuser}")
    elif cmd == headadmin_cmds[2]:
        user = str(input("Username: "))
        if user not in users:
            print("This user doesn't exist.")
        elif user == currentuser:
            print("You cannot change permissions on yourself.")
        else:
            changeperm = str(input("New permission level: "))
            if changeperm != 'admin' and changeperm != 'basic':
                print("Invalid permission level.")
            else:
                users[user]['level'] = changeperm
                logs.append(f"{currentuser} changed {user} to {changeperm}.")
    elif cmd == headadmin_cmds[3]:
        print('\n'.join(messagelogs))
    elif cmd == headadmin_cmds[4]:
        for user in users:
            if users[user]['level'] != 'head_admin':
                print(f"{user} | {users[user]['pass']} | {users[user]['level']}")
            else:
                print(f"{users[user]} | {users[user]['level']}")
    elif cmd == headadmincmds[5]:
        print('**help: your current page.\nuserinfo: gives you your current user information.\nlogout: logs you our of your user.\nuserlist: gives you a list of all current users.')
        print('opennote: opens a given note in your user.\nremovenote: removes a given note from your user.\naddnote: add a new note to your user.\nnotelist: gives you a list of notes.')
        print('send: allows you to send a message to another user.\nviewmessages: views messages sent to you.\n**adduser: adds a user of basic or admin permission level.')
        print('**removeuser: removes a non head admin user,\n*logs: view login, logout, and user logs.\n**userlist: shows the user list with passwords of basic and admin users visible.')
        print('**messagelogs: view messages sent to users.\n**changeperms: change the permission level of a user to admin or basic.')
while True:
    while logged_in == False:
        userlogin = str(input("Username: "))
        loginpass = str(input("Password: "))
        if userlogin not in users:
         print("This user does not exist")
        else:
            if loginpass != users[userlogin]['pass']:
                print("Incorrect password.")
            else:
                if users[userlogin]['level'] == 'admin':
                    logged_in = True
                    admin = True
                    head_admin = False
                    currentuser = userlogin
                    logs.append(f"{userlogin} (admin) logged in.")
                elif users[userlogin]['level'] == 'head_admin':
                    head_admin = True
                    admin = False
                    logged_in = True
                    currentuser = userlogin
                    logs.append(f"{userlogin} (head_admin) logged in.")
                else:
                    logged_in = True
                    admin = False
                    head_admin = False
                    currentuser = userlogin
                    logs.append(f"{userlogin} (basic) logged in.")

    while logged_in == True and not admin and not head_admin:
        print(f"Welcome, {currentuser}. You have {len(users[currentuser]['messages'])} message(s).")
        cmd = str(input(''))
        if cmd in basic_cmds:
            basiccmds(cmd)
        else:
            print("This command doesn't exist.")

    while logged_in == True and admin and not head_admin:
        print(f"Welcome, {currentuser}. You have {len(users[currentuser]['messages'])} message(s).")
        cmd = str(input(''))
        if cmd in basic_cmds:
            basiccmds(cmd)
        elif cmd in admin_cmds:
            admincmds(cmd)
        else:
            print("This command doesn't exist.")

    while logged_in == True and not admin and head_admin:
        print(f"Welcome, {currentuser}. You have {len(users[currentuser]['messages'])} message(s).")
        cmd = str(input(''))
        if cmd in basic_cmds:
            basiccmds(cmd)
        elif cmd in admin_cmds:
            admincmds(cmd)
        elif cmd in headadmin_cmds:
            headadmincmds(cmd)
        else:
            print("This commmand doesn't exist.")
