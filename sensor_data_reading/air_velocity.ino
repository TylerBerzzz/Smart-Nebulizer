#include <Wire.h>
#include <SparkFun_FS3000_Arduino_Library.h> //Click here to get the library: http://librarymanager/All#SparkFun_FS3000

FS3000 fs;

const int numReadings = 5;

int readings[numReadings];  // the readings from the analog input
int readIndex = 0;          // the index of the current reading
int total = 0;              // the running total
int average = 0;            // the average

void setup()
{
  Serial.begin(115200);
  Serial.println("Example 1 - Reading values from the FS3000");

  Wire.begin();

  if (fs.begin() == false) //Begin communication over I2C
  {
    Serial.println("The sensor did not respond. Please check wiring.");
    while(1); //Freeze
  }

  fs.setRange(AIRFLOW_RANGE_7_MPS);

  // initialize all the readings to 0:
  for (int thisReading = 0; thisReading < numReadings; thisReading++) {
    readings[thisReading] = 0;
  }

  Serial.println("Sensor is connected properly.");
}

void loop()
{
    // Serial.print("FS3000 Readings \tRaw: ");
    // Serial.println(fs.readRaw()); // note, this returns an int from 0-3686

    // Serial.print("\tm/s: ");
    // Serial.println(fs.readMetersPerSecond()); // note, this returns a float from 0-7.23 for the FS3000-1005, and 0-15 for the FS3000-1015

    total = total - readings[readIndex];
    // read from the sensor:
    readings[readIndex] = fs.readRaw();
    // add the reading to the total:
    total = total + readings[readIndex];
    // advance to the next position in the array:
    readIndex = readIndex + 1;

    // if we're at the end of the array...
    if (readIndex >= numReadings) {
      // ...wrap around to the beginning:
      readIndex = 0;
    }

    // calculate the average:
    average = total / numReadings;
    // send it to the computer as ASCII digits
    Serial.println(average);

    // Serial.print("\tmph: ");
    // Serial.println(fs.readMilesPerHour()); // note, this returns a float from 0-16.17 for the FS3000-1005, and 0-33.55 for the FS3000-1015 
    
    delay(125); // note, reponse time on the sensor is 125ms
}