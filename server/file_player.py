import pyaudio
import wave

class Player:
    i = 0
    def play_music(self, filename):
        chunk = 1024

        #open a wav format music
        print("\n\n\n\n",filename)
        f = wave.open(filename,"rb")
        #instantiate PyAudio
        p = pyaudio.PyAudio()
        #open stream
        stream = p.open(format = p.get_format_from_width(f.getsampwidth()),
                        channels = f.getnchannels(),
                        rate = f.getframerate(),
                        output = True)
        #read data
        time_sample_diff = int(round((f.getframerate()/60)))
        data = f.readframes(time_sample_diff)

        #play stream
        while data:
            Player.i += 1
            stream.write(data)
            data = f.readframes(time_sample_diff)

        #stop stream
        stream.stop_stream()
        stream.close()

        #close PyAudio
        p.terminate()

    # def main():
    #     play_music("./test_files/test_marley.wav")
    #
    # if __name__ == "__main__":
    #     main()
