from pylsl import StreamInlet, resolve_stream

def init_lsl(stream_type, stream_index):
    """init_lsl() - initialize an LSL stream containing EEG data
    @stream_type:  Should be "EEG" for EEG data.
    @stream_index: LSL supports multiple concurrent streams, this selects one.

    Returns: A stream inlet that can be read from.
    """
    print("looking for an EEG stream...")
    streams = resolve_stream('type', stream_type)

    inlet = StreamInlet(streams[stream_index])
    return inlet

def read_lsl(inlet):
    """
    read_lsl() - reads a single sample from the LSL stream
    @inlet: The inlet from which to read the sample.

    Returns: A tuple with the timestamp integer, and sample (multiple variables in list form)
    """
    sample, timestamp = inlet.pull_sample()
    return timestamp, sample

def classify_buf(buf):
    """
    classify_buf() - Takes the sample buffer, does EEG classification to determine game action.
    buf - The buffer containing relevant  EEG stream samples.

    Returns: ssvep_result controls game rotation and is 0/1/2 for left/none/right,
             mimg_result controls firing and is 0/1 for fire/don't fire
    """
    ssvep_result, mimg_result = 1, 0
    return ssvep_result, mimg_result 
