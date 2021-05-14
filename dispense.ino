#include <Button.h>
#include <Servo.h>
//Button button1(2);
//Button button2(3);
//Button dispense(4);

int start_time1 = 175;
int end_time1 = 320;
int curr_time = 300;
int amount1 = 1;
int time_taken1; 
int user_id = 21;
int start_time2 = 250;
int end_time2 = 450;
int amount2 = 1;
int time_taken2;
int rotation = 512;
bool taken1 = false;
bool taken2 = false;
bool state;
int slot1 = 12;
int slot2 = 13;
//char * machine = "qwerty";

bool active = true;

int pause = 3;
Servo slot;

void dispense1(int steps)
{ 
  if (steps >= 0)
  {
    steps = steps / 4;
    for (int i = 0; i < steps; i++)
    { 
      digitalWrite(8, HIGH); 
      digitalWrite(9, LOW); 
      digitalWrite(10, LOW); 
      digitalWrite(11, LOW); 
      delay(pause); 
      digitalWrite(8, LOW); 
      digitalWrite(9, HIGH); 
      digitalWrite(10, LOW); 
      digitalWrite(11, LOW); 
      delay(pause); 
      digitalWrite(8, LOW); 
      digitalWrite(9, LOW); 
      digitalWrite(10, HIGH); 
      digitalWrite(11, LOW); 
      delay(pause); 
      digitalWrite(8, LOW); 
      digitalWrite(9, LOW); 
      digitalWrite(10, LOW); 
      digitalWrite(11, HIGH);
    } 
  
  }
} 

void dispense2(int steps)
{ 
  if (steps >= 0)
  {
    steps = steps / 4;
    for (int i = 0; i < steps; i++)
    { 
      digitalWrite(4, HIGH); 
      digitalWrite(5, LOW); 
      digitalWrite(6, LOW); 
      digitalWrite(7, LOW); 
      delay(pause); 
      digitalWrite(4, LOW); 
      digitalWrite(5, HIGH); 
      digitalWrite(6, LOW); 
      digitalWrite(7, LOW); 
      delay(pause); 
      digitalWrite(4, LOW); 
      digitalWrite(5, LOW); 
      digitalWrite(6, HIGH); 
      digitalWrite(7, LOW); 
      delay(pause); 
      digitalWrite(4, LOW); 
      digitalWrite(5, LOW); 
      digitalWrite(6, LOW); 
      digitalWrite(7, HIGH);
    } 
  
  }
} 



void setup() {
  // put your setup code here, to run once:
//  dispense.begin();
  slot.attach(3);
  pinMode(4, OUTPUT);
  pinMode(5, OUTPUT);
  pinMode(6, OUTPUT);
  pinMode(7, OUTPUT);
  pinMode(8, OUTPUT);
  pinMode(9, OUTPUT);
  pinMode(10, OUTPUT);
  pinMode(11, OUTPUT);
  pinMode(2, INPUT);
  pinMode(slot1, INPUT);
  pinMode(slot2, INPUT);
  Serial.begin(9600);

}

void loop() {
  while (active)
  {
//      get_data();
//      curr_time = get_time();
//      state = dispense.pressed();
      state = digitalRead(2);
//      Serial.println(state);
      if (start_time1 <= curr_time && end_time1 >= curr_time && !taken1)
      {
        if(state)
        {
          dispense1(amount1*rotation);
            
           Serial.println("HI");
//            digitalWrite(8, HIGH);
//            delay(500);
//            digitalWrite(8, LOW);
          time_taken1 = curr_time;
          taken1 = true;
        }
      }
      else
      {
        if (start_time1 > curr_time)
        {
          taken1 = false;
        }
      }


      
      if (start_time2 <= curr_time && end_time2 >= curr_time && !taken2)
      {
        if(state)
        {
          dispense2(amount2*rotation);
//            digitalWrite(8, HIGH);
            Serial.println("hello");
//            delay(500);
//            digitalWrite(8, LOW);
            
          time_taken2 = curr_time;
          taken2 = true;
        }
      }
      else
      {
        if (start_time2 > curr_time)
        {
          taken2 = false;
        }
      }
      if (digitalRead(slot1) == HIGH)
      {
        slot.write(50);
        
      }
      else if (digitalRead(slot2) == HIGH)
      {
        slot.write(170);
      }
  }
  Serial.println(state);
  Serial.println(digitalRead(slot1));
  Serial.println(digitalRead(slot2));

}
