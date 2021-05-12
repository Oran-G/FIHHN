#include <Button.h>

//Button button1(2);
//Button button2(3);
Button dispense(4);

int start_time1 = 175;
int end_time1 = 320;
int curr_time = 300;
int amount1 = 2;
int time_taken1; 
int user_id = 21;
int start_time2 = 250;
int end_time2 = 450;
int amount2 = 1;
int time_taken2;

bool taken1 = false;
bool taken2 = false;
bool state;
//char * machine = "qwerty";

bool active = true;
void setup() {
  // put your setup code here, to run once:
  dispense.begin();
  pinMode(4, INPUT);
  pinMode(7, OUTPUT);
  pinMode(8, OUTPUT);
  Serial.begin(9600);

}

void loop() {
  while (active)
  {
//      get_data();
//      curr_time = get_time();
//      state = dispense.pressed();
      state = digitalRead(4);
      Serial.println(state);
      if (start_time1 <= curr_time && end_time1 >= curr_time && !taken1)
      {
        if(state)
        {
//          dispense1(amount1);
            digitalWrite(7, HIGH);
            delay(500);
            digitalWrite(7, LOW);
            Serial.println("HI");
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
//          dispense1(amount2);
            digitalWrite(8, HIGH);
            Serial.println("hello");
            delay(500);
            digitalWrite(8, LOW);
            
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
  }
  

}
