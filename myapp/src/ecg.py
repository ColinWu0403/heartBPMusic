import neurokit2 as nk
import pandas as pd
import wfdb
import os


def calculate_bpm(ecg_signal_path):
    # Determine the file extension
    file_extension = os.path.splitext(ecg_signal_path)[1]

    if file_extension == '.csv':
        # Load ECG signal using pandas for .csv files
        df = pd.read_csv(ecg_signal_path)
        ecg_signal = df['Lead2'].values
        sampling_rate = 1000
        try:
            ecg_signal = nk.ecg_clean(ecg_signal, sampling_rate=sampling_rate)
        except Exception as e:
            print(f"Error cleaning ECG signal: {e}")
            return None
    else:
        # Load ECG signal for .dat files
        record = wfdb.rdrecord(ecg_signal_path, channels=[0])
        ecg_signal = record.p_signal[:, 0]
        sampling_rate = record.fs

    # Process ECG signal to get BPM using NeuroKit2
    try:
        ecg_signals, info = nk.ecg_process(ecg_signal, sampling_rate=sampling_rate)
    except Exception as e:
        print(f"Error processing ECG signal: {e}")
        return None

    # Calculate average BPM from processed ECG signal
    bpm = ecg_signals["ECG_Rate"]
    avg_bpm = pd.Series(bpm).mean()
    rounded_avg_bpm = round(avg_bpm)

    return avg_bpm, rounded_avg_bpm
