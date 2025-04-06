#define ANALOG_PIN A0

void setup() {
    Serial.begin(115200);
}

void loop() {
    int value = analogRead(ANALOG_PIN);
    Serial.println(value);
    delayMicroseconds(1);
}
