import neurokit2 as nk
import pandas as pd
import wfdb

def calculate_bpm(ecg_signal_path):
  
    # Load ECG signal using wfdb
    record = wfdb.rdrecord(ecg_signal_path, channels=[0])
    
    ecg_signal = record.p_signal[:, 0]

    sampling_rate = record.fs

    # Process ECG signal to get BPM using NeuroKit2
    try:
        ecg_signals, info = nk.ecg_process(ecg_signal, sampling_rate=sampling_rate)
    except Exception as e:
        print(f"Error processing interval ecg signal: {e}")
        return None
  
    # Calculate average BPM from processed ECG signal
    bpm = ecg_signals["ECG_Rate"]

    avg_bpm = pd.Series(bpm).mean()
    rounded_avg_bpm = round(avg_bpm)
    return avg_bpm, rounded_avg_bpm
