# LineUp
Kivy app with flask s backend

This is a python project for creating virtual queues, the merchants start online window where customer come for their query 
one by one but not necessarily wait in long queues while the merchant is dealing the one at start of line

The files merchant_side/MerchantFlaskAPI.py is the api for a merchant to register itself with the LineUp app so that its customers 
can use it
give the below command to run it
/LineUp/merchant_side$ python MerchantFlaskAPI.py

The files user_side/StepperFlaskAPI.py is the api for the user to add himself/herself in a line 
/LineUp/user_side$ python StepperFlaskAPI.py

The files merchantApp_userApp/main.py and merchantApp_userApp/main_status.py are python apps with Kivy GUI 

For the merchant to start a window for a line of customers
/LineUp/merchantApp_userApp$python main.py

To check the current number in the running line
/LineUp/merchantApp_userApp$python main_status.py

