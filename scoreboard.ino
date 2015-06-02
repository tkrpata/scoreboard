#include <PololuLedStrip.h>

/*
Working decent, but not a good visual indicator - i.e. UX sucks
Also having to have a host machine on serial sucks (Wifi shield too expensive for this!)
Consider migrating this to RPi

*/

// Create an ledStrip object on pin 12.
PololuLedStrip<12> ledStrip;

// Create a buffer for holding 60 colors.  Takes 180 bytes.
#define LED_COUNT 10
//rgb_color colors[LED_COUNT];

rgb_color colors[3] = { (rgb_color){255,255,0}, (rgb_color){0,255,0}, (rgb_color){255,0,0} };
rgb_color strip[LED_COUNT];

void setup() {
  Serial.begin(115200);
  Serial.println("Ready");
  // blank it
  for(byte i = 0; i < LED_COUNT; i++) {
    strip[i] = rgb_color{0,0,0};
  }
  ledStrip.write(strip, LED_COUNT);
}

void loop() {
  if (Serial.available())
  {
    char c = Serial.peek();
    if (!(c >= '0' && c <= '9'))
    {
      Serial.read(); // Discard non-digit character
    }
    else
    {
      int score_delta = Serial.parseInt() / 10; // eventually get this from the web service   
      int color_index = 0;
      int lsb = 0;
      // blank it
        for(byte i = 0; i < LED_COUNT; i++) {
          strip[i] = rgb_color{0,0,0};
        }
      ledStrip.write(strip, LED_COUNT);
      while(color_index < sizeof(colors)/sizeof(rgb_color) && score_delta > 0) {

        
        Serial.println("Color index: ");
        Serial.println(color_index);
        lsb = score_delta % 10;
        Serial.println("LSB:");
        Serial.println(lsb);

        for(byte i = 0; i < LED_COUNT; i++) {
          if(i < score_delta) {
            strip[i] = colors[color_index];
          } else {
            strip[i] = rgb_color{0,0,0};
          }
        }

        Serial.println("Write strip");
        
        score_delta = score_delta / 10;
        Serial.println("score delta:");
        Serial.println(score_delta);
        color_index++;
      }
      ledStrip.write(strip, LED_COUNT);
    }
  }
}
