from flask import Flask,redirect,render_template,request
import pandas as pd
import numpy as np
from validate_user import login,signup
import joblib
import os

app=Flask(__name__)

@app.route("/")
def home():
    return render_template('login.html')

@app.route("/login",methods=['POST','GET'])
def login_user():
    if request.method == 'POST':
        email=request.form.get('email')
        password=request.form.get('password')
        
        data=(email,password)
        res=login(data)
        if res:
            return redirect('/model')
        else:
            return render_template("signup.html",message="Email not register:Please Signup",messagetype="error")
    return render_template("login.html")
        
@app.route("/signup",methods=['POST','GET'])
def signup_user():
    if request.method == 'POST':
        name=request.form.get('name')
        email=request.form.get('email')
        password=request.form.get('password')
        phone=request.form.get('phone')
        data=(name,email,password,phone)
        res=signup(data)
        if res:
            return redirect('/model')
        else:
            return render_template('login.html',message='Email already register.Please login',message_type='error')
    return render_template("signup.html")

@app.route("/model",methods=['GET','POST'])
def model_type():
    if request.method == 'POST':
        col=['Vehicle_Type','State','City','Brand','Model','Fuel_Type','Transmission','Year','Engine_Size','Mileage','Power','Seats']
        int_column=['Year','Engine_Size','Seats']
        float_column=['Mileage','Power']
        data=[]
        vehicle=""
        for i in col:
            if i=='Vehicle_Type':
                vehicle=request.form.get(f'{i}')
            else:
                if i in int_column:
                    val=int(request.form.get(f'{i}'))
                elif i in float_column:
                    val=float(request.form.get(f'{i}'))
                else:
                    val=request.form.get(f'{i}')
                data.append(val)
        # print(data)
        
        model = joblib.load(os.path.join(os.path.dirname(__file__), f"{vehicle}_model.pkl"))
        encoder = joblib.load(os.path.join(os.path.dirname(__file__), f"{vehicle}_encoder.pkl"))
        scaler = joblib.load(os.path.join(os.path.dirname(__file__), f"{vehicle}_scaler.pkl"))
        
        df=pd.DataFrame([data],columns=col[1:])
        
        # print(df)
        col1=['Year','Engine_Size','Mileage','Power','Seats']
        # print(col)
        df[col1]=scaler.transform(df[col1])
        
        col2=['State','City','Brand','Model','Fuel_Type','Transmission']
        # print(col2)
        encode=encoder.transform(df[col2])
        encode_df=pd.DataFrame(encode,columns=encoder.get_feature_names_out(col2))
        final_df=pd.concat([df.drop(columns=col2,axis=1),encode_df],axis=1)
        
        # print(final_df.columns)
        # numeric_cols = ['Year','Engine_Size','Mileage','Power','Seats']
        # final_df = scaler.transform(final_df)
        price=model.predict(final_df)[0]
        
        if price >= 10000000:
            formatted_price = f"{price/10000000:.2f} Crore"
        elif price >= 100000:
            formatted_price = f"{price/100000:.2f} Lakh"
        else:
            formatted_price = f"{price:,.0f}"
            
        return render_template('model.html', predicted_price=formatted_price)
        
    return render_template("model.html")

if __name__=="__main__":
    app.run(host="0.0.0.0", port=10000, debug=True)
