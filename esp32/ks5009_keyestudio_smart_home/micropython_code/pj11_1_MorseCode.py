# Import machine, time and dht modules. 
from machine import Pin, PWM
from time import sleep_ms, ticks_ms 
from machine import I2C, Pin 
from i2c_lcd import I2cLcd 

DEFAULT_I2C_ADDR = 0x27

i2c = I2C(scl=Pin(22), sda=Pin(21), freq=400000) 
lcd = I2cLcd(i2c, DEFAULT_I2C_ADDR, 2, 16)

button1 = Pin(16, Pin.IN, Pin.PULL_UP)
button2 = Pin(27, Pin.IN, Pin.PULL_UP)
count = 0
time_count = 0
password = ""   #Enter password
correct_password = "-.-"  #Correct password
lcd.putstr("Enter password")
pwm = PWM(Pin(13))  
pwm.freq(50)

while True:
    btnVal1 = button1.value()  # Read the value of button 1
    if(btnVal1 == 0):
        sleep_ms(10)
        while(btnVal1 == 0):
            time_count = time_count + 1  #Start counting the pressed time of the button
            sleep_ms(200)                #The time is 200ms cumulative
            btnVal1 = button1.value()
            if(btnVal1 == 1):
                count = count + 1
                print(count)
                print(time_count)
                if(time_count > 3):      #If the pressed time of the button is more than 200*3ms，add"-" to  password
                    lcd.clear()
                    #lcd.move_to(1, 1)
                    password = password + "-"
                else:
                    lcd.clear()
                    password = password + "."  #Otherwise add "."
                lcd.putstr('{}'.format(password)) 
                time_count = 0
                
    btnVal2 = button2.value()
    if(btnVal2 == 0):
        if(password == correct_password):  #If the password is correct
            lcd.clear()
            lcd.putstr("open")
            pwm.duty(128)  #Open the door
            password = ""  #Remove the password
            sleep_ms(1000)
        else:              #If the password is wrong
            lcd.clear()
            lcd.putstr("error")
            pwm.duty(25)  #Close the door
            sleep_ms(2000)
            lcd.clear()
            lcd.putstr("enter again")
            password = ""  #Remove the password


