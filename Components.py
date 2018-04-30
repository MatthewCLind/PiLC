import time
import json
import requests

# http://python-omxplayer-wrapper.readthedocs.io/en/latest/
# pip install omxplayer-wrapper
import omxplayer
from omxplayer.player import OMXPlayer as OMX

# should come pre-installed on RPi
import pygame

# https://github.com/adafruit/Adafruit_Python_MCP3008
# sudo pip install adafruit-mcp3008
import Adafruit_MCP3008

# https://sourceforge.net/p/raspberry-gpio-python/wiki/Home/
# pip install RPi.GPIO
# I think only one instance of RPi.GPIO can be instantiated per machine
# so make sure you don't have another script running this if you get errors
try:
    import RPi.GPIO as gpio
except RuntimeError:
    print('Error importing RPi.GPIO!  ' +
          'This is probably because you need superuser privileges.' +
          'You can achieve this by using \'sudo\' to run your script')


class Component(object):
    """
    Base class for components
    """

    COMPONENT_TYPE = 'COMPONENT'

    def __init__(self, label, initial_value):
        """
        :param label: User-defined identifier, basically the Component's name
        :type label: str
        :param initial_value: Configuration data (such as which gpio pin to use, or initial time on the clock)
        """
        self.LABEL = label

        # INITIAL_VALUE saves the configuration data so that it can be saved later
        self.INITIAL_VALUE = initial_value
        self.value = initial_value

        # Methods which can be called when an Event is evaluated
        # the keys are used to map web-app created Events to Component methods
        self.effect_methods = \
        {
            'set_value': self.set_value
        }
        self.condition_methods = \
        {
            'equal_to': self.equal_to
        }

    def __str__(self):
        return str(self.COMPONENT_TYPE) + ' | ' + str(self.get_label()) + ' | ' + str(self.get_value())

    def __repr__(self):
        return 'repr of ' + self.COMPONENT_TYPE

    def get_value(self):
        self.update()
        return self.value

    def get_label(self):
        return self.LABEL

    def get_type(self):
        return self.COMPONENT_TYPE

    def get_definition(self):
        """
        Creates an dict that is formatted for saving the Component's information to files
        :return: str, dict{str: str, str: object}
        """
        return self.COMPONENT_TYPE, {"LABEL": self.get_label(), "VALUE": self.INITIAL_VALUE}

    def get_display(self):
        """
        Formatted data for the live_feed file
        :return: str, dict{str, object}

        """
        label = self.get_label()
        value = self.get_value()
        return self.COMPONENT_TYPE, {label: value}

    def set_value(self, value):
        self.value = value

    def update(self):
        """
        many components need to be kept up-to-date in real time,
        rather than figuring out if a component needs updating,
        we'll just call update on everything and let it decide for itself
        """
        pass

    def equal_to(self, value):
        return self.value == value

    def evaluate_condition(self, method_name, value=None):
        """
        Returns true or false to give information about the state of this Component
        How an Event determines if a condition is met E.G. 30 minutes has elapsed on a Timer
        :param value: value to compare against, can be a string, float, or what have you
        :param method_name: method which compares value to internal data
        :rtype: bool
        """
        method = self.condition_methods[method_name]
        if value is not None:
            comparison = method(value)
        else:
            comparison = method()
        return comparison


class URIComponent(Component):
    """
    Class for reading and writing to files/urls
    """

    COMPONENT_TYPE = 'URI_COMPONENT'

    def __init__(self, label, uri):
        super(URIComponent, self).__init__(label, '')
        self.uri = uri
        self.condition_methods['key_in_value'] = self.key_in_value

    def key_in_value(self, keyword):
        """
        Looks for a keyword in the current value
        :param keyword: the keyword to look for
        :type keyword: str
        """
        return keyword in self.value


class WebGet(URIComponent):
    """
    Class that reads data from a URL
    Think of it like curl or wget
    """
    def __init__(self, label, url):
        super(WebGet, self).__init__(label, url)
        self.effect_methods['web_get'] = self.web_get

    def web_get(self):
        self.set_value(requests.get(self.uri))


class WebPost(URIComponent):
    """
    Class that posts data to a URL
    Think of it like curl or wget
    """
    def __init__(self, label, url):
        super(WebPost, self).__init__(label, url)

    def web_post(self, data):
        requests.post(self.uri, data)


class FileQueue(URIComponent):
    """
    Class for reading in commands or strings from a file
    Especially useful for receiving communications through the web

    Messages are separated by newlines
    First-in-first-out queue
    Oldest messages at top of file
    """

    COMPONENT_TYPE = 'FILE_QUEUE'

    def __init__(self, label, file_name):
        super(FileQueue, self).__init__(label, file_name)

    def update(self):
        """
        Reads the top line from the file.
        If the file is empty (or basically empty), hold on to the previous command
        """
        with open(self.uri, 'rw') as f:
            all_commands = f.read()
            if all_commands != '' or all_commands != '\n':
                command_list = all_commands.split('\n')
                self.set_value(command_list[0])
                f.write('\n'.join(command_list[1:]))


class NumericalComponent(Component):
    """
    Base class for Components which store a number value, like Timers and Counters
    """

    COMPONENT_TYPE = 'NUMERICAL_COMPONENT'

    def __init__(self, label, initial_value):
        super(NumericalComponent, self).__init__(label, initial_value)
        self.condition_methods['greater_than'] = self.greater_than
        self.condition_methods['less_than'] = self.less_than

    def greater_than(self, amount):
        """
        Mathematical greater than
        :param amount: value to compare against. Component's value > amount
        :return: value > amount
        :rtype: bool
        """
        return self.get_value() > amount

    def less_than(self, amount):
        """
        Mathematical less than
        :param amount: value to compare against. Component's value < amount
        :return: value < amount
        :rtype:bool
        """
        return self.get_value() < amount


class Counter(NumericalComponent):
    """
    Counters keep track of integer counts
    """

    COMPONENT_TYPE = 'COUNTER'

    def __init__(self, label, initial_value):
        initial_value = int(initial_value)
        super(Counter, self).__init__(label, initial_value)
        self.effect_methods['decrease_value'] = self.decrease_value
        self.effect_methods['increase_value'] = self.increase_value

    def decrease_value(self, amount):
        """
        Decreases this Counter's count by amount
        :param amount: amount to decrease count by
        :type amount: int
        """
        new_value = self.value - amount
        super(Counter, self).set_value(new_value)

    def increase_value(self, amount):
        """
        Increases this Counter's count by amount
        :param amount: amount to increase count by
        :type amount: int
        """
        new_value = amount + self.value
        super(Counter, self).set_value(new_value)


class Timer(NumericalComponent):
    """
    Component to keep track of times. State determines if the timer increases its value
    Stopping the timer sets its time to 0
    Pausing holds current time
    """

    COMPONENT_TYPE = 'TIMER'

    def __init__(self, label, initial_value):
        super(Timer, self).__init__(label, initial_value)
        self.state = 'PAUSED'
        self.start_time = 0.0
        self.effect_methods['set_state'] = self.set_state
        self.condition_methods['get_state'] = self.get_state

    def update(self):
        """
        Updates the value with the current relative time (relative to self.start_time)
        """
        if self.state == 'RUNNING':
            elapsed_time = time.time() - self.start_time
            super(Timer, self).set_value(elapsed_time)

    def get_value(self):
        """
        :rtype: float
        """
        # call update() first in order to report on the most accurate time
        self.update()
        return super(Timer, self).get_value()

    def set_state(self, state):
        """
        A Timer can be STOPPED, RUNNING, or PAUSED which influence its behavior
        :param state: "STOPPED", "RUNNING", or "PAUSED"
        """
        old_state = self.state
        self.state = state
        if old_state != 'STOPPED' and state == 'RUNNING':

            # clock just started, take time measurements relative to right now
            self.start_time = time.time()
        elif self.state == 'STOPPED':
            self.set_value(0)
        else:
            # self.state == paused, do nothing
            pass

    def set_value(self, value):
        """
        The value is what time you want to put on the clock.
        :param value: new time on the clock
        :type value: float
        """

        # cast to float so we don't end up with an int. This ain't no counter
        float(value)

        # adjust the starting time so subsequent times will be relative,
        # we don't want to set the value and have it go back to the way things were
        new_start_time = time.time() - value
        self.start_time = new_start_time
        super(Timer, self).set_value(value)

    def get_state(self):
        """
        States can be 'STOPPED', 'PAUSED', or 'RUNNING'
        :return: 'STOPPED', 'PAUSED', or 'RUNNING'
        :rtype: float
        """
        return self.state

    def equal_to(self, compare_time):
        """
        Returns whether the time on the clock is equal to compare_time.
        Rounded to nearest tenth of a second
        :param compare_time: Time you want to compare to
        :rtype: float
        """
        return round(self.value, 1) == round(compare_time, 1)


class AnalogInput(NumericalComponent):
    """
    Interface with onboard MCP3008 ADC over SPI
    """

    COMPONENT_TYPE = 'ANALOG_INPUT'

    # the Adafruit_MCP3008 instance needs to be shared among all AnalogInput components, hence class level
    mcp = Adafruit_MCP3008.MCP3008(clk=2, cs=3, miso=17, mosi=4)

    def __init__(self, label, channel):
        """
        :param channel: value between 0 and 3
        :type channel: int
        """
        super(AnalogInput, self).__init__(label, 0)
        if channel not in range(4):
            raise ValueError('Channel must be between 0 and 3')
        self.channel = channel

    def update(self):
        """
        10-bit precision value reported by the MCP3008
        """
        analog_value = AnalogInput.mcp.read_adc(self.channel)  # type: int
        self.set_value(analog_value)

    def set_value(self, value):
        # You can't dictate the value, the chip does
        pass

    def get_value(self):
        """
        Returns 10-bit precision int reported by MCP3008
        :return: 0 - 1023
        :rtype: int
        """
        self.update()
        return super(AnalogInput, self).get_value()


class GPIOBase(Component):
    """
    Base for GPIO classes, utilizes RPi.GPIO package
    """

    COMPONENT_TYPE = 'GPIO_BASE'

    def __init__(self, label, gpio_pin):
        """
        :param gpio_pin: Give a number, not the actual BCM value
        :type gpio_pin: int
        """
        gpio_pin = int(gpio_pin)
        super(GPIOBase, self).__init__(label, 'LOW')
        self.gpio_pin = gpio_pin
        self.INITIAL_VALUE = gpio_pin


class DigitalInput(GPIOBase):
    """
    Digital input representing opto-isolated input
    """

    COMPONENT_TYPE = 'DIGITAL_INPUT'

    # BCM numbering
    GPIO_PINS = [7, 8, 25, 24, 16, 18]

    def __init__(self, label, gpio_pin):
        super(DigitalInput, self).__init__(label, gpio_pin)
        self.channel = self.GPIO_PINS[gpio_pin]

        # pull_up_down=gpio.PUD_UP specifies to use the built-in pull up resistor
        # this means that a value of gpio.LOW corresponds with +12v across the input
        gpio.setup(self.channel, gpio.IN, pull_up_down=gpio.PUD_UP)

    def update(self):
        # gpio.LOW means +12v is applied across input

        pin_state = gpio.input(self.channel)
        new_val = ''

        # steady on
        if pin_state == gpio.LOW and (self.value == 'PRESSED' or self.value == 'HELD_DOWN'):
            new_val = 'HELD_DOWN'

        # analogous to rising edge
        elif pin_state == gpio.LOW and (self.value == 'RELEASED' or self.value == 'HELD_UP'):
            new_val = 'PRESSED'

        # analogous to falling edge
        elif pin_state == gpio.HIGH and (self.value == 'PRESSED' or self.value == 'HELD_DOWN'):
            new_val = 'RELEASED'

        # steady off
        elif pin_state == gpio.HIGH:
            new_val = 'HELD_UP'

        self.set_value(new_val)

    def set_value(self, value):
        # you don't get to dictate the value of the input
        pass

    def get_value(self):
        """
        :rtype: str
        """
        self.update()
        return super(DigitalInput, self).get_value()


class DigitalOutput(GPIOBase):
    """
    Component to control states of the Solid State Relays
    """

    COMPONENT_TYPE = 'DIGITAL_OUTPUT'

    # BCM pins
    GPIO_PINS = [26, 13, 19, 12, 6, 5, 11, 9, 10, 22]

    def __init__(self, label, gpio_pin):
        """
        :param gpio_pin: Provide 1 - 10 to correspond with the PCB
        :type gpio_pin: int
        """
        # take one off to convert from counting numbers to index
        gpio_pin -= 1
        super(DigitalOutput, self).__init__(label, gpio_pin)

        self.effect_methods['toggle'] = self.toggle_value
        self.channel = self.GPIO_PINS[gpio_pin]
        gpio.setup(self.channel, gpio.OUT, initial=gpio.LOW)

    def set_value(self, new_state):
        """
        Controls the state of the solid state relay
        :param new_state: 'HIGH' or 'LOW'
        :type new_state: str
        """
        super(DigitalOutput, self).set_value(new_state)
        if self.value == 'HIGH':
            gpio.output(self.channel, gpio.HIGH)
        elif self.value == 'LOW':
            gpio.output(self.channel, gpio.LOW)

    def toggle_value(self):
        """
        Flips the output. Convenient for blinking stuff
        :return: Tells you what state it ends up in
        :rtype: str
        """
        if self.value == 'HIGH':
            self.set_value('LOW')
        elif self.value == 'LOW':
            self.set_value('HIGH')

        return self.get_value()


class PWMOutput(GPIOBase):
    """
    Class for using software-defined PWM with the SSRs
    """

    COMPONENT_TYPE = 'PWM_OUTPUT'

    # BCM pins, same as DigitalOutput
    GPIO_PINS = [26, 13, 19, 12, 6, 5, 11, 9, 10, 22]

    def __init__(self, label, gpio_pin):
        """
        :param gpio_pin: Provide 1 - 10 to correspond with the PCB
        :type gpio_pin: int
        """
        # take one off to convert from counting numbers to index
        gpio_pin -= 1
        super(PWMOutput, self).__init__(label, gpio_pin)
        self.effect_methods['start'] = self.start
        self.effect_methods['stop'] = self.stop
        self.channel = self.GPIO_PINS[gpio_pin]
        gpio.setup(self.channel, gpio.OUT, initial=gpio.LOW)
        self.pwm_controller = gpio.PWM(self.channel, 200)
        self.set_value(0)

    def set_value(self, duty_cycle):
        """
        Changes the duty cycle of the PWM signal
        :param duty_cycle: new duty cycle expressed as percentage (1-100)
        :type duty_cycle: int
        """
        self.pwm_controller.ChangeDutyCycle(duty_cycle)

    def start(self, inital_dutycycle=0):
        """
        Starts the PWM signal
        Must be called before the output will function
        :param inital_dutycycle: sets the initial duty cycle when first started
        :type inital_dutycycle: int
        """
        self.pwm_controller.start(inital_dutycycle)

    def stop(self):
        """
        Stops the PWM signal
        Use set_value(0) for intermediate "off", and stop() to free up processor
        """
        self.pwm_controller.stop()


class MediaPlayer(Component):
    """
    Bass class for Media Playing objects
     MediaPlayer methods:
       Play() - starts playing track until track stops playing or,
                   does nothing if already playing
       Stop()      - stops playback of currently playing track
    """

    COMPONENT_TYPE = 'MEDIA_PLAYER'

    def __init__(self, label, track):
        """
        :param track: path to media file
        :type track: str
        """
        super(MediaPlayer, self).__init__(label, track)
        self.effect_methods['play'] = self.play
        self.effect_methods['stop'] = self.stop
        self.track = track

    def play(self):
        pass

    def stop(self):
        pass


class SimpleVideoPlayer(MediaPlayer):
    """
    Uses OMXPlayer to play videos through HDMI port
     - You can only have one OMXPlayer at any time, hence class level player
    """
    COMPONENT_TYPE = 'SIMPLE_VIDEO_PLAYER'
    player = None

    # Things misbehave when you try to issue too many commands too quickly, so these block that
    # Also, gotta keep this class level so all components play by the same rules
    # TODO eventually make it so that if you hit a timeout period, you come back and try again later
    time_out = 0
    TIME_PERIOD = 1

    def __init__(self, label, uri):
        """
        :param uri: Can be a path to local video or even some web-based video streams
        :type uri: str
        """
        super(SimpleVideoPlayer, self).__init__(label, uri)

    @staticmethod
    def start_timeout(block_time):
        """
        Starts the timeout clock
        :param block_time: how long to wait
        """
        SimpleVideoPlayer.time_out = time.time() + block_time

    @staticmethod
    def timeout_elapsed():
        """
        Check if OMXPlayer is ready for a new command
        :return: whether we are beyond the timeout period
        """
        return time.time() > SimpleVideoPlayer.time_out

    def play(self):
        """
        Starts playing video from the beginning, or does nothing if already playing
        """
        playing = False

        # Most of the errors are fine and we can ignore them
        try:
            playing = SimpleVideoPlayer.player.is_playing()
        except omxplayer.player.OMXPlayerDeadError as e:
            print('Exception type: ' + str(type(e)) + '\nMessage: ' + e.message)
        except AttributeError:
            pass
        except Exception as e:
            print('Unknown Error!!!')
            print('Exception type: ' + str(type(e)) + '\nMessage: ' + e.message)

        # Most of the errors are fine and we can ignore them
        try:
            if not playing and self.timeout_elapsed():

                # This creates a brand new player and automatically starts it
                SimpleVideoPlayer.player = OMX(self.track, ['-b', '--no-osd'])
                self.start_timeout(SimpleVideoPlayer.TIME_PERIOD)
        except omxplayer.player.OMXPlayerDeadError:
            pass
        except AttributeError:
            pass
        except Exception as e:
            print('Unknown Error!!!')
            print('Exception type: ' + str(type(e)) + '\nMessage: ' + e.message)
            raise

    def stop(self):
        """
        Stops playing the current video and conceptually sets the playback timer to 0 (not technically exactly true)
        """

        # Most of the errors are fine and we can ignore them
        try:
            if self.timeout_elapsed() and SimpleVideoPlayer.player.get_source() == self.track:
                SimpleVideoPlayer.player.stop()
                self.start_timeout(SimpleVideoPlayer.TIME_PERIOD)
        except omxplayer.player.OMXPlayerDeadError:
            pass
        except AttributeError:
            pass
        except Exception as e:
            print('Unknown Error!!!')
            print('Exception type: ' + str(type(e)) + '\nMessage: ' + e.message)
            raise


class SimpleAudioPlayer(MediaPlayer):
    """
    Audio player which utilizes pygame. Sounds play through HDMI
    """

    COMPONENT_TYPE = 'SIMPLE_AUDIO_PLAYER'

    # init() required for pygame to do its thing
    pygame.init()

    # share one player among all SimpleAudioPlayer instances
    player = None

    # only the component which started the audio can stop it prematurely. All components can start a new track, though
    initiator = ''

    # Things misbehave when you try to issue too many commands too quickly, so these block that
    # Also, gotta keep this class level so all components play by the same rules
    # TODO eventually make it so that if you hit a timeout period, you come back and try again later
    time_out = 0
    TIME_PERIOD = 0.5

    def __init__(self, label, path):
        """
        :param path: path to local audio file
        """
        super(SimpleAudioPlayer, self).__init__(label, path)
        if SimpleAudioPlayer.player is None:
            SimpleAudioPlayer.player = pygame.mixer.music

    @staticmethod
    def start_timeout(block_time):
        """
        Starts the timeout clock
        :param block_time: how long to wait
        """
        SimpleAudioPlayer.time_out = time.time() + block_time

    @staticmethod
    def timeout_elapsed():
        """
        Check if OMXPlayer is ready for a new command
        :return: whether we are beyond the timeout period
        """
        return time.time() > SimpleAudioPlayer.time_out

    def play(self):
        """
        Attempts to play this player's track
        """
        if self.timeout_elapsed():
            try:
                SimpleAudioPlayer.player.load(self.track)
                SimpleAudioPlayer.player.play()
                self.start_timeout(SimpleAudioPlayer.TIME_PERIOD)
                SimpleAudioPlayer.initiator = self.LABEL
            except Exception as e:
                print('could not play audio')
                print('Exception type: ' + str(type(e)) + '\nMessage: ' + e.message)
                raise

    def stop(self):
        """
        Stops play if and only if it was the one to start playing in the first place
        """
        try:
            if self.timeout_elapsed() and SimpleAudioPlayer.initiator == self.LABEL:
                SimpleAudioPlayer.player.stop()
                self.start_timeout(SimpleAudioPlayer.TIME_PERIOD)
        except Exception as e:
            print('could not stop audio')
            print('Exception type: ' + str(type(e)) + '\nMessage: ' + e.message)
            raise


def create_components(component_json_string='', components_dict=None):
    """
    Parses json strings into a list of components. Useful for receiving updates from web browser
    Either send component_json_string or components_dict, not both
    :param component_json_string: stringified representation of all components
    :param components_dict: already-loaded dict of components
    :return: list of parsed out components
    :rtype: list[Component]


    Example json:

    {
        "DIGITAL_INPUT":
        [
            {"LABEL":"din_1","VALUE":0}
        ],
        "ANALOG_INPUT":
        [
            {"LABEL":"anin_1", "VALUE":3},
            {"LABEL":"analog_2, "VALUE":2}
        ]
    }
    """

    # so I can avoid a huge long annoying "if" tree
    # you gotta add any new Component classes to this in order to make them
    # the Key must be COMPONENT_TYPE
    classes_dict = \
        {
            'TIMER': Timer,
            'COUNTER': Counter,
            'DIGITAL_INPUT': DigitalInput,
            'DIGITAL_OUTPUT': DigitalOutput,
            'ANALOG_INPUT': AnalogInput,
            'SIMPLE_AUDIO_PLAYER': SimpleAudioPlayer,
            'SIMPLE_VIDEO_PLAYER': SimpleVideoPlayer
        }

    components = []

    # parse the json string into a dict
    if components_dict is None and component_json_string != '':
        components_dict = json.loads(component_json_string)

    component_types = components_dict.keys()
    for comp_type in component_types:
        for entry in components_dict[comp_type]:
            label = entry['LABEL']
            value = entry['VALUE']
            new_comp = classes_dict[comp_type](label, value)
            components.append(new_comp)

    return components
