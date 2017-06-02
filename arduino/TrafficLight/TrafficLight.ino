
//// Traffic Light ////

// delay time
int greenLight = 30000; // 30 sec 
int yellowLight = 3000; // 3 sec
int redLight = 10000; // 10 sec

// pin number
int greenPin = 3;
int yellowPin = 4;
int redPin = 5;

void setup() {
  pinMode(greenPin, OUTPUT);
  pinMode(yellowPin, OUTPUT);
  pinMode(redPin, OUTPUT); 
}

void loop() {
  // green light
  digitalWrite(yellowPin, 0); digitalWrite(redPin, 0); digitalWrite(greenPin, 1); 
  delay(greenLight);

  // yellow light
  digitalWrite(redPin, 0); digitalWrite(greenPin, 0); digitalWrite(yellowPin, 1);
  delay(yellowLight);

  // red light
  digitalWrite(greenPin, 0); digitalWrite(yellowPin, 0); digitalWrite(redPin, 1);
  delay(redLight);
}



