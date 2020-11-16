import audioread


class AudioFile:

    def __init__(self):

        self.fileopen = False

    def set_file(self, fname):

        r = 0

        # Close old file
        if self.fileopen:
            self.fileopen = False
            self.handle.close()

        print("Stream redirect %s" % fname)

        try:
            self.handle = audioread.audio_open(fname)
            # print("Samplerate %d" % self.handle.samplerate)
            # print("Channels   %d" % self.handle.channels)
            # print("Duration   %d" % self.handle.duration)
            # r = self.handle._file.getnframes()
            self.fileopen = True

        except:
            print("Cant open file")
            return 0

        return r

    def read1k(self) -> []:

        # File end ?
        if not self.fileopen:
            return []

        srclen  = 1024*4
        srcdat  = []
        try:
            for frame in self.handle:
                srcdat = frame
                break
        except Exception as exc:
            print(__file__, exc)

        if srcdat.__len__() < srclen:
            return []

        r = [0] * 1024  # result
        for i in range(1024):
            n = 4
            left1  = (128 + int(srcdat[(i*n) + 0 + 1]))  & 0xFF
            r[i] = int(left1)

        return r

