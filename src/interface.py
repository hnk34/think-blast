import pylsl
import numpy
from sklearn.discriminant_analysis import LinearDiscriminantAnalysis 

def init_lsl(stream_index):
    """init_lsl() - initialize an LSL stream containing EEG data
    @stream_index: LSL supports multiple concurrent streams, this selects one.

    Returns: A stream inlet that can be read from.
    """
    streams = pylsl.resolve_stream('type', 'EEG')
    inlet   = pylsl.StreamInlet(streams[stream_index])
    return inlet

def read_lsl(inlet):
    """
    read_lsl() - reads a single sample from the LSL stream
    @inlet: The inlet from which to read the sample.

    Returns: A tuple with the timestamp integer, and sample (multiple variables in list form)
    """
    sample, time = inlet.pull_sample()
    return time, sample

def csv_to_nparray(cal_file):
    """
    csv_to_nparray() - converts a csv calibration file to numpy array
    @cal_file: The full path of the calibration file.

    Returns: A tuple with the electrode data (x), and the trial data (y)
    """
    dat = numpy.genfromtxt(cal_file, delimiter=',')
    s = dat.shape
    end_col = s[1] - 1
    end_row = s[0] - 1
    dat = dat[:, 0:end_col] # Genfromtext adds a nan to the end of each line, this fixes it
    x = dat[0:end_row, 2:end_col]
    y = dat[0:end_row:301, 1]
    print y
    return x,y

def trial_to_feat(x):
    """
    trial_to_feat() - convert the data from a single calibration trial into a feature vector.
    @x: The raw electrode data for a single trial (should be 300 samples). 

    Returns: A feature vector, read to be appended then fed into the LDA trainer.
    """
    o1 = seq_to_bands(x[:, 0])
    o2 = seq_to_bands(x[:, 1])
    oz = seq_to_bands(x[:, 2])
    mean_8hz  = numpy.mean([o1[0], o2[0], o3[0]])
    mean_19hz = numpy.mean([o1[1], o2[1], o3[1]])
    feat = numpy.array([mean_8hz, mean_19hz])
    return feat

def seq_to_bands(x):
    """
    seq_to_amp() - convert a single electrode data sequence into 2 band powers
    @x: Raw electrode data for a single electrode.

    Returns: A numpy array containing the band power at 8 and 19 Hz.
    """
    amp_8hz  = seq_to_pwr(x, 7.5, 8.5)
    amp_19hz = seq_to_pwr(x, 18.5, 19.5)
    amps = numpy.array([amp_8hz, amp_19hz])
    return amps

def seq_to_pwr(x, lowfreq, hifreq):
    """
    seq_to_pwr() - convert a single electrode data sequence into a band power amplitude
    @x: Single electrode data.
    @lowfreq: Low cutoff frequency.
    @hifreq: High cutoff frequency.

    Returns: A single amplitude value. 
    """
    # TODO: adjust the start time of the fft to ensure SSVEP has been induced
    # Skip first 7 frames
    spec  = numpy.fft.fft(x)
    freqs = numpy.fft.fftfreq(x.size, 1/60)
    mask  = numpy.logical_and(freqs >= lowfreq, freqs <= hifreq)
    avg   = spec[mask].mean()
    return avg

def butter_filter(x):
    pass

def get_classifier(cal_file):
    """"
    get_classifier() - generate an SSVEP classifier using LDA, based on a calibration file
    @cal_file: The full path of the calibration file.

    Returns: Scikit classifier object.
    """
    x,y = csv_to_nparray(cal_file)
    feats = numpy.empty((20, 2))
    j = 0
    for i in range(0, len(y)):
        feats[i] =  trial_to_feat(x[j:j+300, :])
    clf = LinearDiscriminantAnalysis()
    clf.fit(feats,y)
    return clf

def voting_matrix(x):
    """
    voting_matrix() - Given multiple predicted LDA classifications, determine a final class.
    @x: The array of all predicted values.

    Returns: A single class value.
    """
    return np.round(np.mean(x))

def buf_to_feats(buf):
    """
    buf_to_feats(): Converts the raw electrode data buffer into a feature vector, in real-time.
    @buf: The electrode data.

    Returns: The feature vector.
    """
    pass # TODO

def classify_buf(lda_classifier, sample_buf):
    """
    classify_buf() - online function, takes the sample buffer, does EEG classification to determine game action
    buf - The buffer containing relevant  EEG stream samples.

    Returns: ssvep_result controls game rotation and is 0/1/2 for left/none/right,
             mimg_result controls firing and is 0/1 for fire/don't fire
    """
    feats = buf_to_feats(sample_buf)
    preds = clf.predict(feats)
    result = voting_matrix(preds)
    ssvep_result = 0
    return ssvep_result, 0

