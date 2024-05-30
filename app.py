from flask import Flask,render_template,url_for, request, redirect
import json
from csv import DictReader

app = Flask(__name__)

userdata = r"C:\Users\OM\Desktop\CreditCardAppDemo\credentials.json"

def get_userdata():

    with open(userdata) as f:
        data = json.load(f)
    
    return data["Users"]

def add_userdata(data):
    
    with open(userdata,'w') as f:
        json.dump(data, f, indent=4)

def isValidUser(userName,password):
    
    isValid = False
    userData = get_userdata()
    
    for user in userData:
        
        if user['username'] == userName and user['password'] == password:
            isValid = True
            return isValid
    
    return isValid

@app.route("/details",methods=["GET","POST"])
def details():
    if request.method == "GET":
        # open file in read mode
        with open('transactions.csv', 'r') as read_obj:
            # pass the file object to DictReader() to get the DictReader object
            dict_reader = DictReader(read_obj)
            # get a list of dictionaries from dct_reader
            transactions = list(dict_reader)
            # print list of dict i.e. rows
            print(transactions)

        return render_template("details.html", transactions=transactions)
    return render_template("details.html", transactions=transactions)


@app.route("/register",methods=["GET","POST"])
def register():
    
    if request.method == "POST":    
        
        fname = request.form.get("fname")
        lname = request.form.get("lname")
        username = request.form.get("uname")
        password = request.form.get("password") 
        email = request.form.get("email") 

        userData = get_userdata()        
        temp = {"fname":fname, "lname":lname, "username":username, "email":email, "password": password}
        userData.append(temp)
        finalData = {"Users":userData}
        add_userdata(finalData)

        return render_template('login.html')

    return render_template('register.html')


@app.route("/login",methods=["GET","POST"])
def login():
    
    if request.method == "POST":
        
        username = request.form.get("uname")
        password = request.form.get("password") 

        if isValidUser(username,password):
            return redirect(url_for('home'))
        else:
            return redirect(url_for('register'))

    return render_template('login.html')

@app.route("/home",methods=["GET","POST"])
def home():
    return render_template('home.html')

@app.route("/transactioDetailsForm",methods=["GET","POST"])
def transactioDetailsForm():
    if request.method == "GET":
        return render_template('transactionDetailsForm.html')


@app.route("/validateTransaction",methods=["GET","POST"])
def validateTransaction():
    if request.method == "POST":
        ccnum = request.form.get("inputCCNumber")
        bank = request.form.get("inputBank")
        methodTransaction = request.form.get("inputTransactionMethod")
        city = request.form.get("inputCity")  

        print(type(ccnum),ccnum)
        print(type(bank),bank)
        print(type(methodTransaction),methodTransaction)
        print(type(city),city)
        # open file in read mode
        with open('transactions.csv', 'r') as read_obj:
            # pass the file object to DictReader() to get the DictReader object
            dict_reader = DictReader(read_obj)
            # get a list of dictionaries from dct_reader
            transactions = list(dict_reader)
        
        for transaction in transactions:
            print(transaction)
            if (transaction['Credit Card Number']==str(ccnum).strip() and transaction['Bank']==bank and transaction['Method of Transaction']==methodTransaction and transaction['City']==city):
                
                return render_template('transactionDetailsForm.html',flag='success')

        return render_template('transactionDetailsForm.html',flag='danger')
    return render_template('transactionDetailsForm.html')

@app.route("/about",methods=["GET","POST"])
def about():
    return render_template('about.html')


