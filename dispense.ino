#include <Servo.h> //Includes libraries for wifi and servo
#include <ESP8266WiFi.h>
#include <ESP8266HTTPClient.h>

// Update HOST URL here
//Sets up wifi connection
#define HOST "fihhn.tech"          // Enter HOST URL without "http:// "  and "/" at the end of URL

#define WIFI_SSID "Frisch Secure"            // WIFI SSID here                                   
#define WIFI_PASSWORD "zaA692ekS7"         // WIFI password here

//Button button1(2);
//Button button2(3);
//Button dispense(4);

//Sets variables for times
int stimeMIN1;
int stimeHR1;
int stimeMIN2;
int stimeHR2;
int etimeMIN1;
int etimeHR1;
int etimeMIN2;
int etimeHR2;
int curr_timeMIN = 30;
int curr_timeHR = 16;
int amount1 = 1;
int time_taken1MIN;
int time_taken1HR;
int user_id = 21;
int amount2 = 1;
int time_taken2MIN;
int time_taken2HR;
int rotation = 512;
bool taken1 = false;
bool taken2 = false;
int state;
int timeget = 0;
int last_time = 600000;
int sendtaken1 = 0;
int sendtaken2 = 0;
String postData, valtaken, valtaken2;
//char * machine = "qwerty";

bool active = true;

int wait = 3;
Servo slot;

void dispense1(int steps)
{
  if (steps >= 0)
  {
    Serial.println("Welcome");
    //Turns motor to dispense pill
    steps = steps / 4;
    for (int i = 0; i < steps; i++)
    {
      digitalWrite(D5, HIGH);
      digitalWrite(D6, LOW);
      digitalWrite(D7, LOW);
      digitalWrite(D8, LOW);
      delay(wait);
      digitalWrite(D5, LOW);
      digitalWrite(D6, HIGH);
      digitalWrite(D7, LOW);
      digitalWrite(D8, LOW);
      delay(wait);
      digitalWrite(D5, LOW);
      digitalWrite(D6, LOW);
      digitalWrite(D7, HIGH);
      digitalWrite(D8, LOW);
      delay(wait);
      digitalWrite(D5, LOW);
      digitalWrite(D6, LOW);
      digitalWrite(D7, LOW);
      digitalWrite(D8, HIGH);
    }

  }
}

void dispense2(int steps)
{
  //Turns motor to dispense second pill
  Serial.println("Hello again");
  if (steps >= 0)
  {
    steps = steps / 4;
    for (int i = 0; i < steps; i++)
    {
      digitalWrite(D1, HIGH);
      digitalWrite(D2, LOW);
      digitalWrite(D3, LOW);
      digitalWrite(D4, LOW);
      delay(wait);
      digitalWrite(D1, LOW);
      digitalWrite(D2, HIGH);
      digitalWrite(D3, LOW);
      digitalWrite(D4, LOW);
      delay(wait);
      digitalWrite(D1, LOW);
      digitalWrite(D2, LOW);
      digitalWrite(D3, HIGH);
      digitalWrite(D4, LOW);
      delay(wait);
      digitalWrite(D1, LOW);
      digitalWrite(D2, LOW);
      digitalWrite(D3, LOW);
      digitalWrite(D4, HIGH);
    }

  }
}



void setup() {
  // put your setup code here, to run once:
  //  dispense.begin();
  //Sets up pins and wifi connection
  slot.attach(9);
  pinMode(D1, OUTPUT);
  pinMode(D2, OUTPUT);
  pinMode(D3, OUTPUT);
  pinMode(D4, OUTPUT);
  pinMode(D5, OUTPUT);
  pinMode(D6, OUTPUT);
  pinMode(D7, OUTPUT);
  pinMode(D8, OUTPUT);
  pinMode(9, INPUT);
  Serial.begin(115200);
  Serial.println("Communication Started \n\n");
  delay(1000);
  pinMode(LED_BUILTIN, OUTPUT);
  WiFi.mode(WIFI_STA);
  WiFi.begin(WIFI_SSID, WIFI_PASSWORD);                                     //try to connect with wifi
  Serial.print("Connecting to ");
  Serial.print(WIFI_SSID);
  while (WiFi.status() != WL_CONNECTED)
  { Serial.print(".");
    delay(500);
  }

  Serial.println();
  Serial.print("Connected to ");
  Serial.println(WIFI_SSID);
  Serial.print("IP Address is : ");
  Serial.println(WiFi.localIP());    //print local IP address

  delay(30);
}

void loop() {
  while (active) 
  {
    if (millis() - last_time >= 600000 || timeget == 0) //If this variable has not been changed or 10 minutes has passed
     {
       //Go to get_time
       Serial.println("Going to get times!");
       last_time = millis();
       get_time();
     }
    //      curr_time = get_time();
    //      state = dispense.pressed();
    Serial.println("Will it pass?");
    state = digitalRead(9);
    Serial.println("Guess it will.");
    Serial.println(digitalRead(9));
    delay(100);
    //      Serial.println(state);
    if (stimeHR1 <= curr_timeHR && etimeHR1 >= curr_timeHR && taken1 == false)
    {
      Serial.println("Begin");
      //The above if statement checks if the time set for when you can take your pills has been reached or exceeded
      if (stimeMIN1 <= curr_timeMIN && etimeMIN1 >= curr_timeMIN || stimeHR1 < curr_timeHR && etimeHR1 > curr_timeHR)
      {
        Serial.println("Another pass");
        //If the current time is after the set time but before the ending time
        if (state == HIGH) 
        {
          time_taken1MIN = curr_timeMIN; //Set time_taken to the current time for server
          time_taken1HR = curr_timeHR;
          taken1 = true;
          sendtaken1 = 1;
          HTTPClient http;    // http object of clas HTTPClient
          valtaken = String(sendtaken1);
          postData = "valtaken=" + valtaken;
          http.begin("http://fihhn.tech/dbwritetaken.php"); 
          http.addHeader("Content-Type", "application/x-www-form-urlencoded");    
          int httpCode = http.POST(postData);
          Serial.println(httpCode);
          String webpage = http.getString();
          Serial.println(webpage + "\n"); 
          http.end();
          Serial.println("HI"); //Print test message
          dispense1(amount1 * rotation); //Dispense from slot 1
          //            digitalWrite(8, HIGH);
          //            delay(500);
          //            digitalWrite(8, LOW);
        }
      }
    }
    else
    {
      if (stimeHR1 > curr_timeHR) //If the current time is before the alloted time
      {
        //Reset taken1
        Serial.println("sup");
        taken1 = false;
        sendtaken1 = 0;
        HTTPClient http;    // http object of clas HTTPClient
        valtaken = String(sendtaken1);
        postData = "valtaken=" + valtaken;
        http.begin("http://fihhn.tech/dbwritetaken.php"); 
        http.addHeader("Content-Type", "application/x-www-form-urlencoded");    
        int httpCode = http.POST(postData);
        Serial.println(httpCode);
        String webpage = http.getString();
        Serial.println(webpage + "\n"); 
        http.end();
      }
    }



    if (stimeHR2 <= curr_timeHR && etimeHR2 >= curr_timeHR && taken2 == false)
    {
      Serial.println("Come in");
      //The above if statement is checking if the current time is after or during the time alloted to take the pill in slot 2
      if (stimeMIN2 <= curr_timeMIN && etimeMIN2 >= curr_timeMIN || stimeHR2 < curr_timeHR && etimeHR2 > curr_timeHR)
      {
       Serial.println("Yo");
        if (state == HIGH) 
        {
          time_taken2MIN = curr_timeMIN; //Set time_taken2 (time you took the pill from slot 2) to the current time
          time_taken2HR = curr_timeHR;
          taken2 = true;
          sendtaken2 = 1;
          HTTPClient http;    // http object of clas HTTPClient
          valtaken2 = String(sendtaken2);
          postData = "valtaken2=" + valtaken2;
          http.begin("http://fihhn.tech/dbwritetaken2.php"); 
          http.addHeader("Content-Type", "application/x-www-form-urlencoded");    
          int httpCode = http.POST(postData);
          Serial.println(httpCode);
          String webpage = http.getString();
          Serial.println(webpage + "\n"); 
          http.end();
          Serial.println("hello"); //Print test message
          dispense2(amount2 * rotation); //Dispense from slot 2
          //            digitalWrite(8, HIGH);
          //            delay(500);
          //            digitalWrite(8, LOW);
        }
      }
    }
    else
    {
      if (stimeHR2 > curr_timeHR) //if the current time is before the alloted time to take the pill in slot 2
      {
        //Reset taken2
        Serial.println("hello");
        taken2 = false;
        sendtaken2 = 0;
        HTTPClient http;    // http object of clas HTTPClient
        valtaken2 = String(sendtaken2);
        postData = "valtaken2=" + valtaken2;
        http.begin("http://fihhn.tech/dbwritetaken2.php"); 
        http.addHeader("Content-Type", "application/x-www-form-urlencoded");    
        int httpCode = http.POST(postData);
        Serial.println(httpCode);
        String webpage = http.getString();
        Serial.println(webpage + "\n"); 
        http.end();
      }
    }
    //if (digitalRead(slot1) == HIGH)
    //{
      //slot.write(50);

    //}
    //else if (digitalRead(slot2) == HIGH)
    //{
      //slot.write(170);
    //}
  }
  Serial.println("Finish!");
  Serial.println(state); //Print status of state
}

void get_time()
{
  //This code is long, but all it is doing is requesting the times the user set to take their pills from the server and changing the varibles to match those times.
  HTTPClient http;    //Declare object of class HTTPClient
  http.begin("http://fihhn.tech/dbgetsmin.php");
  http.addHeader("Content-Type", "application/x-www-form-urlencoded");

  int httpCode = http.GET();   //Get the request
  String payload = http.getString();    //Get the response payload

  Serial.print("HTTP Status: ");
  Serial.println(httpCode);   //Print HTTP return code
  Serial.print("Result: ");
  Serial.println(payload); //Print result
  delay(50);
  stimeMIN1 = payload.toInt(); //Change result into an integer
  Serial.println(stimeMIN1);
  
  http.begin("http://fihhn.tech/dbgetshr.php");
  http.addHeader("Content-Type", "application/x-www-form-urlencoded");
  httpCode = http.GET();   //Get the request
  payload = http.getString();    //Get the response payload
  Serial.print("Result: ");
  Serial.println(payload);
  delay(50);
  stimeHR1 = payload.toInt();

  http.begin("http://fihhn.tech/dbgetemin.php");
  http.addHeader("Content-Type", "application/x-www-form-urlencoded");
  httpCode = http.GET();   //Get the request
  payload = http.getString();    //Get the response payload
  Serial.print("Result: ");
  Serial.println(payload);
  delay(50);
  etimeMIN1 = payload.toInt();

  http.begin("http://fihhn.tech/dbgetehr.php");
  http.addHeader("Content-Type", "application/x-www-form-urlencoded");
  httpCode = http.GET();   //Get the request
  payload = http.getString();    //Get the response payload
  Serial.print("Result: ");
  Serial.println(payload);
  delay(50);
  etimeHR1 = payload.toInt();

  http.begin("http://fihhn.tech/dbgetsmin2.php");
  http.addHeader("Content-Type", "application/x-www-form-urlencoded");
  httpCode = http.GET();   //Get the request
  payload = http.getString();    //Get the response payload
  Serial.print("Result: ");
  Serial.println(payload);
  delay(50);
  stimeMIN2 = payload.toInt();

  http.begin("http://fihhn.tech/dbgetshr2.php");
  http.addHeader("Content-Type", "application/x-www-form-urlencoded");
  httpCode = http.GET();   //Get the request
  payload = http.getString();    //Get the response payload
  Serial.print("Result: ");
  Serial.println(payload);
  delay(50);
  stimeHR2 = payload.toInt();

  http.begin("http://fihhn.tech/dbgetemin2.php");
  http.addHeader("Content-Type", "application/x-www-form-urlencoded");
  httpCode = http.GET();   //Get the request
  payload = http.getString();    //Get the response payload
  Serial.print("Result: ");
  Serial.println(payload);
  delay(50);
  etimeMIN2 = payload.toInt();

  http.begin("http://fihhn.tech/dbgetehr2.php");
  http.addHeader("Content-Type", "application/x-www-form-urlencoded");
  httpCode = http.GET();   //Get the request
  payload = http.getString();    //Get the response payload
  Serial.print("Result: ");
  Serial.println(payload);
  delay(50);
  etimeHR2 = payload.toInt();
  http.end();  //Close connection
  timeget++; //make timeget 1 so that it doesn't check for the times again
  loop();
}
