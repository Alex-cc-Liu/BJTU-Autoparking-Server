# BJTU-Autoparking-server


# Requirement:
Flask, socket, pandas, time, logging, keras, tensorflow


# Function SignUp

通过 get 请求传递的参数：{"password": , "username": }

访问本端口通过 ip: IP地址:端口号/SignUp/

return: 创建账户失败：'This account has existed!'
        创建账户成功："Create account successfully!"


# Function LogIn

功能：判断是否登陆成功，并在控制台输出提示。

通过 get 请求传递的参数：{"password": , "username": }

访问本端口通过 ip: IP地址:端口号/LogIn/

return: 账户登陆失败：'0'
        账户登陆成功："1"



# Function predict

功能：通过列车传回的运行数据通过神经网络进行预测

通过 get 请求传递的参数：{"Location": , "Velocity": }

访问本端口通过 ip: IP地址:端口号/predict/

return: “预测的误差”


# Function record

功能：将列车传回的数据记录到文件中

通过 get 请求传递的参数：{”record“:}

当 {”record“: “1”} 时代表实验结束，将本次实验数据一次性计入到文档，并清空全局变量，等待下一次实验开始
当 {”record“: “0”} 时表示实验未开始或未结束，不做任何动作。

访问本端口通过 ip: IP地址:端口号/record/

return: “预测的误差”

# Function checkIP

功能：返回一个特定的字符串以确定列车正确连接服务器

不需要传递参数

访问本端口通过 ip: IP地址:端口号/checkIP/

return: “LHDL_YYDS_2021”

# getIPAddress(ip)

功能：通过开放API和用户的IP地址确定登陆用户的地理位置

传参：用户的登陆IP地址

return: 地理信息
