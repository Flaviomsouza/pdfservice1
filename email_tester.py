import smtplib
import email.message


email_body = 'Testando cronjobs'

msg = email.message.Message()
msg['Subject'] = 'TESTE CRONJOB'
msg['From'] = 'calebbds@gmail.com'
msg['To'] = 'calebporto@hotmail.com'
password = 'qfhrpmbdbbmyrlna'
msg.add_header('Content-Type', 'text/html')
msg.set_payload(email_body)

s = smtplib.SMTP('smtp.gmail.com: 587')
s.starttls()
s.login(msg['From'], password)
s.sendmail(msg['From'], msg['To'], msg.as_string().encode('utf-8'))