"""Setup initial categories and sample products."""
from decimal import Decimal
from django.core.management.base import BaseCommand
from django.contrib.auth import get_user_model
from shop.models import Category, Product

User = get_user_model()


class Command(BaseCommand):
    help = "Add initial categories and sample products"

    def handle(self, *args, **options):
        categories_data = [
            ("arduino", "Arduino", "Arduino boards and shields"),
            ("esp", "ESP", "ESP32, ESP8266 microcontrollers"),
            ("raspberry-pi", "Raspberry Pi", "Raspberry Pi boards and accessories"),
            ("sensors", "Sensors", "Temperature, humidity, motion, ultrasonic sensors"),
            ("actuators", "Actuators", "Servos, stepper motors, relays"),
            ("motors", "Motors", "DC motors, stepper motors"),
            ("modules", "Modules", "Arduino modules, shields, drivers"),
        ]
        for slug, name, desc in categories_data:
            cat, _ = Category.objects.get_or_create(slug=slug, defaults={"name": name, "description": desc})
            self.stdout.write(f"Category: {cat.name}")

        seller = User.objects.filter(role="seller").first()
        if not seller:
            seller = User.objects.create_user("seller", "seller@roboshop.com", "seller123", role="seller")

        products_data = [
            # Arduino boards
            ("arduino", "arduino-uno-r3", "Arduino Uno R3", "Classic Arduino Uno board, ATmega328P, 14 digital I/O, 6 analog inputs.", Decimal("24.99"), 50),
            ("arduino", "arduino-nano", "Arduino Nano", "Compact Arduino Nano, ATmega328, USB interface, breadboard friendly.", Decimal("18.99"), 60),
            ("arduino", "arduino-mega-2560", "Arduino Mega 2560", "Arduino Mega 2560, ATmega2560, 54 digital I/O, 16 analog inputs.", Decimal("45.99"), 30),
            ("arduino", "arduino-due", "Arduino Due", "Arduino Due, ARM Cortex-M3 32-bit, 84 MHz, 3.3V logic.", Decimal("42.99"), 25),
            ("arduino", "arduino-leonardo", "Arduino Leonardo", "Arduino Leonardo with native USB, ATmega32u4.", Decimal("22.99"), 40),
            ("arduino", "arduino-pro-mini", "Arduino Pro Mini", "Arduino Pro Mini 5V 16MHz, compact bare board.", Decimal("9.99"), 80),
            # ESP boards
            ("esp", "esp32-devkit", "ESP32 DevKit V1", "ESP32-WROOM-32, dual-core 240MHz, WiFi + Bluetooth, 36 GPIO.", Decimal("12.99"), 100),
            ("esp", "esp8266-nodemcu", "ESP8266 NodeMCU", "NodeMCU ESP-12E, WiFi 802.11 b/g/n, Lua programmable.", Decimal("8.99"), 120),
            ("esp", "esp32-cam", "ESP32-CAM", "ESP32 with OV2640 camera module, WiFi, microSD slot.", Decimal("15.99"), 50),
            ("esp", "esp8266-d1-mini", "ESP8266 D1 Mini", "Wemos D1 Mini, compact ESP8266, WiFi enabled.", Decimal("6.99"), 90),
            # Raspberry Pi
            ("raspberry-pi", "raspberry-pi-pico", "Raspberry Pi Pico", "RP2040 dual-core ARM Cortex-M0+, 264KB SRAM, MicroPython/C.", Decimal("4.99"), 150),
            ("raspberry-pi", "raspberry-pi-pico-w", "Raspberry Pi Pico W", "Pico W with 2.4GHz WiFi, RP2040, wireless projects.", Decimal("6.99"), 100),
            ("raspberry-pi", "raspberry-pi-3-model-b", "Raspberry Pi 3 Model B+", "Quad-core 64-bit, 1GB RAM, WiFi, Bluetooth.", Decimal("35.99"), 40),
            ("raspberry-pi", "raspberry-pi-4-2gb", "Raspberry Pi 4 Model B 2GB", "Quad-core ARM Cortex-A72, 2GB RAM, dual HDMI.", Decimal("45.99"), 35),
            ("raspberry-pi", "raspberry-pi-4-4gb", "Raspberry Pi 4 Model B 4GB", "Quad-core 1.5GHz, 4GB RAM, USB 3.0, Gigabit Ethernet.", Decimal("55.99"), 30),
            ("raspberry-pi", "raspberry-pi-5", "Raspberry Pi 5", "Quad-core ARM Cortex-A76 2.4GHz, 4GB/8GB RAM, PCIe 2.0.", Decimal("79.99"), 20),
            # Sensors
            ("sensors", "hc-sr04-ultrasonic", "HC-SR04 Ultrasonic Sensor", "Ultrasonic distance sensor, 2cm-400cm range, 3-5V.", Decimal("4.99"), 100),
            ("sensors", "dht22-temperature-humidity", "DHT22 Temperature Humidity Sensor", "Digital temp & humidity, 0-100% RH, -40 to 80°C.", Decimal("8.99"), 80),
            ("sensors", "dht11-sensor", "DHT11 Temperature Humidity", "Basic DHT11, 20-80% RH, 0-50°C, digital output.", Decimal("3.99"), 100),
            ("sensors", "pir-motion-sensor", "PIR Motion Sensor HC-SR501", "Passive infrared motion detector, 3-5m range.", Decimal("3.49"), 120),
            ("sensors", "ldr-photoresistor", "LDR Photoresistor 5mm", "Light dependent resistor, pack of 10.", Decimal("2.99"), 200),
            ("sensors", "mq2-gas-sensor", "MQ-2 Gas Sensor Module", "Smoke, LPG, alcohol, hydrogen detector.", Decimal("5.99"), 60),
            ("sensors", "bmp280-pressure", "BMP280 Barometric Pressure Sensor", "I2C/SPI, temperature and pressure sensor.", Decimal("6.99"), 70),
            ("sensors", "mpu6050-accelerometer", "MPU6050 6-Axis Accelerometer Gyroscope", "3-axis gyro + 3-axis accelerometer, I2C.", Decimal("4.99"), 90),
            ("sensors", "hc-sr501-pir", "HC-SR501 PIR Motion Sensor", "Adjustable delay and sensitivity, 3-7m detection.", Decimal("2.99"), 150),
            ("sensors", "ultrasonic-sensor-jsn-sr04t", "JSN-SR04T Waterproof Ultrasonic", "Waterproof ultrasonic sensor, 25cm-450cm.", Decimal("7.99"), 50),
            # Actuators
            ("actuators", "sg90-servo-motor", "SG90 Micro Servo Motor", "9g micro servo, 1.8kg/cm torque, 180° rotation.", Decimal("3.99"), 80),
            ("actuators", "mg995-servo", "MG995 Metal Gear Servo", "Metal gear servo, 10kg/cm, waterproof.", Decimal("12.99"), 40),
            ("actuators", "relay-module-5v", "5V 4-Channel Relay Module", "4-channel relay, 10A 250V AC, optocoupler isolated.", Decimal("6.99"), 70),
            ("actuators", "relay-module-1ch", "1-Channel 5V Relay Module", "Single relay, 10A 250V AC, low level trigger.", Decimal("2.99"), 100),
            ("actuators", "stepper-motor-28byj48", "28BYJ-48 Stepper Motor + ULN2003", "5V stepper motor with driver board, 512 steps.", Decimal("4.99"), 60),
            ("actuators", "solenoid-valve-12v", "12V Solenoid Valve", "Brass solenoid valve, 1/2 inch, DC 12V.", Decimal("9.99"), 30),
            # Motors
            ("motors", "dc-motor-tt", "TT DC Gear Motor", "TT motor with wheels, 1:48 gear ratio, dual shaft.", Decimal("4.99"), 80),
            ("motors", "l298n-motor-driver", "L298N Motor Driver Module", "Dual H-bridge, 2A per channel, 5-35V.", Decimal("5.99"), 70),
            ("motors", "l293d-motor-driver", "L293D Motor Driver IC", "Quad half-H driver, 600mA per channel.", Decimal("2.49"), 100),
            ("motors", "dc-motor-130", "130 DC Motor", "130 size DC motor, 3-6V, 10000 RPM.", Decimal("2.99"), 150),
            ("motors", "n20-micro-gear-motor", "N20 Micro Gear Motor", "Encoder optional, 6V 200RPM, compact.", Decimal("4.49"), 90),
            # Modules
            ("modules", "lcd-16x2-i2c", "16x2 LCD Display I2C", "HD44780 LCD with I2C backpack, blue backlight.", Decimal("6.99"), 60),
            ("modules", "lcd-20x4-i2c", "20x4 LCD Display I2C", "20x4 character LCD with I2C interface.", Decimal("9.99"), 40),
            ("modules", "oled-128x64-ssd1306", "OLED 128x64 SSD1306", "I2C OLED display, 0.96 inch, white/blue.", Decimal("7.99"), 70),
            ("modules", "bluetooth-hc05", "HC-05 Bluetooth Module", "Bluetooth 2.0 serial, master/slave configurable.", Decimal("8.99"), 50),
            ("modules", "bluetooth-hc06", "HC-06 Bluetooth Module", "Bluetooth slave module, simple serial.", Decimal("5.99"), 60),
            ("modules", "rfid-rc522", "RFID-RC522 Module", "13.56MHz RFID reader, SPI interface.", Decimal("5.99"), 55),
            ("modules", "neopixel-strip-ws2812b", "WS2812B LED Strip", "Addressable RGB LED strip, 30/60 LEDs per meter.", Decimal("12.99"), 40),
            ("modules", "buzzer-active", "Active Buzzer 5V", "5V active buzzer, pack of 10.", Decimal("2.99"), 100),
            ("modules", "breadboard-830", "Breadboard 830 Points", "Solderless breadboard, 830 tie points.", Decimal("4.99"), 80),
            ("modules", "jumper-wires-mm", "Jumper Wires M-M 40pcs", "40pcs male-to-male jumper wires, 20cm.", Decimal("2.99"), 150),
            ("modules", "jumper-wires-ff", "Jumper Wires F-F 40pcs", "40pcs female-to-female jumper wires.", Decimal("2.99"), 150),
            ("modules", "resistor-kit", "Resistor Kit 1/4W", "Assorted resistor kit, 1 ohm - 1M ohm.", Decimal("9.99"), 50),
            ("modules", "capacitor-kit", "Electrolytic Capacitor Kit", "Assorted capacitor kit, various values.", Decimal("8.99"), 45),
            ("modules", "led-kit", "LED Kit Assorted", "5mm LED assorted colors, 100pcs.", Decimal("4.99"), 60),
            ("modules", "push-button-switch", "Tactile Push Button 6x6mm", "Momentary push button, pack of 50.", Decimal("3.99"), 100),
        ]

        created = 0
        for cat_slug, prod_slug, name, desc, price, stock in products_data:
            cat = Category.objects.get(slug=cat_slug)
            _, was_created = Product.objects.get_or_create(
                slug=prod_slug,
                defaults={
                    "name": name,
                    "category": cat,
                    "description": desc,
                    "price": price,
                    "stock": stock,
                    "seller": seller,
                },
            )
            if was_created:
                created += 1

        self.stdout.write(self.style.SUCCESS(f"Created {created} new products. Total products: {Product.objects.count()}"))
