import smtplib
import socket as sc
from datetime import datetime
from ping3 import ping
import csv
import nmap3
import time

class enviarMensagens:
  def __init__(self, mensagem):
    self.mensagem = mensagem
      
  def enviar_email(self, email, titulo, message):
      sender = "Diego Crisostomo <diego.crisostomo@hotmail.com>"
      message = f"""\
      Subject: {titulo}
      To: {email}
      From: {sender}
      {message}"""
      with smtplib.SMTP("smtp.mailtrap.io", 2525) as server:
          server.login("21782f6b065f67", "026d5db4f0c38c")
          server.sendmail(sender, email, message)

  def verificar_servidor(self, porta):
    resultado_socket = []
    testconnect = sc.socket(sc.AF_INET, sc.SOCK_STREAM)         
    try:
      testconnect.connect((self.mensagem, porta))
      mensagem = "Verificado com sucesso " + str(datetime.today()) + " no IP/dominio " + self.mensagem 
      resultado_socket.append(mensagem)      
      with open(r'sucesso.csv', 'a') as f:
        writer = csv.writer(f)
        writer.writerow(resultado_socket)      
      testconnect.close()
    except:
      mensagem = "Ocorreu um erro as " + str(datetime.today()) + " no IP/dominio " + self.mensagem
      resultado_socket.append(mensagem)
      with open(r'erro.csv', 'a') as f:
        writer = csv.writer(f)
        writer.writerow(resultado_socket)        
      self.enviar_email("Diego Crisostomo <diego@teste.com.br>", "Erro durante a execução".encode('utf-8'), mensagem)
      testconnect.close()
  
  def verificar_portas (self, tempo=2):  
    nmap_results = []
    nmap = nmap3.Nmap()
    results = nmap.scan_top_ports(self.mensagem)
    nmap_results.append(results)
    with open(r'nmap.csv', 'a') as f:
        writer = csv.writer(f)
        writer.writerow(nmap_results)
    time.sleep(int(tempo))
  
  def realizar_ping(self, tempo=2):
    resultado_ping = []
    resultado = ping(self.mensagem, unit='ms')         
    if resultado == False: 
      mensagem = "Ocorreu um erro as " + str(datetime.today()) + " no ping IP/dominio " + self.mensagem     
      self.enviar_email("Diego Crisostomo <diego@teste.com.br>", "Erro durante a execução do ping ".encode('utf-8'), mensagem)
    else:
      resultado_ping.append(str(resultado) + "ms")
      with open(r'ping.csv', 'a') as f:
        writer = csv.writer(f)
        writer.writerow(resultado_ping)
    time.sleep(int(tempo)) 


#dominios_ips = ['google.com.br', 'www.google.com.br', 'minhacasa.edu.br']
#for i in dominios_ips:
#  resultado = enviarMensagens(i)
#  resultado.verificar_servidor(80)
#  resultado.verificar_portas()
#  resultado.realizar_ping()

resultado = enviarMensagens('minhacasa.edu.br')
resultado.realizar_ping()