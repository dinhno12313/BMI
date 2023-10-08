from tkinter import *
import sqlite3
import hashlib
import random
import string
from math import *
import time
import datetime
from tkinter import messagebox
from matplotlib import pyplot as plt

BMIDB = sqlite3.connect("bmidatabase.db")
c = BMIDB.cursor()
class Welcome():
    def __init__ (self, master): 
        self.master = master 
        self.master.geometry('260x260+100+200')
        self.master.title('BMI Welcome') 
        self.master.configure(background='white') 
        welcometext = "CHÀO MỪNG BẠN ĐẾN VỚI BMI CALCULATOR"
        self.label1 = Label(self.master, text = welcometext, fg='red', background = 'white').grid(row=1, column=1) 
        today = datetime.datetime.now()
        repr(today) 
        self.label3 = Label(self.master, text = ("Thời gian:",today), fg='black', background = 'white').place(x=0, y=140)
        self.button1 = Button(self.master, text= "BMI Calculator", fg = 'blue', width = 15, command = self.gotobmicalculator).place(x=0, y=20) 
        self.button2 = Button(self.master, text = "Sổ theo dõi", fg = 'blue', width = 15, command = self.gotorecords).place(x=0, y=50)
        self.button3 = Button(self.master, text = "Biểu đồ cân nặng", fg = 'blue', width = 15, command = self.gotochart).place(x=0, y=80)
        self.button4 = Button(self.master, text = "Thoát",fg='blue', width = 15, command=self.exit).place(x=0, y=110)
    def exit(self):
        self.master.destroy()
    def gotobmicalculator(self):
        root2 = Toplevel(self.master)   
        myGUIO = bmicalculator(root2)
    def gotorecords(self):
        root2=Toplevel(self.master)
        mygui=records(root2)
    def gotochart(self):
        myguii=chart(self.master)
class bmicalculator():
    def __init__(self,master):
        c.execute('CREATE TABLE IF NOT EXISTS BMIStorage(timestamp TEXT, bodymassindex REAL, weightclass TEXT, weightkg REAL)')
        self.heightcm=DoubleVar()
        self.weightkg=DoubleVar()
        self.ageyear=IntVar()
        self.master=master
        self.master.geometry('280x200+650+250')
        self.master.title('BMI Calculator')
        self.master.configure(background='white')
        self.hello = Label(self.master,text="BMI CALCULATOR", relief=RAISED)
        self.hello.pack(side=TOP) 
        self.var = IntVar()
        self.frame = Frame(master,padx=10, pady=10, relief=RAISED, borderwidth=1)
        self.frame.pack(fill=BOTH, expand=True)
        self.bmiage = Label(self.frame,text="Nhập tuổi")
        self.bmiage.grid(row=1, column=1)
        self.age = Entry(self.frame,textvariable=self.ageyear)
        self.age.grid(row=1, column=2, pady=5)
        self.gen_lb = Label(self.frame,text='Giới tính')
        self.gen_lb.grid(row=2, column=1)
        self.frame2 = Frame(self.frame)
        self.frame2.grid(row=2, column=2, pady=5)
        self.male_rb = Radiobutton(self.frame2,text = 'Nam',variable = self.var,value = 1)
        self.male_rb.pack(side=LEFT)
        self.female_rb = Radiobutton(self.frame2,text = 'Nữ',variable = self.var,value = 2)
        self.female_rb.pack(side=RIGHT)
        self.bmiheight = Label(self.frame,text="Nhập chiều cao(cm)  ")
        self.bmiheight.grid(row=3, column=1)
        self.bmiweight = Label(self.frame,text="Nhập cân nặng(kg)  ")      
        self.bmiweight.grid(row=4, column=1)
        self.height = Entry(self.frame,textvariable=self.heightcm)
        self.height.grid(row=3, column=2, pady=5)
        self.weight = Entry(self.frame,textvariable=self.weightkg)
        self.weight.grid(row=4, column=2, pady=5)
        self.frame3 = Frame(self.frame)
        self.frame3.grid(row=5, columnspan=3, pady=10)
        self.cal_btn = Button(self.frame3,text='Tính BMI',command=self.bmicalculation)
        self.cal_btn.pack(side=LEFT)
        self.save_btn = Button(self.frame3,text="Lưu chỉ số", command=self.dynamic_data_entry)
        self.save_btn.pack(side=LEFT)     
        self.exit_btn = Button(self.frame3,text='Trở về',command=self.exit)
        self.exit_btn.pack(side=RIGHT)
    def bmicalculation(self):
        bmiheight=self.heightcm.get()
        bmiweight=self.weightkg.get()
        bmiage = self.ageyear.get()
        bmivar = self.var.get()
        self.weightt = bmiweight
        if bmiheight == 0.0 or bmiweight == 0.0 or bmiage == 0 or (bmivar!=1 and bmivar!=2):
            messagebox.showerror('BMI Calculator', f'Vui lòng nhập đầy đủ thông tin!')
            totalindex = ''
            self.totalindex = totalindex
        elif (bmiage < 2) or (bmiage > 120):
            messagebox.showerror('BMI Calculator', f'Tuổi nhập vào không hợp lệ!')
            totalindex = ''
            self.totalindex = totalindex
        else:
            bmi = float((bmiweight)/((bmiheight/100)**2))
            bmi = round(bmi, 2)
            self.bmi = bmi
            if (0 < bmi < 18.5) and (bmiheight > 0):
                messagebox.showinfo('BMI Calculator', f'BMI = {self.bmi}. Bạn đang thiếu cân. Chú ý ăn uống đủ bữa, nghỉ ngơi đúng giờ nha ^^')
                totalindex = 'Thiếu cân'
                self.totalindex = totalindex
            elif (bmi > 18.5) and (bmi < 24.9) and (bmiheight > 0):
                messagebox.showinfo('BMI Calculator', f'BMI = {self.bmi}. Cơ thể bạn đang rất vừa vặn. Hãy tiếp tục giữ phong độ bạn nhé ^^')
                totalindex = 'Khoẻ mạnh'
                self.totalindex = totalindex
            elif (bmi > 24.9) and (bmi < 29.9) and (bmiheight > 0):
                messagebox.showinfo('BMI Calculator', f'BMI = {self.bmi}. Bạn đang hơi thừa cân. Hãy giảm thiểu lượng dầu mỡ, đường và protein để cơ thể trở nên vừa vặn hơn nha ^^')
                totalindex = 'Thừa cân'
                self.totalindex = totalindex
            elif (bmi > 29.9) and (bmiheight > 0):
                messagebox.showinfo('BMI Calculator', f'BMI = {self.bmi}. Bạn đang béo phì!!! Hãy ăn uống một cách khoa học hơn, giảm thiểu lượng dầu mỡ, đường, protein và nghe theo chỉ dẫn của bác sĩ dinh dưỡng!!!') 
                totalindex = 'Béo phì'
                self.totalindex = totalindex
            else:
                messagebox.showerror('BMI Calculator', f'Có vẻ bạn đã nhập sai!!!')
                totalindex = ''
                self.totalindex = totalindex
    def dynamic_data_entry(self):
        timestamp = str(datetime.datetime.now().date())
        bodymassindex = self.bmi
        weightclass = self.totalindex
        weightkg = self.weightt
        if  weightclass == '':
            messagebox.showerror('BMI Calculator', f'Không có thông tin!')
        else:
            c.execute("INSERT INTO BMIStorage (timestamp, bodymassindex, weightclass, weightkg) VALUES (?, ?, ?, ?)",(timestamp, bodymassindex, weightclass, weightkg))
            BMIDB.commit()
            messagebox.showinfo('BMI Calculator', f'Lưu thành công!')
    def exit(self):
        self.master.destroy()
class records():
    def __init__(self,master):
        self.master = master
        self.master.geometry('400x400+650+250')
        self.master.configure(background='white')
        self.master.title('Sổ theo dõi')
        self.connection = sqlite3.connect('bmidatabase.db')
        self.cur = self.connection.cursor()
        self.dateLabel = Label(self.master, text="Ngày", width=10)
        self.dateLabel.grid(row=0, column=0)
        self.BMILabel = Label(self.master, text="BMI", width=10)
        self.BMILabel.grid(row=0, column=1)
        self.stateLabel = Label(self.master, text="Trạng thái", width=10)
        self.stateLabel.grid(row=0, column=2)
        self.showallrecords()
        self.button5=Button(self.master, text="Tình trạng cân nặng", width=15, fg = 'blue', command=self.showweight).grid(row=0,column=6)
        self.button4=Button(self.master,text="Trở về", width=15, fg = 'red',command=self.exit).grid(row=1,column=6)
        self.l2 = list()
        self.connection = sqlite3.connect('bmidatabase.db')
        self.cur = self.connection.cursor()
        for i in self.cur.execute("Select weightkg FROM BMIStorage"):
            self.weightlist = list(i)
            self.realweight = self.weightlist.pop()
            self.l2.append(self.realweight)
    def showweight(self):
        if len(self.l2)>1:
            self.showkg = self.l2[-2] - self.l2[-1]
            if self.showkg == 0:
                messagebox.showinfo('Thông báo cân nặng', f'Lần lưu cân nặng gần nhất của bạn là ' + str(self.l2[-1]) + 'kg!\nSo với lần lưu cân nặng trước đó, cân nặng của bạn không thay đổi!')
            elif self.showkg > 0:
                messagebox.showinfo('Thông báo cân nặng', f'Lần lưu cân nặng gần nhất của bạn là ' + str(self.l2[-1]) + 'kg!\nSo với lần lưu cân nặng trước đó, bạn đã giảm ' + str(self.showkg) + 'kg!')
            else:
                messagebox.showinfo('Thông báo cân nặng', f'Lần lưu cân nặng gần nhất của bạn là ' + str(self.l2[-1]) + 'kg!\nSo với lần lưu cân nặng trước đó, bạn đã tăng ' + str(fabs(self.showkg)) + 'kg!')
    def showallrecords(self):
        data = self.readfromdatabase()
        for index, dat in enumerate(data):
            Label(self.master, text=dat[0], width=10).grid(row=index+1, column=0)
            Label(self.master, text=dat[1], width=10).grid(row=index+1, column=1)
            Label(self.master, text=dat[2], width=10).grid(row=index+1, column=2)
    def readfromdatabase(self):
        self.cur.execute("SELECT timestamp, bodymassindex, weightclass FROM BMIStorage")
        return self.cur.fetchall()
    def exit(self):
        self.master.destroy()
class chart():
    def __init__(self,master):
        self.l1 = list()
        self.l2 = list()
        self.connection = sqlite3.connect('bmidatabase.db')
        self.cur = self.connection.cursor()
        for i, k in enumerate(self.cur.execute("Select weightkg FROM BMIStorage")):
            self.weightlist = list(k)
            self.realweight = self.weightlist.pop()
            self.l2.append(self.realweight)
            self.l1.append(str(i+1))
        plt.plot(self.l1,self.l2,marker='o', markersize=5, linestyle='-', linewidth=2)
        plt.title("Biểu đồ cân nặng")
        plt.ylabel("Cân nặng")
        plt.xlabel("Số lần tính")
        plt.show()

class Register:
    def __init__(self, master):
        self.master = master
        self.master.geometry('300x200+650+250')
        self.master.title('Đăng ký')
        self.master.configure(background='white')

        self.label1 = Label(self.master, text="Tên tài khoản: ")
        self.label1.grid(row=1, column=0, pady=5)
        self.username = Entry(self.master)
        self.username.grid(row=1, column=1, pady=5)

        self.label2 = Label(self.master, text="Mật khẩu: ")
        self.label2.grid(row=2, column=0, pady=5)
        self.password = Entry(self.master, show="*")
        self.password.grid(row=2, column=1, pady=5)
        self.label3 = Label(self.master, text="Email: ")
        self.label3.grid(row=3, column=0, pady=5)
        self.email = Entry(self.master)
        self.email.grid(row=3, column=1, pady=5)

        self.register_button = Button(self.master, text="Đăng ký", command=self.register)
        self.register_button.grid(row=4, columnspan=2, pady=10)

        self.login_link = Label(self.master, text="Đã có tài khoản? Đăng nhập", fg='blue', cursor='hand2')
        self.login_link.grid(row=5, columnspan=2, pady=5)
        self.login_link.bind("<Button-1>", self.go_to_login)

    def register(self):
        username = self.username.get()
        password = self.password.get()
        email = self.email.get()

        if len(username) < 6:
            messagebox.showerror('Đăng ký', 'Tên tài khoản phải có ít nhất 6 ký tự.')
            return

        if len(password) < 8:
            messagebox.showerror('Đăng ký', 'Mật khẩu phải có ít nhất 8 ký tự.')
            return

        # Kiểm tra tính hợp lệ của email
        if not self.is_valid_email(email):
            messagebox.showerror('Đăng ký', 'Email không hợp lệ.')
            return

        # Kiểm tra xem tài khoản đã tồn tại chưa
        if self.is_username_exists(username):
            messagebox.showerror('Đăng ký', 'Tên tài khoản đã tồn tại.')
            return
        
        if self.is_email_exists(email):
            messagebox.showerror('Đăng ký', 'Email đã tồn tại.')
            return

        # Lưu thông tin tài khoản vào CSDL (trong trường hợp thực tế, bạn cần mã hóa mật khẩu trước khi lưu)
        c.execute("INSERT INTO Users (username, password, email) VALUES (?, ?, ?)", (username, hashlib.md5(password.encode()).hexdigest(), email))
        BMIDB.commit()

        messagebox.showinfo('Đăng ký', 'Đăng ký thành công!')
        self.go_to_login()

    def is_valid_email(self, email):
        # Đây chỉ là một kiểm tra đơn giản, bạn có thể sử dụng biểu thức chính quy mạnh hơn để kiểm tra email.
        if "@" in email and "." in email:
            return True
        return False

    def is_username_exists(self, username):
        c.execute("SELECT * FROM Users WHERE username=?", (username,))
        user = c.fetchone()
        if user:
            return True
        return False
    
    def is_email_exists(self, email):
        c.execute("SELECT * FROM Users WHERE email=?", (email,))
        user = c.fetchone()
        if user:
            return True
        return False

    def go_to_login(self, event=None):
        self.master.destroy()
        root = Tk()
        myGUILogin = Login(root)
        root.mainloop()


class Login:
    def __init__(self, master):
        self.master = master
        self.master.geometry('250x210+650+250')
        self.master.title('Đăng nhập')
        self.master.configure(background='white')

        self.label1 = Label(self.master, text="Tên tài khoản: ")
        self.label1.grid(row=0, column=0, pady=5)
        self.username = Entry(self.master)
        self.username.grid(row=0, column=1, pady=5)

        self.label2 = Label(self.master, text="Mật khẩu: ")
        self.label2.grid(row=1, column=0, pady=5,  sticky="w")
        self.password = Entry(self.master, show="*")
        self.password.grid(row=1, column=1, pady=5)

        self.login_button = Button(self.master, text="Đăng nhập", command=self.login)
        self.login_button.grid(row=2, columnspan=2, pady=5)

        self.register_link = Label(self.master, text="Chưa có tài khoản? Đăng ký", fg='blue', cursor='hand2')
        self.register_link.grid(row=5, columnspan=2, pady=5)
        self.register_link.bind("<Button-1>", self.go_to_register)

        self.forgot_password_button = Button(self.master, text="Quên mật khẩu", command=self.go_to_forgot_password)
        self.forgot_password_button.grid(row=4, columnspan=2, pady=5)

        self.change_password_button = Button(self.master, text="Đổi mật khẩu", command=self.go_to_change_password)
        self.change_password_button.grid(row=3, columnspan=2, pady=5)


    def login(self):
        global logged_in_user
        username = self.username.get()
        password = self.password.get()

        # Kiểm tra xem tài khoản và mật khẩu có tồn tại trong CSDL hay không
        c.execute("SELECT * FROM Users WHERE username=? AND password=?", (username, hashlib.md5(password.encode()).hexdigest()))
        user = c.fetchone()
        if user:
            logged_in_user = username
            self.master.destroy()
            root = Tk()
            myGUIWelcome = Welcome(root)
            root.mainloop()
        else:
            messagebox.showerror('Đăng nhập', 'Tên tài khoản hoặc mật khẩu không đúng.')

    def go_to_register(self, event=None):
        self.master.destroy()
        root = Tk()
        myGUIRegister = Register(root)
        root.mainloop()

    def go_to_forgot_password(self):
        self.master.destroy()
        root = Tk()
        myGUIForgotPassword = ForgotPassword(root)
        root.mainloop()

    def go_to_change_password(self):
        self.master.destroy()
        root = Tk()
        myGUIForgotPassword = ChangePassword(root)
        root.mainloop()



class ForgotPassword:
    def __init__(self, master):
        self.master = master
        self.master.geometry('300x150+650+250')
        self.master.title('Quên mật khẩu')
        self.master.configure(background='white')

        self.label1 = Label(self.master, text="Tên tài khoản: ")
        self.label1.grid(row=0, column=0, pady=5)
        self.username = Entry(self.master)
        self.username.grid(row=0, column=1, pady=5)

        self.label2 = Label(self.master, text="Email: ")
        self.label2.grid(row=1, column=0, pady=5)
        self.email = Entry(self.master)
        self.email.grid(row=1, column=1, pady=5)

        self.reset_password_button = Button(self.master, text="Đặt lại mật khẩu", command=self.reset_password)
        self.reset_password_button.grid(row=2, columnspan=2, pady=10)

        self.login_link = Label(self.master, text="Đã nhớ mật khẩu? Đăng nhập", fg='blue', cursor='hand2')
        self.login_link.grid(row=3, columnspan=2, pady=5)
        self.login_link.bind("<Button-1>", self.go_to_login)

    def reset_password(self):
        username = self.username.get()
        email = self.email.get()

        # Kiểm tra xem tài khoản có tồn tại trong CSDL hay không
        c.execute("SELECT * FROM Users WHERE username=? AND email=?", (username, email))
        user = c.fetchone()
        if user:
            # Trong thực tế, bạn có thể thực hiện các bước khác để đặt lại mật khẩu, như gửi email xác minh và cung cấp một liên kết đặt lại mật khẩu.
            # Ở đây, chúng ta chỉ đặt lại mật khẩu thành một mật khẩu mặc định (ví dụ: "password123")
            new_password = "password123"
            c.execute("UPDATE Users SET password=? WHERE username=?", (hashlib.md5(new_password.encode()).hexdigest(), username))
            BMIDB.commit()
            messagebox.showinfo('Quên mật khẩu', 'Mật khẩu đã được đặt lại thành công. Mật khẩu mới là "password123". Vui lòng đăng nhập và đổi mật khẩu sau khi đăng nhập.')
        else:
            messagebox.showerror('Quên mật khẩu', 'Tên tài khoản hoặc email không đúng.')

    def go_to_login(self, event=None):
        self.master.destroy()
        root = Tk()
        myGUILogin = Login(root)
        root.mainloop()

class ChangePassword:
    def __init__(self, master):
        self.master = master
        self.master.geometry('300x220+650+250')
        self.master.title('Đổi mật khẩu')
        self.master.configure(background='white')

        self.label1 = Label(self.master, text="Tên tài khoản: ")
        self.label1.grid(row=0, column=0, pady=5)
        self.username = Entry(self.master)
        self.username.grid(row=0, column=1, pady=5)

        self.label2 = Label(self.master, text="Email: ")
        self.label2.grid(row=1, column=0, pady=5)
        self.email = Entry(self.master)
        self.email.grid(row=1, column=1, pady=5)

        self.label3 = Label(self.master, text="Mật khẩu cũ: ")
        self.label3.grid(row=2, column=0, pady=5)
        self.password_old = Entry(self.master, show="*")
        self.password_old.grid(row=2, column=1, pady=5)
        
        self.label4 = Label(self.master, text="Mật khẩu mới: ")
        self.label4.grid(row=3, column=0, pady=5)
        self.password_new = Entry(self.master, show="*")
        self.password_new.grid(row=3, column=1, pady=5)

        self.reset_password_button = Button(self.master, text="Đổi mật khẩu", command=self.change_password)
        self.reset_password_button.grid(row=4, columnspan=2, pady=10)

        self.login_link = Label(self.master, text="Đăng nhập", fg='blue', cursor='hand2')
        self.login_link.grid(row=5, columnspan=2, pady=5)
        self.login_link.bind("<Button-1>", self.go_to_login)

    def change_password(self):
        username = self.username.get()
        email = self.email.get()
        password_old = self.password_old.get()
        password_new = self.password_new.get()
        
        # Kiểm tra xem tài khoản có tồn tại trong CSDL hay không
        c.execute("SELECT * FROM Users WHERE username=? AND password=? AND email=?", (username, hashlib.md5(password_old.encode()).hexdigest(), email))
        user = c.fetchone()
        if user:
            new_password = password_new
            c.execute("UPDATE Users SET password=? WHERE username=?", (hashlib.md5(new_password.encode()).hexdigest(), username))
            BMIDB.commit()
            messagebox.showinfo('Quên mật khẩu', 'Mật khẩu đã được đổi thành công.')
        else:
            messagebox.showerror('Quên mật khẩu', 'Thông tin tài khoản không đúng.')

    def go_to_login(self, event=None):
        self.master.destroy()
        root = Tk()
        myGUILogin = Login(root)
        root.mainloop()



def main():
    BMIDB = sqlite3.connect("bmidatabase.db")
    c = BMIDB.cursor()

    # Tạo bảng Users nếu nó chưa tồn tại
    c.execute('''
        CREATE TABLE IF NOT EXISTS Users (
            id INTEGER PRIMARY KEY,
            username TEXT,
            password TEXT,
            email TEXT
        )
    ''')
    root = Tk()
    myGUILogin = Login(root)  # Hiển thị giao diện đăng nhập
    root.mainloop()

if __name__ == '__main__':
    main()
