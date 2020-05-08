import re
from utilities.GeneralUtilities import IS_MACOS, IS_WIN
import os
from gtts import gTTS
from playsound import playsound


if IS_MACOS:
    from os import system
else:
    import pyttsx3

def create_voice(self, gtts_status, rate=120):
    """
    Checks that status of gtts engine, and calls the correct speech engine
    :param rate: Speech rate for the engine (if supported by the OS)
    """

    if gtts_status==True:
        return VoiceGTTS()

    else:
        if IS_MACOS:
            return VoiceMac()
        elif IS_WIN:
            return VoiceWin(rate)
        else:
            try:
                return VoiceLinux(rate)
            except OSError:
                return VoiceNotSupported()


def remove_ansi_escape_seq(text):
    """
    This method removes ANSI escape sequences (such as a colorama color
    code) from a string so that they aren't spoken.
    :param text: The text that may contain ANSI escape sequences.
    :return: The text with ANSI escape sequences removed.
    """
    if text:
        text = re.sub(r'''(\x9B|\x1B\[)[0-?]*[ -\/]*[@-~]''', '', text)
    return text


# class Voice:
#     """
#     ABOUT: This class is the Voice of Jarvis.
#         The methods included in this class
#         generate audio output of Jarvis while
#         interacting with the user.
#     DOCUMENTATION on pyttsx3:
#         https://pyttsx3.readthedocs.io/en/latest/
#     """

class VoiceGTTS():
    def text_to_speech(self,speech):
        speech = remove_ansi_escape_seq(speech)
        tts = gTTS(speech, lang="en")
        tts.save("voice.mp3")
        playsound("voice.mp3")
        os.remove("voice.mp3")

class VoiceMac():
    def text_to_speech(self, speech):
        speech = remove_ansi_escape_seq(speech)
        speech = speech.replace("'", "\\'")
        system('say $\'{}\''.format(speech))


class VoiceLinux():
    def __init__(self, rate):
        """
        This constructor creates a pyttsx3 object.
        """
        self.rate = rate
        self.min_rate = 50
        self.max_rate = 500
        self.create()

    def create(self):
        """
        This method creates a pyttsx3 object.
        :return: Nothing to return.
        """
        self.engine = pyttsx3.init()
        self.engine.setProperty('rate', self.rate)

    def destroy(self):
        """
        This method destroys a pyttsx3 object in order
        to create a new one in the next interaction.
        :return: Nothing to return.
        """
        del self.engine

    def text_to_speech(self, speech):
        """
        This method converts a text to speech.
        :param speech: The text we want Jarvis to generate as audio
        :return: Nothing to return.
        A bug in pyttsx3 causes segfault if speech is '', so used 'if' to avoid that.
        Instability in the pyttsx3 engine can cause problems if the engine is
        not created and destroyed every time it is used.
        """
        if speech != '':
            speech = remove_ansi_escape_seq(speech)
            self.create()
            self.engine.say(speech)
            self.engine.runAndWait()
            self.destroy()

    def change_rate(self, delta):
        """
        This method changes the speech rate which is used to set the speech
        engine rate. Restrict the rate to a usable range.
        :param delta: The amount to modify the rate from the current rate.
        Note: The actual engine rate is set by create().
        """
        if self.rate + delta > self.max_rate:
            self.rate = self.max_rate
        elif self.rate + delta < self.min_rate:
            self.rate = self.min_rate
        else:
            self.rate = self.rate + delta


class VoiceWin():
    def __init__(self, rate):
        """
        This constructor creates a pyttsx3 object.
        """
        self.rate = rate
        self.min_rate = 50
        self.max_rate = 500
        self.create()

    def create(self):
        """
        This method creates a pyttsx3 object.
        :return: Nothing to return.
        """
        self.engine = pyttsx3.init()
        self.engine.setProperty('rate', 180)  # setting up new voice rate

    def destroy(self):
        """
        This method destroys a pyttsx3 object in order
        to create a new one in the next interaction.
        :return: Nothing to return.
        """
        del self.engine

    def text_to_speech(self, speech):
        """
        This method converts a text to speech.
        :param speech: The text we want Jarvis to generate as audio
        :return: Nothing to return.

        Instability in the pyttsx3 engine can cause problems if the engine is
        not created and destroyed every time it is used.
        """
        speech = remove_ansi_escape_seq(speech)
        self.create()
        voices = self.engine.getProperty('voices') #getting details of current voice
        self.engine.setProperty('voices', voices[1].id) #changing index, changes voices. 1 for female
        self.engine.say(speech)
        self.engine.runAndWait()
        self.destroy()

    def change_rate(self, delta):
        """
        This method changes the speech rate which is used to set the speech
        engine rate. Restrict the rate to a usable range.
        :param delta: The amount to modify the rate from the current rate.

        Note: The actual engine rate is set by create().
        """
        if self.rate + delta > self.max_rate:
            self.rate = self.max_rate
        elif self.rate + delta < self.min_rate:
            self.rate = self.min_rate
        else:
            self.rate = self.rate + delta



class VoiceNotSupported():
    def __init__(self):
        self.warning_print = False

    def text_to_speech(self, speech):
        if not self.warning_print:
            print(
                "Speech not supported! Please install pyttsx3 text-to-speech engine (sapi5, nsss or espeak)")
            self.warning_print = True
