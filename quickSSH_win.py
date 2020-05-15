import os, sys, paramiko
import tkinter.messagebox
from scp import SCPClient
from tkinter import *
from PIL import ImageTk, Image

__author__ = "The One & Only Javi"
__version__ = "1.0.0"
__start_date__ = "June 2019"
__end_date__ = ""
__maintainer__ = "me"
__email__ = "little_kh@hotmail.com.com"
__requirements__ = "tkinter, Pillow, SSH access"
__status__ = "Testing on different OS"
__description__ = "This script creates a software that launches SSH commands"



window = Tk()
window.title('SSH Remote Support Software 1.0 BETA Windows Version')
window.geometry("1000x320")

# Insert here the credentials, WATCH OUT!
port = 22
username = 'root'
password = ''



# main function to bypass SSH orders
def print_output(order):
    global ssh
    t2.delete("1.0", END)  # we erase the buffer_file after each call
    try:
        ssh = paramiko.SSHClient()
        ssh.load_system_host_keys()
        ssh.connect(e1_value.get() + '.yourdomain.com', port, username, password)
        stdin, stdout, stderr = ssh.exec_command(order)
        stdoutstring = stdout.readlines()
        t2.insert(END, stdoutstring)

    finally:
        ssh.close()

def execute_not_print(order):
    global ssh
    t2.delete("1.0", END)  # we erase the buffer_file after each call
    try:
        ssh = paramiko.SSHClient()
        ssh.load_system_host_keys()
        ssh.set_missing_host_key_policy(paramiko.AutoAddPolicy())
        ssh.connect(e1_value.get() + '.yourdomain.com', port, username, password)
        stdin, stdout, stderr = ssh.exec_command(order)

    finally:
        ssh.close()

def download():
    ssh = paramiko.SSHClient()
    ssh.load_system_host_keys()
    ssh.set_missing_host_key_policy(paramiko.AutoAddPolicy())
    ssh.connect(e1_value.get() + '.yourdomain.com', port, username, password)
    # SCPCLient takes a paramiko transport as an argument
    scp = SCPClient(ssh.get_transport())
    # we read the outputs, as we can't download more than 1 file
    stdin, stdout, stderr = ssh.exec_command('ls /var/tmp/test-*.mp4')
    file_list = stdout.read().split()
    for listed_file in file_list:
        scp.get(listed_file)
        scp.close()

# Indivual functions for each button
def list_num_pend_upload():
    order = 'ls /home/user/record | wc -l'
    print_output(order)
#WORKS

def list_pend_upload():
    order = 'ls /home/user/record'
    print_output(order)
#WORKS

def list_rec_channels():
    order = 'bash /usr/lib/check_mk_agent/plugins/rec_channels'
    print_output(order)
#WORKS

def dvbrecd_restart():
    order = 'service dvbrecd restart'
    execute_not_print(order)
#Creates restart but doesn't start

def streams_restart():
    order = 'bash /home/user/restartStoppedStreams.sh'
    print_output(order)
#WORKS

def analogtvd_restart():
    order = 'service analogtvd restart'
    execute_not_print(order)
    data = "Done! Please check again in 5 minutes"
    t2.insert(END, data)
#WORKS

def analogtvd_testrecord():
    t2.delete("1.0", END)
    # da muchos problemas!!!
    order = 'bash /home/user/newconfig/check_channels.sh'
    tkinter.messagebox.showinfo(message="Please check after 5 minutes", title="Command launched")
    execute_not_print(order)
    download()
    data = "Done!"
    t2.insert(END, data)
#Hace restart pero no graba

def dvbrecd_testrecord():
    t2.delete("1.0", END)
    # It gives a lot of errors launching this script through SSH
    tkinter.messagebox.showinfo(message="Warning! Don't close the program while it does the operation"
                                "\nPlease wait until a new window appears",
                                title="Command launched")
    order = 'bash /home/user/newconfig/check_dvb_channels.sh'
    print_output(order)
    download()
    tkinter.messagebox.showinfo(message="Done! Please check files in same folder", title="Command launched")
    data = "Done!"
    t2.insert(END, data)
#WORKS

def reboot_server():
    t2.delete("1.0", END)
    # we ask a question to proceed
    result = tkinter.messagebox.askquestion("Rebooting sever",
                                            "Are You Sure?\n\nYou can lose access to the server\n\nPlease proceed "
                                            "only if necessary",
                                            icon='warning')
    if result == 'yes':
        order = 'shutdown -rf now && exit'
        print_output(order)
        data = "Setup rebooted"
        t2.insert(END, data)
    else:
        t2.delete("1.0", END)
        data = "Setup not rebooted"
        t2.insert(END, data)
#WORKS

# Frontend buttons, each calls operation
b1 = Button(window, text="List number of files pending to upload (rec folder)", bg='IndianRed2', fg='snow',
            command=list_num_pend_upload)
b1.grid(row=1, column=0)

b2 = Button(window, text="List files pending to upload (rec folder)", bg='IndianRed2', fg='snow',
            command=list_pend_upload)
b2.grid(row=2, column=0)

b3 = Button(window, text="List channels being recorded", bg='IndianRed2', fg='snow', command=list_rec_channels)
b3.grid(row=3, column=0)

b4 = Button(window, text="Restart Digital TV & IPTV recording", bg='IndianRed2', fg='snow', command=dvbrecd_restart)
b4.grid(row=4, column=0)

b5 = Button(window, text="Restart streams recording", bg='IndianRed2', fg='snow', command=streams_restart)
b5.grid(row=5, column=0)

b6 = Button(window, text="Restart Analog TV recording", bg='IndianRed2', fg='snow', command=analogtvd_restart)
b6.grid(row=6, column=0)

b7 = Button(window, text="Record 10 seconds Analog TV", bg='IndianRed2', fg='snow', command=analogtvd_testrecord)
b7.grid(row=7, column=0)

b8 = Button(window, text="Record 10 seconds Digital TV & IPTV module", bg='IndianRed2', fg='snow',
            command=dvbrecd_testrecord)
b8.grid(row=8, column=0)

b9 = Button(window, text="Reboot recording unit", bg='IndianRed2', fg='snow', command=reboot_server)
b9.grid(row=9, column=0)

# IMPORTANT: entry of text by user
e1_value = StringVar()
e1 = Entry(window, textvariable=e1_value)
e1.grid(row=0, column=1)

l1 = Label(window, text="Please insert the recording unit name here ->")
l1.grid(row=0, column=0)

# Outputs of the operations!
t2 = Text(window, height=1, width=100)

t2.grid(row=1, column=1, rowspan=20, columnspan=8, sticky=W + E + N + S, padx=5, pady=5)
# BMAT Logo
logo_path = 'company_logo.jpg'
img = ImageTk.PhotoImage(Image.open("company_logo.jpg"))
# imglabel = Label(window, image=img).grid(row=0, column=3, rowspan=5, sticky=W+E+N+S, padx=5, pady=5)
imglabel = Label(window, image=img).grid(row=0, column=3, sticky=E + N, rowspan=10)

# C.pack()
window.mainloop()

