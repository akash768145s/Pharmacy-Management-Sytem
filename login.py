from tkinter import *
from tkinter import messagebox
import sqlite3
import importlib

# Windows Size and Placement
AccountSystem = Tk()
AccountSystem.rowconfigure(0, weight=1)
AccountSystem.columnconfigure(0, weight=1)
height = 600
width = 500
AccountSystem.geometry(f"{width}x{height}")
AccountSystem.state('zoomed')
AccountSystem.title('LOGIN PAGE')

# Navigating through windows
sign_in = Frame(AccountSystem)
sign_up = Frame(AccountSystem)
for frame in (sign_in, sign_up):
    frame.grid(row=0, column=0, sticky='nsew')

def show_frame(frame):
    frame.tkraise()
show_frame(sign_up)


FirstName=StringVar()
LastName=StringVar()
Email =StringVar()
Password=StringVar()
ConfirmPassword = StringVar()

"""========================================================SIGNUP Page================================================================================================================="""

sign_up.configure(bg="#525561")
backgroundImage = PhotoImage(file=r"/Users/tsrk04/Desktop/-_-/SSN/2ND SEM/software dev lab/Final_SDP/__pycache__/New folder/assets/image_1.png")
bg_image = Label(
    sign_up,
    image=backgroundImage,
    bg="#525561"
)
bg_image.place(x=120, y=28)

sign_up.configure(bg="#525561")

# ================Background Image ====================
backgroundImage = PhotoImage(file=r"/Users/tsrk04/Desktop/-_-/SSN/2ND SEM/software dev lab/Final_SDP/__pycache__/New folder/assets/image_1.png")
bg_image = Label(
    sign_up,
    image=backgroundImage,
    bg="#525561"
)
bg_image.place(x=120, y=28)


# ================ CREATE ACCOUNT HEADER ====================
createAccount_header = Label(
    bg_image,
    text="Create new account",
    fg="#FFFFFF",
    font=("yu gothic ui Bold", 28 * -1),
    bg="#272A37"
)
createAccount_header.place(x=75, y=121)

# ================ ALREADY HAVE AN ACCOUNT TEXT ====================
text = Label(
    bg_image,
    text="Already a member?",
    fg="#FFFFFF",
    font=("yu gothic ui Regular", 15 * -1),
    bg="#272A37"
)
text.place(x=75, y=187)

# ================ GO TO LOGIN ====================
switchLogin = Button(
    bg_image,
    text="Login",
    fg="#206DB4",
    font=("yu gothic ui Bold", 15 * -1),
    bg="#272A37",
    bd=0,
    cursor="hand2",
    activebackground="#272A37",
    activeforeground="#ffffff",
    command=lambda: show_frame(sign_in)
)
switchLogin.place(x=242, y=187)

# ================ LABELS AND ENTRY BOXES ====================
# --------------- First Name ---------------
firstName = Label(
    bg_image,
    text="First Name",
    fg="#ffffff",
    font=("yu gothic ui Light", 15 * -1),
    bg="#272A37"
)
firstName.place(x=75, y=229)

firstNameEntry = Entry(
    bg_image,
    bd=0,
    bg="#206DB4",
    highlightbackground="#ffffff",
    highlightcolor="#ffffff",
    highlightthickness=0,
    foreground="#ffffff",
    font=("yu gothic ui Light", 15 * -1),
    textvariable=FirstName
)
firstNameEntry.place(x=75, y=254)

# --------------- Last Name ---------------
lastName = Label(
    bg_image,
    text="Last Name",
    fg="#ffffff",
    font=("yu gothic ui Light", 15 * -1),
    bg="#272A37"
)
lastName.place(x=390, y=229)

lastNameEntry = Entry(
    bg_image,
    bd=0,
    bg="#206DB4",
    highlightbackground="#ffffff",
    highlightcolor="#ffffff",
    highlightthickness=0,
    foreground="#ffffff",
    font=("yu gothic ui Light", 15 * -1),
    textvariable=LastName
)
lastNameEntry.place(x=390, y=254)

# --------------- Email ---------------
email = Label(
    bg_image,
    text="Email",
    fg="#ffffff",
    font=("yu gothic ui Light", 15 * -1),
    bg="#272A37"
)
email.place(x=75, y=289)

emailEntry = Entry(
    bg_image,
    bd=0,
    bg="#206DB4",
    highlightbackground="#ffffff",
    highlightcolor="#ffffff",
    highlightthickness=0,
    foreground="#ffffff",
    font=("yu gothic ui Light", 15 * -1),
    textvariable=Email
)
emailEntry.place(x=75, y=314)

# --------------- Password ---------------
password = Label(
    bg_image,
    text="Password",
    fg="#ffffff",
    font=("yu gothic ui Light", 15 * -1),
    bg="#272A37"
)
password.place(x=390, y=289)

passwordEntry = Entry(
    bg_image,
    bd=0,
    bg="#206DB4",
    highlightbackground="#ffffff",
    highlightcolor="#ffffff",
    highlightthickness=0,
    foreground="#ffffff",
    font=("yu gothic ui Light", 15 * -1),
    show="*",
    textvariable=Password
)
passwordEntry.place(x=390, y=314)

# --------------- Confirm Password ---------------
confirmPassword = Label(
    bg_image,
    text="Confirm Password",
    fg="#ffffff",
    font=("yu gothic ui Light", 15 * -1),
    bg="#272A37"
)
confirmPassword.place(x=75, y=349)

confirmPasswordEntry = Entry(
    bg_image,
    bd=0,
    bg="#206DB4",
    highlightbackground="#ffffff",
    highlightcolor="#ffffff",
    highlightthickness=0,
    foreground="#ffffff",
    font=("yu gothic ui Light", 15 * -1),
    show="*",
    textvariable=ConfirmPassword
)
confirmPasswordEntry.place(x=75, y=374)

# ================ SIGNUP BUTTON ====================
def signup():
    try:
        if FirstName.get() == "" or LastName.get() == "" or Email.get() == "" or Password.get() == "" or ConfirmPassword.get() == "":
            messagebox.showerror("Error", "All fields are required!")
        elif Password.get() != ConfirmPassword.get():
            messagebox.showerror("Error", "Passwords do not match!")
        else:
            conn = sqlite3.connect("user_database.db")
            cursor = conn.cursor()
            cursor.execute(
                "CREATE TABLE IF NOT EXISTS users (first_name TEXT, last_name TEXT, email TEXT, password TEXT)")
            cursor.execute("SELECT * FROM users WHERE email=?", (Email.get(),))
            if cursor.fetchall():
                messagebox.showerror("Error", "User with this email already exists!")
            else:
                cursor.execute("INSERT INTO users VALUES (?, ?, ?, ?)",
                               (FirstName.get(), LastName.get(), Email.get(), Password.get()))
                conn.commit()
                conn.close()
                messagebox.showinfo("Success", "Account created successfully!")
                FirstName.set("")
                LastName.set("")
                Email.set("")
                Password.set("")
                ConfirmPassword.set("")
    except Exception as e:
        print(str(e))
signup_button = Button(
    bg_image,
    text="Create Account",
    fg="#ffffff",
    bg="#206DB4",
    font=("yu gothic ui Bold", 18 * -1),
    relief=FLAT,
    cursor="hand2",
    command=signup
)
signup_button.place(x=75, y=424)


"""========================================================LOGIN PAGE================================================================================================================="""

sign_in.configure(bg="#525561")

# ================Background Image ====================
backgroundImage = PhotoImage(file=r"/Users/tsrk04/Desktop/-_-/SSN/2ND SEM/software dev lab/Final_SDP/__pycache__/New folder/assets/image_1.png")
bg_image2 = Label(
    sign_in,
    image=backgroundImage,
    bg="#525561"
)
bg_image2.place(x=120, y=28)

# ================ LOGIN HEADER ====================
login_header = Label(
    bg_image2,
    text="Login",
    fg="#FFFFFF",
    font=("yu gothic ui Bold", 28 * -1),
    bg="#272A37"
)
login_header.place(x=75, y=121)

# ================ DON'T HAVE AN ACCOUNT TEXT ====================
text = Label(
    bg_image2,
    text="Don't have an account?",
    fg="#FFFFFF",
    font=("yu gothic ui Regular", 15 * -1),
    bg="#272A37"
)
text.place(x=75, y=187)

# ================ GO TO SIGNUP ====================
switchSignup = Button(
    bg_image2,
    text="Create an account",
    fg="#206DB4",
    font=("yu gothic ui Bold", 15 * -1),
    bg="#272A37",
    bd=0,
    cursor="hand2",
    activebackground="#272A37",
    activeforeground="#ffffff",
    command=lambda: show_frame(sign_up)
)
switchSignup.place(x=242, y=187)

# ================ LABELS AND ENTRY BOXES ====================
# --------------- Email ---------------
email = Label(
    bg_image2,
    text="Email",
    fg="#ffffff",
    font=("yu gothic ui Light", 15 * -1),
    bg="#272A37"
)
email.place(x=75, y=229)

emailEntry = Entry(
    bg_image2,
    bd=0,
    bg="#206DB4",
    highlightbackground="#ffffff",
    highlightcolor="#ffffff",
    highlightthickness=0,
    foreground="#ffffff",
    font=("yu gothic ui Light", 15 * -1)
)
emailEntry.place(x=75, y=254)

# --------------- Password ---------------
password = Label(
    bg_image2,
    text="Password",
    fg="#ffffff",
    font=("yu gothic ui Light", 15 * -1),
    bg="#272A37"
)
password.place(x=75, y=289)

passwordEntry = Entry(
    bg_image2,
    bd=0,
    bg="#206DB4",
    highlightbackground="#ffffff",
    highlightcolor="#ffffff",
    highlightthickness=0,
    foreground="#ffffff",
    font=("yu gothic ui Light", 15 * -1),
    show="*"
)
passwordEntry.place(x=75, y=314)


# ================ LOGIN BUTTON ====================
def login():
    try:
        conn = sqlite3.connect("user_database.db")
        cursor = conn.cursor()
        cursor.execute("SELECT * FROM users WHERE email=? AND password=?", (emailEntry.get(), passwordEntry.get()))
        if cursor.fetchall():
            AccountSystem.destroy()
            home_module = importlib.import_module('Home')
        else:
            messagebox.showerror("Error", "Invalid Email or Password!")
        conn.close()
        emailEntry.delete(0, END)
        passwordEntry.delete(0, END)
    except Exception as e:
        print(str(e))

        
login_button = Button(
    bg_image2,
    text="Login",
    fg="#ffffff",
    bg="#206DB4",
    font=("yu gothic ui Bold", 18 * -1),
    relief=FLAT,
    cursor="hand2",
    command=login
)
login_button.place(x=75, y=359)

AccountSystem.protocol("WM_DELETE_WINDOW", lambda: exit())

AccountSystem.mainloop()
