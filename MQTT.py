
#teste com app de mqtt

import paho.mqtt.client as mqtt
import sys
from gtts import gTTS
import os
import threading as threading, time
    
#Callback - conexao ao broker realizada
def on_connect(client, userdata, flags, rc):
    print("[STATUS] Conectado ao Broker. Resultado de conexao: "+str(rc))
 
    #faz subscribe automatico no topico
    client.subscribe("AVISOIFCEMaracanau")
 
#Callback - mensagem recebida do broker
def on_message(client, userdata, msg):
    MensagemRecebida = str(msg.payload)
    
    print("[MSG RECEBIDA] Topico: "+msg.topic+" / Mensagem: "+MensagemRecebida)
    converter_texto_voz(MensagemRecebida)
    return MensagemRecebida
 
#callback - converter texto em voz
def converter_texto_voz(MensagemRecebida):
    #rotina de conversao texto em voz
    MesagemRecebida = str(MensagemRecebida[5:])
    AudioTexto = gTTS(text=MensagemRecebida, lang='pt')
    
    arq = open('/home/pi/mqtt.txt', 'w')
    
    global contador

    if (contador == 0):
        AudioTexto.save("/home/pi/audio.mp3")
        contador += 1
        arq.write(str(contador))
    elif (contador == 1):
        AudioTexto.save("/home/pi/audio1.mp3")
        contador += 1
        arq.write(str(contador))
    elif (contador >= 2):
        AudioTexto.save("/home/pi/audio.mp3")
        contador = 2
        arq.write(str(contador))
    arq.close()

class AudioThread(threading.Thread):
    def __init__(self, meuId, cont, mutex, contador):
        self.meuId = meuId
        self.cont = cont
        self.contador = contador
        self.mutex = mutex
        threading.Thread.__init__(self)
    
    #callback - reproduzir audio
    def run(self):
        while(True):
            with self.mutex:
                if (contador == 0):
                    #print("Sem auidos cadastrados. \n")
                    #os.system("mpg321 /home/pi/audio.mp3")
                    time.sleep(5)
                    x=0
                elif(contador == 1):
                    os.system("mpg321 /home/pi/audio.mp3")
                    time.sleep(5)
                elif(contador >= 2): 
                    os.system("mpg321 /home/pi/audio.mp3")
                    time.sleep(5)
                    os.system("mpg321 /home/pi/audio1.mp3")
                    time.sleep(5)    
    
arq = open('/home/pi/mqtt.txt', 'r')

contador = int(arq.read())
print(type(contador))
arq.close()

stdoutmutex = threading.Lock()
threads = []
thread1 = AudioThread(1, 100, stdoutmutex, contador)
thread1.start()

for thread in threads:
    thread.join()

#programa principal:
try:
    print("[STATUS] Inicializando MQTT...")
    #inicializa MQTT:
    client = mqtt.Client()

    client.on_connect = on_connect
    client.on_message = on_message  

    client.connect("mqtt.eclipse.org", 1883, 80)
   
    client.loop_forever() 
    print('Saindo da thread principal')

except KeyboardInterrupt:
        print ("\nCtrl+C pressionado, encerrando aplicacao e saindo...")
        sys.exit(0)