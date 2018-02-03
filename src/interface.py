import libmushu
import wyrm

def init_mushu_amp(index):
    """init_lsl() - initialize an LSL stream containing EEG data
    @stream_type:  Should be "EEG" for EEG data.
    @stream_index: LSL supports multiple concurrent streams, this selects one.

    Returns: A stream inlet that can be read from.
    """
    print("looking for an EEG stream...")
    available_amps = libmushu.get_available_amps()
    ampname        = available_amps[index]
    amp            = libmushu.get_amp(ampname)
    amp.configure()
    return amp

def read_mushu_amp(amp, amp_freq, amp_channels):
    """
    read_lsl() - reads a single sample from the LSL stream
    @inlet: The inlet from which to read the sample.

    Returns: A tuple with the timestamp integer, and sample (multiple variables in list form)
    """
    data, trigger = amp.get_data()
    wyrm_data     = wyrm.io.convert_mushu_data(data, trigger, amp_freq, amp_channels)
    return wyrm_data

def process_wyrm_data(data, csp_filter = None):
    dat = data.copy()
    fs_n = dat.fs / 2
    
    b, a = proc.signal.butter(5, [13 / fs_n], btype='low')
    dat = proc.filtfilt(dat, b, a)
    
    b, a = proc.signal.butter(5, [9 / fs_n], btype='high')
    dat = proc.filtfilt(dat, b, a)
    
    dat = proc.subsample(dat, 50)

    if filt is None:
        filt, pattern, _ = proc.calculate_csp(dat)
        plot_csp_pattern(pattern)
    dat = proc.apply_csp(dat, filt)
    
    dat = proc.variance(dat)
    dat = proc.logarithm(dat)
    return dat, filt

def train_classifier(training_data):
    pass

def classify_buf(buf, classifier):
    """
    classify_buf() - Takes the sample buffer, does EEG classification to determine game action.
    buf - The buffer containing relevant  EEG stream samples.

    Returns: ssvep_result controls game rotation and is 0/1/2 for left/none/right,
             mimg_result controls firing and is 0/1 for fire/don't fire
    """
    ssvep_result, mimg_result = 1, 0
    return ssvep_result, mimg_result

def gen_filter_vars(lowfreq, highfreq, fn, channels):
    b_low, a_low   = wyrm.processing.signal.butter(5, [highfreq / fn], btype='low')
    b_high, a_high = wyrm.processing.signal.butter(5, [lowfreq / fn], btype='high')
    zi_low         = wyrm.processing.lfilter_zi(b_low, a_low, channels)
    zi_high        = wyrm.processing.lfilter_zi(b_high, a_high, channels)
    return zi_low, zi_high
