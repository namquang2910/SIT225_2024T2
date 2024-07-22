#define LED_BUILTIN 13
int blink_times;
int randomNumber;


void setup() {
  Serial.begin(9600);  // set baud rate
  pinMode(LED_BUILTIN, OUTPUT);
}

void loop() {
  blink_times = Serial.parseInt();

  for(int i = 0; i < blink_times; i++)
  {
    digitalWrite(LED_BUILTIN, HIGH);  // turn the LED on (HIGH is the voltage level)
    delay(500);                      // wait for a second
    digitalWrite(LED_BUILTIN, LOW);   // turn the LED off by making the voltage LOW
    delay(500);                      // wait for a second
  }
  randomNumber = random(1,10);
  Serial.println(randomNumber);  
  Serial.flush();
}