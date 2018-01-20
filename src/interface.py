from pylsl import StreamInlet, resolve_stream

def init_lsl(stream_type, stream_index):
    print("looking for an EEG stream...")
    streams = resolve_stream('type', stream_type)

    # create a new inlet to read from the stream
    inlet = StreamInlet(streams[stream_index])
    return inlet

def read_lsl(inlet):
    sample, timestamp = inlet.pull_sample()
    return timestamp, sample

def classify_buf(buf):
    ssvep_result, mimg_result = 1, 0
    return ssvep_result, mimg_result 
