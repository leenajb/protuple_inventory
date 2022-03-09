from logging import root
from pydoc import plain
from time import time
from tkinter import*
from turtle import title
from PIL import Image,ImageTk
from tkinter import messagebox
import sqlite3
import os
import email_pass
import smtplib
import time
root_dir=os.path.dirname(__file__)


class Login:
    def __init__(self,root):
        self.root=root
        self.root.title("Login System")
        self.root.geometry("1350x700+0+0")
        self.root.config(bg="lightblue")

        self.otp=''

        #==========Images====================
        self.log_img=Image.open(os.path.join(root_dir,"F:\\Project Pic\\log1.jpg"))
        self.log_img=self.log_img.resize((390,380),Image.ANTIALIAS)
        self.log_img=ImageTk.PhotoImage(self.log_img)
        lbl_img=Label(self.root,image=self.log_img,bd=2)
        lbl_img.place(x=200,y=110)

        #================login frame=================
        self.employee_id=StringVar()
        self.password=StringVar()
        login_frame=Frame(self.root,bd=2,relief=RIDGE,bg="white")
        login_frame.place(x=650,y=90,width=350,height=460)

        title=Label(login_frame,text="Login System",font=("Elephant",30,"bold"),bg="white").place(x=0,y=30,relwidth=1)
        lbl_user=Label(login_frame,text="Eployee ID",font=("Andalus",15),bg="white",fg="#767171").place(x=50,y=100)
        
        txt_employee_id=Entry(login_frame,textvariable=self.employee_id,font=("times new roman",15),bg="lightgrey").place(x=50,y=140,width=250)

        lbl_pass=Label(login_frame,text="Paswword",font=("Andalus",15),bg="white",fg="#767171").place(x=50,y=200)
        txt_pass=Entry(login_frame,textvariable=self.password,show="*",font=("times new roman",15),bg="lightgrey").place(x=50,y=240,width=250)
        
        btnlogin=Button(login_frame,command=self.login,text="Log In",font=("Arial Rounded MT Bold",15),bg="#00B0F0",cursor="hand2").place(x=50,y=300,width=250,height=35)
        hr=Label(login_frame,bg="lightgray").place(x=50,y=380,width=250,height=2)
        or_=Label(login_frame,text="OR",bg="white",fg="lightgrey",font=("times new roman",15,"bold")).place(x=150,y=355)
        btn_forget=Button(login_frame,text="Forget Password?",command=self.forget_window,font=("times new roman",13),bg="white",fg="#00759e",bd=0,activebackground="white",activeforeground="#00759e").place(x=100,y=390)

        #=================frame2=============================
        register_frame=Frame(self.root,bd=2,relief=RIDGE,bg="white")
        register_frame.place(x=650,y=570,width=350,height=60)
        lbl_reg=Label(register_frame,text="Subscribe | Like | Share",font=("times new roman",13),bg="white").place(x=0,y=20,relwidth=1)

        
        #==============All Function==========================

    def login(self):
        con=sqlite3.connect(database=r'protuple_inventory.db')
        cur=con.cursor()
        try:
            if self.employee_id.get()=="" or self.password.get()=="":
                messagebox.showerror("Error","All fields are required",parent=self.root)
            else:
                cur.execute("select utype from employee where eid=? AND pass=?",(self.employee_id.get(),self.password.get()))
                user=cur.fetchone()
                if user==None:
                    messagebox.showerror("Error","Invalid Username/Password",parent=self.root)
                else:
                    if user[0]=="Admin":
                        self.root.destroy()
                        os.system("python dashboard.py")
                    else:
                        self.root.destroy()
                        os.system("python billing.py")
        except Exception as ex:
            messagebox.showerror("Error",f"Error due to :{str(ex)}",parent=self.root)

    def forget_window(self):
        con=sqlite3.connect(database=r'protuple_inventory.db')
        cur=con.cursor()
        try:
            if self.employee_id.get()=="":
                messagebox.showerror("Error","Employee ID required",parent=self.root)
            else:
                cur.execute("select email from employee where eid=?",(self.employee_id.get(),))
                email=cur.fetchone()
                if email==None:
                    messagebox.showerror("Error","Invalid Employee ID try again",parent=self.root)
                else:
                    #=======forget window==========
                    self.var_otp=StringVar()
                    self.var_newpass=StringVar()
                    self.var_con_pass=StringVar()
                    #====call send email function====
                    chk=self.send_email(email[0])
                    if chk=='f':
                        messagebox.showerror("Error","Connection Error,try again",parent=self.root)
                    else:
                        self.forget_win=Toplevel(self.root)
                        self.forget_win.title('RESET Passwprd')
                        self.forget_win.geometry('400x350+500+100')
                        self.forget_win.focus_force()

                        title=Label(self.forget_win,text="Reset Password",font=("goudy old style",15,"bold"),bg="#3f51b5",fg="white").pack(side=TOP,fill=X)
                        lbl_reset=Label(self.forget_win,text="Enter OTP sent on Registered Email",font=("times new roman",15)).place(x=20,y=60)
                        txt_reset=Entry(self.forget_win,textvariable=self.var_otp,font=("times new roman",15),bg="lightyellow").place(x=20,y=100,width=250,height=30)

                        self.btn_reset=Button(self.forget_win,text="Submit",command=self.validate_otp,font=("times new roman",15),bg="lightblue")
                        self.btn_reset.place(x=280,y=100,width=100,height=30)

                        lbl_newpass=Label(self.forget_win,text="New Password",font=("times new roman",15)).place(x=20,y=160)
                        txt_newpass=Entry(self.forget_win,textvariable=self.var_newpass,font=("times new roman",15),bg="lightyellow").place(x=20,y=190,width=250,height=30)

                        lbl_c_pass=Label(self.forget_win,text="Confirm Password",font=("times new roman",15)).place(x=20,y=225)
                        txt_c_pass=Entry(self.forget_win,textvariable=self.var_con_pass,font=("times new roman",15),bg="lightyellow").place(x=20,y=255,width=250,height=30)

                        self.btn_update=Button(self.forget_win,text="Update",command=self.update_password,state=DISABLED,font=("times new roman",15),bg="lightblue")
                        self.btn_update.place(x=150,y=300,width=100,height=30)

        except Exception as ex:
            messagebox.showerror("Error",f"Error due to :{str(ex)}",parent=self.root)

    def update_password(self):
        if self.var_newpass.get()=="" or self.var_con_pass.get()=="":
            messagebox.showerror("Error","Password is required",parent=self.forget_win)
        elif self.var_newpass.get()!= self.var_con_pass.get():
             messagebox.showerror("Error","New Password  & comfirm password must be same",parent=self.forget_win)

        else:
             con=sqlite3.connect(database=r'protuple_inventory.db')
             cur=con.cursor()
             try:
                 cur.execute("Update employee SET pass=? where eid=?",(self.var_newpass.get(),self.employee_id.get()))
                 con.commit()
                 messagebox.showinfo("Success","Password updated successfully",parent=self.forget_win)
                 self.forget_win.destroy()
             except Exception as ex:
                messagebox.showerror("Error",f"Error due to :{str(ex)}",parent=self.root)

    def validate_otp(self):
        if int(self.otp)==int(self.var_otp.get()):
            self.btn_update.config(state=NORMAL)
            self.btn_reset.config(state=DISABLED)
        else:
            messagebox.showerror("Error","Invalid OTP, Try again",parent=self.forget_win)

    def send_email(Self,to_):
        s=smtplib.SMTP('smtp.gmail.com',587)
        s.starttls()
        email_=email_pass.email_
        pass_=email_pass.pass_

        s.login(email_,pass_)

        Self.otp=int(time.strftime("%H%S%M"))+int(time.strftime("%S"))
        subj='IMS Reset Password OTP'
        msg=f'Dear Sir/Madam,\n\nYour Reset OTP is {str(Self.otp)}.\n\nWith Regards, \nIMS Team'
        msg="Subject:{}\n\n{}".format(subj,msg)
        s.sendmail(email_,to_,msg)
        chk=s.ehlo()
        if chk[0]==250:
            return 's'
        else:
            return 'f'

        
root=Tk()
obj=Login(root)
root.mainloop()
