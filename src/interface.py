import pylsl
import numpy
from sklearn.discriminant_analysis import LinearDiscriminantAnalysis
from scipy import signal 

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
    samples, times = inlet.pull_chunk()
    return times, samples

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
    dat = dat[:, 0:end_col]
    x = dat[0:end_row, 2:end_col]
    y = dat[0:end_row, 1]
    return x,y

def trial_to_feat(x, lowfreq, hifreq):
    """
    trial_to_feat() - convert the data from a single calibration trial into a feature vector.
    @x: The raw electrode data for a single trial (should be 300 samples). 

    Returns: A feature vector, ready to be appended then fed into the LDA trainer.
    """
    o1 = seq_to_bands(x[:, 0], lowfreq, hifreq)
    o2 = seq_to_bands(x[:, 1], lowfreq, hifreq)
    oz = seq_to_bands(x[:, 2], lowfreq, hifreq)
    p3 = seq_to_bands(x[:, 3], lowfreq, hifreq)
    p4 = seq_to_bands(x[:, 4], lowfreq, hifreq)
    pz = seq_to_bands(x[:, 5], lowfreq, hifreq)
    c3 = seq_to_bands(x[:, 6], lowfreq, hifreq)
    c4 = seq_to_bands(x[:, 7], lowfreq, hifreq)

    weights = numpy.array([1, 1, 1, 0.2, 0.2, 0.2, 0.2, 0.2])

    mean_8hz  = numpy.mean([o1[0], o2[0], oz[0]])
    mean_19hz = numpy.mean([o1[1], o2[1], oz[1]])
    feat = numpy.array([mean_8hz, mean_19hz])
    return feat

def seq_to_bands(x, lowfreq, hifreq):
    """
    seq_to_amp() - convert a single electrode data sequence into 2 band powers
    @x: Raw electrode data for a single electrode.

    Returns: A numpy array containing the band power at the relevant frequencies.
    """
    amp_lo  = seq_to_pwr(x, lowfreq - 0.5, lowfreq + 0.5, 37, 750)
    amp_hi = seq_to_pwr(x, highfreq - 0.5, highfreq + 0.5, 37, 750)
    amps = numpy.array([amp_lo, amp_hi])
    return amps

def seq_to_pwr(x, lowfreq, hifreq, first_sample, epoch):
    """
    seq_to_pwr() - convert a single electrode data sequence into a band power amplitude
    @x: Single electrode data.
    @lowfreq: Low cutoff frequency.
    @hifreq: High cutoff frequency.

    Returns: A single amplitude value. 
    """
    # Skip first 150ms
    x = x[first_sample:(first_sample+epoch), :]
    spec  = numpy.fft.fft(x)
    freqs = numpy.fft.fftfreq(len(x), 1.0/250.0)
    mask  = numpy.logical_and(freqs >= lowfreq, freqs <= hifreq)
    avg   = spec[mask].mean()
    return avg

def butter_filter():
    filt_a, filt_b = signal.butter(5, [5, 20], 'bandpass', analog=True)
    return filt_a, filt_b

def butter_bp(x):
    a, b = butter_filter()
    y =  lfilter(a, b, x)
    return y 

def get_classifier(cal_file):
    """"
    get_classifier() - generate an SSVEP classifier using LDA, based on a calibration file
    @cal_file: The full path of the calibration file.

    Returns: Scikit classifier object.
    """
    x,y = csv_to_nparray(cal_file)
    feats = numpy.empty((60, 2))

    indecies = []
    k = 0
    l = 0
    y2 = []
    while l <= 60:
        if y[k] != y[k+1]:
            indecies.append(k)
            l += 1
            y2.append(y[k])
        k += 1

    j = 0
    for i in range(0, 60):
        feats[i] =  trial_to_feat(x[j:j+indecies[i], :], 12.0, 20.0)
        j += indecies[i]
    print feats
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

def classify_buf(lda_classifier, sample_buf):
    """
    classify_buf() - online function, takes the sample buffer, does EEG classification to determine game action
    buf - The buffer containing relevant  EEG stream samples.

    Returns: ssvep_result controls game rotation and is 0/1/2 for left/none/right,
             mimg_result controls firing and is 0/1 for fire/don't fire
    """
    feat = trial_to_feat(sample_buf)
    pred = clf.predict(feats)
    ssvep_result = pred
    return ssvep_result, 0

