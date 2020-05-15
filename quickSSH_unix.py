import os
# from tkinter import ttk -> seems not to work with MacOs
# from tkmacosx import Button -> seems not to work with MacOs
import tkinter.messagebox
#import time
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
window.title('SSH Remote Support Software 1.0 BETA')
window.geometry("1200x800")

# Please insert here the path to an empty temp .txt file
buffer_file = '/Users/kh/Downloads/buffer.txt'


# main function to bypass SSH orders
# we use a text file because all the existing problems to redirect
# stdout into the widget. This way it works
def print_output(order):
    t2.delete("1.0", END)  # we erase the buffer_file after each call
    original = sys.stdout
    sys.stdout = open(buffer_file, 'w')
    command = os.popen(order)
    print(command.read())
    print(command.close())
    sys.stdout = original
    output_file = open(buffer_file, "r")
    data = output_file.read()
    t2.insert(END, data)

def download():
    command = os.popen('scp root@' + e1_value.get() + '.yourdomain.com:/var/tmp/test-*.mp4 /Users/$USER/Downloads/')

# Indivual functions for each button
def list_num_pend_upload():
    order = 'ssh root@' + e1_value.get() + '.yourdomain.com ls /home/user/record | wc -l'
    print_output(order)


def list_pend_upload():
    order = 'ssh root@' + e1_value.get() + '.yourdomain.com ls /home/user/record'
    print_output(order)


def list_rec_channels():
    order = 'ssh root@' + e1_value.get() + '.yourdomain.com /usr/lib/check_mk_agent/plugins/rec_channels'
    print_output(order)


def digital_tvrecd_restart():
    order = 'ssh root@' + e1_value.get() + '.yourdomain.com service digital_tvrecd restart'
    print_output(order)


def streams_restart():
    order = 'ssh root@' + e1_value.get() + '.yourdomain.com bash /home/user/restartStoppedStreams.sh'
    print_output(order)


def analogtvd_restart():
    order = 'ssh root@' + e1_value.get() + '.yourdomain.com service analogtvd restart'
    print_output(order)


def analogtvd_testrecord():
    # command = os.popen('ssh -o "StrictHostKeyChecking no" root@'+e1_value.get()+'.yourdomain.com bash /home/user/newconfig/check_channels.sh')
    command = os.popen('ssh root@' + e1_value.get() + '.yourdomain.com bash /home/user/newconfig/check_channels.sh')
    tkinter.messagebox.showinfo(message="Please check after 5 minutes", title="Command launched")
    download()
    data = "Done!"
    t2.insert(END, data)


def digital_tvrecd_testrecord():
    t2.delete("1.0", END)
    # It gives a lot of errors launching this script through SSH
    command = os.popen('ssh root@' + e1_value.get() + '.yourdomain.com bash /home/user/newconfig/check_digital_tv_channels.sh')
    tkinter.messagebox.showinfo(message="Please check after 5 minutes", title="Command launched")
    #time.sleep(300)
    download()
    data = "Done!"
    t2.insert(END, data)


def reboot_server():
    t2.delete("1.0", END)
    # we ask a question to proceed
    result = tkinter.messagebox.askquestion("Rebooting sever",
                                            "Are You Sure?\n\nYou can lose access to the server\n\nPlease proceed only if necessary",
                                            icon='warning')
    if result == 'yes':
        command = os.popen('ssh root@' + e1_value.get() + '.yourdomain.com shutdown -rf now && exit')
        data = "Setup rebooted"
        t2.insert(END, data)
    else:
        t2.delete("1.0", END)
        data = "Setup not rebooted"
        t2.insert(END, data)


# Frontend buttons, each calls operation
b1 = Button(window, text="List number of files pending to upload (rec folder)", command=list_num_pend_upload)
b1.grid(row=1, column=0)

b2 = Button(window, text="List files pending to upload (rec folder)", command=list_pend_upload)
b2.grid(row=2, column=0)

b3 = Button(window, text="List channels being recorded", command=list_rec_channels)
b3.grid(row=3, column=0)

b4 = Button(window, text="Restart Digital TV & IPTV recording", command=digital_tvrecd_restart)
b4.grid(row=4, column=0)

b5 = Button(window, text="Restart streams recording", command=streams_restart)
b5.grid(row=5, column=0)

b6 = Button(window, text="Restart Analog TV recording", command=analogtvd_restart)
b6.grid(row=6, column=0)

b7 = Button(window, text="Record 10 seconds Analog TV", command=analogtvd_testrecord)
b7.grid(row=7, column=0)

b8 = Button(window, text="Record 10 seconds Digital TV & IPTV module", command=digital_tvrecd_testrecord)
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
# t2.grid(row=1,column=1,rowspan=10,columnspan=10,sticky=W+E+N+S, padx=5, pady=5)
t2.grid(row=1, column=1, rowspan=20, columnspan=8, sticky=W + E + N + S, padx=5, pady=5)
# Company Logo
logo_path = 'company_logo.jpg'
img = ImageTk.PhotoImage(Image.open("company_logo.jpg"))
imglabel = Label(window, image=img).grid(row=0, column=3, sticky=E + N, rowspan=10)

# C.pack()
window.mainloop()

# TO-DOs:

# Create the option to receive files from the server
