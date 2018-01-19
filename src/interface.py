from pylsl import StreamInlet, resolve_stream

def init_lsl()
    print("looking for an EEG stream...")
    streams = resolve_stream('type', 'EEG')

    # create a new inlet to read from the stream
    inlet = StreamInlet(streams[0])
    return inlet

def read_lsl(inlet)
    sample, timestamp = inlet.pull_sample()
    return sample, timestamp
