import time
import busio
import digitalio
import board
import adafruit_mcp3xxx.mcp3008 as MCP
from adafruit_mcp3xxx.analog_in import AnalogIn
from PIL import Image, ImageDraw, ImageFont
import adafruit_mpl3115a2
import adafruit_ssd1306

WIDTH = 128
HEIGHT = 64
i2c = board.I2C()  # uses board.SCL and board.SDA
oled = adafruit_ssd1306.SSD1306_I2C(WIDTH, HEIGHT, i2c)
oled.fill(0)
oled.show()
image = Image.new("1", (oled.width, oled.height))
draw = ImageDraw.Draw(image)
font = ImageFont.load_default()

# Create the SPI bus
spi = busio.SPI(clock=board.SCK, MISO=board.MISO, MOSI=board.MOSI)

# Create the chip select (CS)
cs = digitalio.DigitalInOut(board.D25)

# Create the MCP3008 object
mcp = MCP.MCP3008(spi, cs)

# Create an analog input channel on pin 0 (MCP3008 channel 0)
chan0 = AnalogIn(mcp, MCP.P0)

def voltage_to_distance(voltage):
    """Convert sensor voltage to distance (in cm)."""
    if voltage > 0.1:  # Avoid division by very small values or negative voltage
        return 27.86 / (voltage - 0.1)
    else:
        return None  # Return None for invalid readings
while True:
    # Print the raw ADC value and the corresponding voltage
    voltage = chan0.voltage
    distance = voltage_to_distance(voltage)
    print('Sensor Voltage: {:.2f}V'.format(voltage))
    if distance is not None:
        print(f"Distance: {distance:.2f} cm")
    else:
        print("Distance: Out of range")
    # Delay before the next reading
    draw.text((0,HEIGHT/2), f"voltage: {voltage:.2f}V",font=font,fill=255)
    oled.image(image)
    oled.show()
    time.sleep(1)
    draw.rectangle((0, 0, WIDTH, HEIGHT), outline=0, fill=0)
    time.sleep(1)

