import pickle
from flask import Flask, request
import pandas as pd
import time
import logging
import keras
import os
import socket

app = Flask(__name__)

errors = []
locations = []
velocities = []
# TODO: the file name of the model and how to predict
model_path = ""
model = keras.models.load_model(model_path)
datapath = "data/"


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

    log_df = pd.read_csv("data/log/log_info.csv")

    # find the username and password from the data list
    res = df.query(f"username == '{user}'")

    # check the password
    if (not res.empty) and (res.iloc[0]['password'] == psd):
        logging.info(
            f"{struct_time.tm_year}/{struct_time.tm_mon}/{struct_time.tm_mday}"
            f" {struct_time.tm_hour}:{struct_time.tm_min}:{struct_time.tm_sec} "
            f"{ip} {res.iloc[0]['username']} log in successfully!")

        # Write the log information into the og file
        new_log_df = log_df.append({"date": f"{struct_time.tm_year}/{struct_time.tm_mon}/{struct_time.tm_mday}",
                                    "time": f"{struct_time.tm_hour}_{struct_time.tm_min}_{struct_time.tm_sec}",
                                    "username": user,
                                    "ip": ip})
        new_log_df.to_csv("data/log_info.csv")
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
    struct_time = time.localtime(time.time())
    user = request.args.get("username")
    user_dir = os.path.join(datapath, user)
    data_dir = os.path.join(user_dir, f"{struct_time.tm_year}_{struct_time.tm_mon}_{struct_time.tm_mday}")
    data_name = os.path.join(data_dir, f"{struct_time.tm_hour}_{struct_time.tm_min}_{struct_time.tm_sec}.pkl")
    if not os.path.exists(user_dir):
        os.makedirs(user_dir)

    if not os.path.exists(data_dir):
        os.makedirs(data_dir)

    with open(data_name, "wb") as file:
        pickle.dump({"Errors": errors,
                     "Locations": locations,
                     "Velocities": velocities}, file)
    logging.info(f"{data_name} done!")

    # clear the list of the data.
    errors.clear()
    locations.clear()
    velocities.clear()

    return "1"


@app.route("/check/")
def checkIP():
    """
    Check whether the customer link the right ip address of the server.
    :return: The signal for check.
    """
    return "LHDL_YYDS_2021"


def get_host_ip():
    """
    Get the IP address of the local host
    :return: IP address for the local host
    """
    try:
        s = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
        s.connect(('8.8.8.8', 80))
        ip = s.getsockname()[0]
    finally:
        s.close()

    return ip


if __name__ == "__main__":
    """Run the Server"""
    local_IP = get_host_ip()
    print(local_IP)
    app.run(host=local_IP)
