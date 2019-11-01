#!/usr/bin/env python
import collections
from tkinter import *
from tkinter import ttk as tk
import psutil
import os
import signal
import sys




class start_window(Frame):
    def __init__(self, parent=None):


        Frame.__init__(self, parent, background="white")
        Frame.pack(self, expand=True, fill=BOTH)


        #Label
        Label(self, text = 'Choose From Menu', background="white", width=30).pack()

        #Buttons
        self.list_process = Button(self, text='list processes', command=self.init_list_process)
        self.list_process.pack(side=TOP, fill=X, expand=YES)

        self.cpu_time = Button(self, text='cpu info', command=self.init_total_cpu_time)
        self.cpu_time.pack(side=TOP,fill=X, expand=YES)

        self.mem_usage = Button(self, text='memory used', command=self.init_mem_usage)
        self.mem_usage.pack(side=TOP, fill=X,expand=YES)
        self.disk_usage = Button(self, text='disk used', command=self.init_disk_usage)
        self.disk_usage.pack(side=TOP,fill=X, expand=YES)
        self.network_info = Button(self, text='network information',command=self.init_network_info)
        self.network_info.pack(side=TOP,fill=X,expand=YES)

    def init_list_process(self):
        self.after(1,self.list_all_process)

    def init_total_cpu_time(self):
        self.after(1,self.total_cpu_time)

    def init_mem_usage(self):
        self.after(1, self.memory_usage)

    def init_disk_usage(self):
        self.after(1, self.disk_d_usage)

    def init_network_info(self):
        self.after(1, self.network_d_info)

    def list_all_process(self):
        # SrollBar
        self.list = Tk()
        # process
        self.scrollbar = Scrollbar(self.list)
        # tree
        self.tree = tk.Treeview(self.list, height=40, yscrollcommand=self.scrollbar.set)
        self.scrollbar.pack(side=RIGHT, fill=Y)
        self.scrollbar.config(command=self.tree.yview)

        self.tree["columns"]=("one","two")
        self.tree.column("0", width=0)
        self.tree.column("one", width=150, minwidth=150,anchor=E)
        self.tree.column("two", width=80, minwidth=50,anchor=E)

        self.tree.heading("one", text="name")
        self.tree.heading("two", text="ID")
        i=1
        for proc in psutil.process_iter():
            try:
                # Get process name & pid from process object.
                processName = proc.name()
                processID = proc.pid
                self.tree.insert('', 'end', text="process "+str(i),
                         values=(processName,
                                 processID))


                i+=1

            except (psutil.NoSuchProcess, psutil.AccessDenied, psutil.ZombieProcess):
                pass

        self.list.title("process list")
        self.list.wm_iconbitmap('sys.ico')
        self.list.geometry("500x400")
        self.tree.pack(fill='x')
        self.popup_menu = Menu(self.list, tearoff=0)

        self.popup_menu.add_command(label="stop process",
                                    command=self.delete_selected)

        self.tree.bind('<Button-3>', self.popup)
        # self.tree.bind('<Button-3>', self.delete_selected)

    def delete_selected(self):

        try:
            curItem = self.tree.item(self.tree.focus())
            item = self.tree.selection()[0]
            self.kill_process(curItem['values'])
            self.tree.delete(item)

        except:
             pass

    def popup(self, event):
        """action in event of button 3 on tree view"""

        try:
            self.popup_menu.tk_popup(event.x_root, event.y_root, 0)

        finally:
            self.popup_menu.grab_release()

    def kill_process(self, value):


        done=FALSE;
        for proc in psutil.process_iter():
            try:

                if(proc.name()==value[0]):
                    proc.terminate()
            except:
                pass


    def total_cpu_time(self):
        # SrollBar
        self.list = Tk()
        # process
        self.scrollbar = Scrollbar(self.list)
        # tree
        self.tree = tk.Treeview(self.list, height=40, yscrollcommand=self.scrollbar.set)
        self.scrollbar.pack(side=RIGHT, fill=Y)
        self.scrollbar.config(command=self.tree.yview)

        self.tree["columns"] = ("one", "two","three", "four","five","six")
        self.tree.column("0", width=0)
        self.tree.column("one", width=150, minwidth=150,anchor=E)
        self.tree.column("two", width=80, minwidth=50,anchor=E)
        self.tree.column("three", width=80, minwidth=50,anchor=E)
        self.tree.column("four", width=80, minwidth=50,anchor=E)
        self.tree.column("five", width=80, minwidth=50, anchor=E)
        self.tree.column("six", width=80, minwidth=50, anchor=E)

        self.tree.heading("one", text="user time/min")
        self.tree.heading("two", text="system time/min")
        self.tree.heading("three", text="idle time/min")
        self.tree.heading("four", text="interrupts")
        self.tree.heading("five", text="total usage/%")
        self.tree.heading("six", text="total processors")

        time=psutil.cpu_times()
        usage=psutil.cpu_percent();
        count=psutil.cpu_count(1);

        #user time system time idle time interrupts
        self.tree.insert('', 'end', text="processor info",
                         values=("{:.2f}".format(time.user*0.0166667), "{:.2f}".format(time.system*0.0166667),"{:.2f}".format(time.idle*0.0166667), "{:.2f}".format(time.interrupt), usage,count))

        self.list.title("cpu info")
        self.list.wm_iconbitmap('sys.ico')
        self.list.geometry("510x400")
        self.tree.pack(fill='x')

    # def total_cpu_usage(self):
    #     print("Total Cpu Usage %: ", psutil.cpu_percent())


    # def total_cpu_count(self):
    #     print("Total Logical Processors: ", psutil.cpu_count(1))


    def memory_usage(self):

        self.list = Tk()
        # process
        self.scrollbar = Scrollbar(self.list)
        # tree
        self.tree = tk.Treeview(self.list, height=40, yscrollcommand=self.scrollbar.set)
        self.scrollbar.pack(side=RIGHT, fill=Y)
        self.scrollbar.config(command=self.tree.yview)

        self.tree["columns"] = ("one", "two", "three", "four")
        self.tree.column("0", width=0)
        self.tree.column("one", width=150, minwidth=150, anchor=E)
        self.tree.column("two", width=80, minwidth=50, anchor=E)
        self.tree.column("three", width=80, minwidth=50, anchor=E)
        self.tree.column("four", width=80, minwidth=50, anchor=E)

        self.tree.heading("one", text="total/bytes")
        self.tree.heading("two", text="used/bytes")
        self.tree.heading("three", text="available/bytes")
        self.tree.heading("four", text="free/bytes")

        mem = psutil.virtual_memory()

        # user time system time idle time interrupts
        self.tree.insert('', 'end', text="memory usage",
                         values=("{:.2f}".format(mem.total), "{:.2f}".format(mem.used),
                                 "{:.2f}".format(mem.available), "{:.2f}".format(mem.free)))

        self.list.title("memory usage")
        self.list.wm_iconbitmap('sys.ico')
        self.list.geometry("510x400")
        self.tree.pack(fill='x')


    def disk_d_usage(self):
        disk = psutil.disk_partitions()
        # for info in disk:
        #     print("Drive :", info.device)
        #     print("Mount Point: ", info.mountpoint)
        #     print("File SYstem: ", info.fstype)
        #     print("Read/Write: ", info.opts)
        self.list = Tk()
        # process
        self.scrollbar = Scrollbar(self.list)
        # tree
        self.tree = tk.Treeview(self.list, height=40, yscrollcommand=self.scrollbar.set)
        self.scrollbar.pack(side=RIGHT, fill=Y)
        self.scrollbar.config(command=self.tree.yview)

        self.tree["columns"] = ("one", "two", "three", "four")
        self.tree.column("0", width=0)
        self.tree.column("one", width=150, minwidth=150, anchor=E)
        self.tree.column("two", width=80, minwidth=50, anchor=E)
        self.tree.column("three", width=80, minwidth=50, anchor=E)
        self.tree.column("four", width=80, minwidth=50, anchor=E)

        self.tree.heading("one", text="drive")
        self.tree.heading("two", text="mount point")
        self.tree.heading("three", text="file system")
        self.tree.heading("four", text="read/write")



        # user time system time idle time interrupts
        for info in disk:
            self.tree.insert('', 'end', text="disk info",
                         values=(info.device, info.mountpoint,
                                 info.fstype, info.opts))

        self.list.title("disk usage")
        self.list.wm_iconbitmap('sys.ico')
        self.list.geometry("510x400")
        self.tree.pack(fill='x')

    def network_d_info(self):

       network_pack=psutil.net_io_counters(pernic=True) #dic
       network_conn=psutil.net_connections(kind='all') #list
       network_nic=psutil.net_if_addrs() #dict
       network_nic_meta= psutil.net_if_stats() #dict





       self.list = Tk()
       # process
       self.hscrollbar1 = Scrollbar(self.list, orient=HORIZONTAL)
       self.vscrollbar1 = Scrollbar(self.list, orient=VERTICAL)
       # tree
       self.tree1 = tk.Treeview(self.list,  height=40, yscrollcommand = self.vscrollbar1.set,
                                  xscrollcommand = self.hscrollbar1.set)

       self.hscrollbar1.config(command=self.tree1.xview)
       self.vscrollbar1.config(command=self.tree1.yview)
       self.hscrollbar1.pack(side=BOTTOM, fill=X, expand=FALSE)
       self.vscrollbar1.pack(side=RIGHT, fill=Y, expand=FALSE)


       # general

       self.tree1["columns"] = ("one")

       columns1 = ['NIC/IP addr','netmask addr','broadcast addr']
       self.tree1.column("0", width=0)
       self.tree1.column("one", width=150, minwidth=150, anchor=E)

       self.tree1.heading("one", text="network type")


       idRoot=[]
       value=[]
       fieldList=[]
       key=[]



       #add network names
       once=0
       for k,v in network_nic_meta.items():

               key.append(k)
               if(once==0):
                   fieldList.append(v._fields)
                   once+=1


               value.append(v)

       i=1
       for network_name in key:
           node =self.tree1.insert('', 'end', text="network "+str(i), values=(network_name,network_name))
           idRoot.append(node)
           i+=1


       # #

       first = 0
       second = 4
       k=0
       # for k in range(len(idRoot)):
       for subitem in value:
               val_ = subitem[first:second]

               for index in range(len(val_)):
                  self.tree1.insert(idRoot[k],index,text=fieldList[0][index], values=(val_[index]))
               k+=1

       q = collections.deque()
       masterList=[]
       value=[]

       #NIC
       for k, v in network_nic.items():
           i=1
           for index in range(len(v)):
                value.append(v[index].address)
                value.append(v[index].netmask)
                value.append(v[index].broadcast)

                if(i==len(v)):
                    copyValue=value.copy()
                    q.append(copyValue)
                    masterList.append(copyValue)
                    value.clear()
                i+=1
       j=0

       for index in range(len(idRoot)):
          count = 1
          for data in masterList[index]:

                   self.tree1.insert(idRoot[index], "end", text=columns1[j]+" "+str(count), values=(data, data, data))
                   j+=1
                   if(j==3):
                     j=0
                     count += 1

       columns1=["local address", "local port", "remote address", "remote port", "status", "process ID"]

       readConn=[]
       for data in network_conn:

             if(len(data.laddr)>0):
                 readConn.append(data.laddr[0])
                 readConn.append(data.laddr[1])

             if (len(data.laddr) == 0):
                 readConn.append("N/A")
                 readConn.append("N/A")
             if (len(data.raddr) == 0):
                readConn.append("N/A")
                readConn.append("N/A")

             if (len(data.raddr) > 0):
                 readConn.append(data.raddr[0])
                 readConn.append(data.raddr[1])


             if(len(data.status)>0):
                 readConn.append(data.status)



             if(data.pid):
                 readConn.append(data.pid)



       node = self.tree1.insert('', 'end', text="connections")

       j=0
       i=1
       for data in readConn:
            self.tree1.insert(node, "end", text=columns1[j]+" "+str(i), values=(data,data,data,data,data,data))
            j+=1


            if(j==6):
                j=0
                i+=1
       self.list.title("network usage")
       self.list.wm_iconbitmap('sys.ico')
       self.list.geometry("510x400")
       self.tree1.pack(fill='x')




def main():

        # list_all_process()
        # total_cpu_count()
        # total_cpu_usage()
        # total_cpu_time()
        # mem_usage()
        # disk_usage()
        # kill_process()

        #network_info()
        root = Tk()
        root.title("Python System Info")
        root.geometry("500x400")

        root.wm_iconbitmap('sys.ico')
        app = start_window(root)
        root.mainloop()


if __name__ == "__main__":
    main()