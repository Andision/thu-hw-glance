import wlxt
username=input("Your Account:")
userpswd=input("Your Password:")

hw_list=wlxt.get_wjhw(str(username).strip(),str(userpswd).strip())
for i in hw_list:
    print(i)