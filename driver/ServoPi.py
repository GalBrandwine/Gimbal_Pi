import math

from driver.Raspi_PWM_Servo_Driver import PWM


class Servo(object):
    """
    Servo class for controlling RC servos with the Servo PWM Pi Zero
    """
    __pwm = None
    __position = [0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0]
    __lowpos = [0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0]
    __highpos = [0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0]
    __useoffset = False
    __offset = [0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0]
    __frequency = 50

    # local methods

    def __refresh_channels(self):
        for i in range(0, 16):
            if self.__position == 0:
                self.__pwm.set_pwm(i + 1, 0, 0)
            else:
                if self.__useoffset is True:
                    self.__pwm.set_pwm(i + 1, self.__offset[i],
                                       self.__position[i] + self.__offset[i])
                else:
                    self.__pwm.set_pwm(i + 1, 0, self.__position[i])

    def __calculate_offsets(self):
        """
        Calculate the start positions to stagger the servo position pulses
        """
        x = 0
        for i in range(0, 16):
            x = x + self.__highpos[i]
            if x > 4095 - self.__highpos[i]:
                x = self.__highpos[0] / 2
            self.__offset[i] = x
        self.__refresh_channels()

    # public methods

    def __init__(self, address=0x40, low_limit=1.0,
                 high_limit=2.0, reset=True):
        """
        init object with i2c address, default is 0x40 for ServoPi board
        """

        self.__pwm = PWM(address)
        self.set_low_limit(low_limit)
        self.set_high_limit(high_limit)

        if reset is True:
            self.set_frequency(50)
            self.__calculate_offsets()  # reset the offset values
        else:
            # get the on and off times from the pwm controller
            for i in range(0, 16):
                self.__offset[i] = self.__pwm.get_pwm_on_time(i + 1)
                self.__position[i] = self.__pwm.get_pwm_off_time(i + 1) - self.__offset[i]

    def move(self, channel, position, steps=250):
        """
        set the position of the servo
        """
        if channel < 1 or channel > 16:
            raise ValueError('for channel: {} move: channel out of range'.format(channel))

        if steps < 0 or steps > 4095:
            raise ValueError('move: steps out of range')

        if position >= 0 and position <= steps:
            high = float(self.__highpos[channel - 1])
            low = float(self.__lowpos[channel - 1])

            pwm_value = int((((high - low) / float(steps)) *
                             float(position)) + low)

            self.__position[channel - 1] = pwm_value

            if self.__useoffset:
                self.__pwm.set_pwm(channel, self.__offset[channel - 1],
                                   pwm_value + self.__offset[channel - 1])

            else:
                self.__pwm.set_pwm(channel, 0, pwm_value)
        else:
            raise ValueError('position: out of range'.format(position))

    def get_position(self, channel, steps=250):
        """
        get the position of the servo
        """
        if channel < 1 or channel > 16:
            raise ValueError('get_position: channel out of range')

        pwm_value = float(self.__pwm.get_pwm_off_time(channel))

        if self.__useoffset:
            pwm_value = pwm_value - self.__offset[channel - 1]

        steps = float(steps)
        high = float(self.__highpos[channel - 1])
        low = float(self.__lowpos[channel - 1])

        position = int(math.ceil((steps * (pwm_value - low)) / (high - low)))

        return position

    def set_low_limit(self, low_limit, channel=0):
        """
        Set the low limit in milliseconds
        """

        if channel < 0 or channel > 16:
            raise ValueError('set_low_limit: channel out of range')

        lowpos = int(4096.0 * (low_limit / 1000.0) * self.__frequency)

        if (lowpos < 0) or (lowpos > 4095):
            raise ValueError('set_low_limit: low limit out of range')

        if channel >= 1 and channel <= 16:
            # update the specified channel
            self.__lowpos[channel - 1] = lowpos
        else:
            # no channel specified so update all channels
            for i in range(16):
                self.__lowpos[i] = lowpos

    def set_high_limit(self, high_limit, channel=0):
        """
        Set the high limit in milliseconds
        """

        if channel < 0 or channel > 16:
            raise ValueError('set_high_limit: channel out of range')

        highpos = int(4096.0 * (high_limit / 1000.0) * self.__frequency)

        if (highpos < 0) or (highpos > 4095):
            raise ValueError('set_high_limit: high limit out of range')

        if channel >= 1 and channel <= 16:
            # update the specified channel
            self.__highpos[channel - 1] = highpos
        else:
            # no channel specified so update all channels
            for i in range(16):
                self.__highpos[i] = highpos

    def set_frequency(self, freq, calibration=0):
        """
        Set the PWM frequency
        """
        self.__pwm.set_pwm_freq(freq, calibration)
        self.__frequency = freq

    def output_disable(self):
        """
        disable output via OE pin
        """
        try:
            self.__pwm.output_disable()
        except:
            raise IOError("Failed to write to GPIO pin")

    def output_enable(self):
        """
        enable output via OE pin
        """
        try:
            self.__pwm.output_enable()
            self.__calculate_offsets()  # update the offset values
        except:
            raise IOError("Failed to write to GPIO pin")

    def offset_enable(self):
        """
        enable pulse offsets.
        This will set servo pulses to be staggered across the channels
        to reduce surges in current draw
        """
        self.__useoffset = True
        self.__calculate_offsets()  # update the offset values

    def offset_disable(self):
        """
        enable pulse offsets.
        This will set servo pulses to be staggered across the channels
        to reduce surges in current draw
        """
        self.__useoffset = False
        self.__refresh_channels()  # refresh the channel locations

    def sleep(self):
        """
        Put the device into a sleep state
        """
        self.__pwm.sleep()

    def wake(self):
        """
        Wake the device from its sleep state
        """
        self.__pwm.wake()

    def is_sleeping(self):
        """
        Check the sleep status of the device
        """
        return self.__pwm.is_sleeping()
