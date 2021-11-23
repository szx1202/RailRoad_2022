// ver 2.0 --> servopos shortened from 4 to 3 Byte i.e. fw12 to f12)
// ver 2.1 --> added 3rd servo series
// ver 2.2 --| added single turnout servos
// ver 3.0 --> created Turn_FW and Turn_BW funtion for servo rotation control
// ver 4.0 --| added code for line occupancy and Manual Block  
// ver 4.1 ..> simplified interrupt routine

#include "BluetoothSerial.h"
#if !defined(CONFIG_BT_ENABLED) || !defined(CONFIG_BLUEDROID_ENABLED)
#error Bluetooth is not enabled! Please run `make menuconfig` to and enable it
#endif

BluetoothSerial SerialBT;

#include <Adafruit_PWMServoDriver.h>

// called this way, it uses the default address 0x40
//SDA (default is GPIO 21) SCL (default is GPIO 22)

Adafruit_PWMServoDriver pwm = Adafruit_PWMServoDriver();
const int numItems=16; //number of servo's to manage

//https://www.makerslab.it/pca9685-controllo-i2c-a-16-canali-pwm-per-led-e-servomotori/
#define SERVOMIN  150 //set 150 300  this is the 'minimum' pulse length count (out of 4096)
#define SERVOMAX  185 //set 175 600  this is the 'maximum' pulse length count (out of 4096)
//Led to check BT Connection

char servopos[3]; //4 is the string leght for Bluethooth command (F12, R12,...)

// block for IR module
unsigned int busyPins[]= {0, 0, 0, 0, 32, 33};  // array for occupation signal where connected occupation modules
unsigned int itrPins []= {0, 0, 0, 0, 16, 17}; //array for pin where to connect ifr chip data pin used for interrpt 
unsigned int relayPins[]= {19, 19, 0, 0, 0,0};  // array for Line Halt-Go 

int valBlock;     // variable to store result
int idxIR=0;      // store which IR started interrupt
int BTled=12; // Led for BT status
String btBlock; // String to be sent via BT with the Block info LHx/LLx  
bool isFree = true ; // char to store the status after interrupt false=blocked true=free

void IRAM_ATTR isr_4() {
  idxIR=4;
} 

void IRAM_ATTR isr_5() {
  idxIR=5;
  //isFree=(!isFree);
}  

void setup()
{
  //Setup usb serial connection to computer
  Serial.begin(115200);
//  pinMode(BTled, OUTPUT);
//  digitalWrite(BTled, LOW); 
  
 SerialBT.begin("ESP32Track"); //Bluetooth device name
 Serial.println("The device started, now you can pair it with bluetooth!");
  
  // Pin for block module set as output
  for (int i=0; i<6;i++){
    if (busyPins[i]!=0){
      pinMode(busyPins[i], OUTPUT);
      digitalWrite(busyPins[i], LOW); //signal leds block OFF
    }
  }
   for (int i=0; i<6;i++){
    if (relayPins[i]!=0){
      pinMode(relayPins[i], OUTPUT);
      digitalWrite(relayPins[i], LOW); //array of relay
    }
  }
   
   for (int i=0; i<6;i++){
    if (itrPins[i]!=0){
      pinMode(itrPins[i], INPUT_PULLUP);
    }
  }
    
  // Triggers detectMotion isr function on rising mode to turn the relay on, if the condition is met
  attachInterrupt(digitalPinToInterrupt(itrPins[4]),isr_4, CHANGE);
  attachInterrupt(digitalPinToInterrupt(itrPins[5]),isr_5,CHANGE);
  //attachInterrupt(itrPins[5],isr_6,RISING );
  
  // PWM setup for Servos
  pwm.begin();
  delay(10);
  pwm.setPWMFreq(60);  // Analog servos run at ~60 Hz updates
 
  
  for(int i=0; i<numItems; i++)
    {
     Turn_FW(i);     
     delay(100);
  }
}

void loop()
{
String idxBlock;

// Serial.println (digitalRead(17));
if (idxIR!=0){
  switch (idxIR) {
    case 4: 
      idxBlock= "4";
      //Serial.println("idxIR_4= ");
      //Serial.println(idxIR);
      break;
     case 5:
      idxBlock= "5";
      //Serial.println("idxIR_5= ");
      //Serial.println(idxIR);
      break; 
  }
   
  valBlock = digitalRead(itrPins[idxIR]); // Read valBlockue from block sensor 
  Serial.print("isFree prima= ");
  Serial.println(isFree);
    
  if((digitalRead(itrPins[idxIR])==0)){    
    btBlock="HD"+idxBlock;
    Serial.print ("  btBlock= ");
    Serial.println(btBlock);
    isFree=false;
    }
    if((digitalRead(itrPins[idxIR])==1)){    
      btBlock="LD"+idxBlock;
      Serial.println ("btBlocke= ");
      Serial.println(btBlock);
      isFree=true;
    }  
    if (btBlock!=""){
      SerialBT.write(btBlock[0]);
      SerialBT.write(btBlock[1]);
      SerialBT.write(btBlock[2]);
      if (btBlock[0] == 'L') {
        digitalWrite(busyPins[idxIR], LOW);
      } 
      if (btBlock[0] == 'H') 
      {
      digitalWrite(busyPins[idxIR], HIGH);
      //Serial.print(busyPins[idxIR]);
      }
      //Serial.println(btBlock[1]);
      btBlock="";
      SerialBT.flush(); 
      delay(500);
    }
    //interrupts();
    idxIR=0;
  }
  
  if (SerialBT.available())
  
  { 
    //Serial.println ("BT OK");
    
    digitalWrite(BTled, LOW); 
    for (int i=0;i<3;i++){
      servopos[i] = SerialBT.read();
      //Serial.print(servopos[i]);
      //Serial.println();
     }
     
  SerialBT.flush();
        if ((servopos[0] == 'l')  && (servopos[2]=='1')) { // Check Track 1
          if (servopos[1]=='h'){
            //Serial.println(busyPins[0]);
            digitalWrite(relayPins[0], HIGH);
          }
        else{
          //Serial.println("GO track T1");
          //Serial.println(busyPins[0]);
          digitalWrite(relayPins[0], LOW);  
        }
      }
      if ((servopos[0] == 'l')  && (servopos[2]=='2')) { // Check Track 1
          if (servopos[1]=='h'){
            //Serial.println(busyPins[1]);
            digitalWrite(relayPins[1], HIGH);
          }
        else{
          //Serial.println("GO track T2");
          //Serial.println(busyPins[1]);
          digitalWrite(relayPins[1], LOW);  
        }
      }
      if ((servopos[0] == 'l')  && (servopos[2]=='5')) { // Check Track 1
          if (servopos[1]=='h'){
            //Serial.println(busyPins[4]);
            digitalWrite(relayPins[4], HIGH);
          }
        else{
          //Serial.println("GO track R2");
          //Serial.println(busyPins[4]);
          digitalWrite(relayPins[4], LOW);  
        }
      }
      
    if ((servopos[0] == 'f') && (servopos[1]=='2')) {                     //if (realservo >= 1000 && realservo <1180) in case of sliders
        Serial.println("fw23");
        Turn_FW(2);
      }
    if ((servopos[0] == 'r') && (servopos[1]=='2')){
       Serial.println("rw23");
       Turn_BW(2);
      }
      
    if ((servopos[0] == 'f') && (servopos[1]=='4')) {                     //if (realservo >= 1000 && realservo <1180) in case of sliders
        Serial.println("fw45");
        Turn_FW(4);
        }
        
    if ((servopos[0] == 'r') && (servopos[1]=='4')){
       Serial.println("bw45");
       Turn_BW(4);
      }
    
     if ((servopos[0] == 'f') && (servopos[1]=='5')) {                     //if (realservo >= 1000 && realservo <1180) in case of sliders
        Serial.println("f55");
        pwm.setPWM(10, 0, 135);
      }

     if ((servopos[0] == 'r') && (servopos[1]=='5')) {                     //if (realservo >= 1000 && realservo <1180) in case of sliders
        Serial.println("r55");
        pwm.setPWM(10, 0, 180);
      }
     
     if ((servopos[0] == 'f') && (servopos[1]=='6')) {                     //if (realservo >= 1000 && realservo <1180) in case of sliders
        Serial.println("f66");
        //Turn_FW(12);
        pwm.setPWM(12, 0, 145);
      }

     if ((servopos[0] == 'r') && (servopos[1]=='6')) {                     //if (realservo >= 1000 && realservo <1180) in case of sliders
        Serial.println("r66");
        //Turn_BW(12);
        pwm.setPWM(12, 0, 185);
      }
     if ((servopos[0] == 'f') && (servopos[1]=='7')) {                     //if (realservo >= 1000 && realservo <1180) in case of sliders
        Serial.println("f77");
        Turn_FW(14);
      }

     if ((servopos[0] == 'r') && (servopos[1]=='7')) {                     //if (realservo >= 1000 && realservo <1180) in case of sliders
        Serial.println("r77");
        Turn_BW(14);
      }
      
    if (servopos[0] == 't') {
      Serial.println("TestBT");
      SerialBT.write('k');
    }
    
    if (servopos[0] == 'i') {
      Serial.println("reset");
       for(int i=0; i<numItems; i++)
      {
        //Serial.println(i);
        Turn_FW(i);
       }
    }
  }
//delay(100);
}

void Relay_SW (){
Serial.print("Relay");
}
void Turn_BW(uint16_t servonum) {
  //Serial.println(servonum);
  for (uint16_t pulselen = SERVOMIN; pulselen < SERVOMAX; pulselen++) {
    pwm.setPWM(servonum, 0, pulselen);
    delay (5);
  }
}

void Turn_FW(uint16_t servonum) {
 //Serial.println(servonum);
 for (uint16_t pulselen = SERVOMAX; pulselen > SERVOMIN; pulselen--) {
    pwm.setPWM(servonum, 0, pulselen);
    delay (5);
  }
}
