void setup() {
  // put your setup code here, to run once:
  Serial.begin(9600);
}

void loop() {
  // put your main code here, to run repeatedly:
  float ampA = analogRead(A0) * (5.0/1023.0) / 0.01;
  float ampB = analogRead(A1) * (5.0/1023.0) / 0.01;
  float ampC = analogRead(A2) * (5.0/1023.0) / 0.01;
  float temp = (analogRead(A3) * (500.0/1023.0)) - 50;

  Serial.print("A: ");
  Serial.print(ampA);
  Serial.print("A B: ");
  Serial.print(ampB);
  Serial.print("A C: ");
  Serial.print(ampC);
  Serial.print("A T: ");
  Serial.println(temp);
  
  delay(1000);
}
