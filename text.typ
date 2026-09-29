== general architecture

=== hardware
- arduino UNO
- temperature sensors
- vibration sensor
- LCD
- keyboard
- wifi

=== software
- fastAPI
- websockets
- sql (for the history)
- web technologies (front end)
  - css
  - html
  - js

=== how they play together:
- you install the module in the device to be monitored
- you enter a unique identifier for the device
- you connect to the wifi
- you connect to the server
- every known period of time, a sample containing the id and the measurements from the sensors is sent as a json to an endpoint e.g.: "localhost:[PORT]/device/[id]/sample"
