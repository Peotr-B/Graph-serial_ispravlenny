//Создан специально для исправленного скрипта Graph-serial.py!

void setup() {
Serial.begin(9600);

}

void loop() 
{
//for (int j = 0; j<360; j++)
for (int j = 0; j<360; j += 2)  //для подгонки частоты
{
  Serial.println(1000*sin(j * (PI / 180)));
//  Serial.print(" ");
//  Serial.println(1000*sin((j+180) * (PI / 180)));
delay(1);
}
}
