import smtplib
import RPi.GPIO as GPIO
import time
import cv2

from email.mime.multipart import MIMEMultipart
from email.mime.text import MIMEText
from email.mime.image import MIMEImage


#Email Variables
SMTP_SERVER = 'smtp.gmail.com' #Email Server
SMTP_PORT = 587 #Server Port
GMAIL_USERNAME = '' 
GMAIL_PASSWORD = ''

GPIO.setmode(GPIO.BOARD) #Set GPIO to pin numbering
pir = 8 #Assign pin 8 to PIR
led = 10 #Assign pin 10 to LED
GPIO.setup(pir, GPIO.IN) #Setup GPIO pin PIR as input
GPIO.setup(led, GPIO.OUT) #Setup GPIO pin for LED as output
print ("Sensor initializing . . .")
time.sleep(2) #Give sensor time to startup
print ("Active")
print ("Press Ctrl+c to end program")


class Emailer:
    def sendmail(self, recipient, subject, content, image):

        #Create Headers
        emailData = MIMEMultipart()
        emailData['Subject'] = subject
        emailData['To'] = recipient
        emailData['From'] = GMAIL_USERNAME

        #Attach our text data
        emailData.attach(MIMEText(content))

        #Create our Image Data from the defined image
        imageData = MIMEImage(open(image, 'rb').read(), 'jpg')
        imageData.add_header('Content-Disposition', 'attachment; filename="image.jpg"')
        emailData.attach(imageData)

        #Connect to Gmail Server
        session = smtplib.SMTP(SMTP_SERVER, SMTP_PORT)
        session.ehlo()
        session.starttls()
        session.ehlo()

        #Login to Gmail
        session.login(GMAIL_USERNAME, GMAIL_PASSWORD)

        #Send Email & Exit
        session.sendmail(GMAIL_USERNAME, recipient, emailData.as_string())
        session.quit

sender = Emailer()
'''
sendTo = ''
emailSubject = "Someone is at your door!"
emailContent = "Someone looks sus at: " + time.ctime()
sender.sendmail(sendTo, emailSubject, emailContent)
print("Email Sent")
'''
try:
        while True:
                if GPIO.input(pir) == True: #If PIR pin goes high, motion is detected
                        print ("Motion Detected!")
                        cap = cv2.VideoCapture(0)
                        ret,frame = cap.read()
                        if ret:
                                cv2.imwrite('/home/pi/Desktop/image.jpg', frame)

                        image = '/home/pi/Desktop/image.jpg'
                        sendTo = ''
                        emailSubject = "Someone at your door!!"
                        emailContent = "someone looking sus at: " + time.ctime()
                        sender.sendmail(sendTo, emailSubject, emailContent, image)
                        print("Email Sent")
                        GPIO.output(led, True) #Turn on LED
                        time.sleep(4) #Keep LED on for 4 seconds
                        GPIO.output(led, False) #Turn off LED
                        time.sleep(0.1)

except KeyboardInterrupt: #Ctrl+c
        pass #Do nothing, continue to finally

finally:
        GPIO.output(led, False) #Turn off LED in case left on
        GPIO.cleanup() #reset all GPIO
        print ("Program ended")
