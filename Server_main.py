from flask import Flask, request
import socket
import pandas as pd
import time
import logging
import tensorflow
import keras

app = Flask(__name__)

errors = []
locations = []
velocities = []
model_path = ""
model = keras.models.load_model(model_path)


@app.route('/SignUp/')
def SignUp():
    """
    Create the new account
    :return: Whether creating is successful
    """
    # load the account information from the file
    df = pd.read_csv('user_info.csv', usecols=['username', 'password']).astype(str)

    # get the username and the password
    user = request.args.get('username')
    password = request.args.get('password')

    # print(f"({user, type(user)}\n"
    #       f"{password, type(password)}")

    # check whether the account has existed
    check = df.query(f"username == '{user}'")
    if not check.empty:
        return f'This account has existed!'

    # create the new account
    new_df = df.append({'username': user, 'password': password}, ignore_index=True)

    # rewrite the information of the account
    new_df.to_csv('user_info.csv')

    # return prompt information
    return 'Create account successfully!'


@app.route('/LogIn/')
def LogIn():
    """
    CHeck the user name and password
    :return: 0 for login unsuccessfully, 1 fpr login successfully.
    """
    # get the time of the server
    struct_time = time.localtime(time.time())

    # get the password and the username
    psd = request.args.get('password')
    user = request.args.get('username')
    ip = request.remote_addr

    # load the account information from the file
    df = pd.read_csv('user_info.csv', usecols=['username', 'password']).astype(str)

    # find the username and password from the data list
    res = df.query(f"username == '{user}'")

    # check the password
    if (not res.empty) and (res.iloc[0]['password'] == psd):
        logging.info(
            f"{struct_time.tm_year}/{struct_time.tm_mon}/{struct_time.tm_mday}"
            f" {struct_time.tm_hour}:{struct_time.tm_min}:{struct_time.tm_sec} "
            f"{request.remote_addr} {res.iloc[0]['username']} log in successfully!")
        return "1"

    # return the wrong signal
    logging.warning(
        f"{struct_time.tm_year}/{struct_time.tm_mon}/{struct_time.tm_mday}"
        f" {struct_time.tm_hour}:{struct_time.tm_min}:{struct_time.tm_sec} "
        f"{request.remote_addr} {user} failed to log in!")
    return "0"


@app.route("/predict/")
def predict():
    """
    Predict the error base on the information provided by the train.
    TODO: import the model based on tensorflow.
    :return: The error if brake at that time.
    """
    curr_loc = request.args.get("Location")
    curr_vel = request.args.get("Velocity")
    curr_err = model.predict()
    velocities.append(float(curr_vel))
    locations.append(float(curr_loc))
    errors.append(curr_err)
    return str(curr_err)


@app.route("/record/")
def record():
    """
    Record the data into the data file.
    :return: None or some signal for check
    """


@app.route("/check/")
def checkIP():
    """
    Check whether the customer link the right ip address of the server.
    :return: The signal for check.
    """
    return "LHDL_YYDS_2021"


def getIPAddress(ip):
