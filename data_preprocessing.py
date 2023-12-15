import mne
import zipfile

import pandas as pd


def get_data(file='A01E'):
    # get data
    raw = mne.io.read_raw_gdf(f"{file}.gdf", eog=['EOG-left', 'EOG-central', 'EOG-right'], preload=True)
    raw.drop_channels(['EOG-left', 'EOG-central', 'EOG-right'])
    raw.set_eeg_reference()

    # filter(notch, s-golay)
    raw = raw.notch_filter(50)
    raw = raw.savgol_filter(10)

    # feature extraction
    events = mne.events_from_annotations(raw)
    epoch = mne.Epochs(raw, events[0], event_id=[7, 8, 9, 10], tmin=-0.1, tmax=0.7, on_missing='warn')

    return epoch, raw


def make_csv_file(file='A01E'):
    epoch, raw = get_data(file=file)
    epoch.to_data_frame().to_csv(file)


# Extract and Open BCICIV_2a zip file
zipfile.ZipFile('BCICIV_2a_gdf.zip').extractall()

gdf_file_name = []
with zipfile.ZipFile('BCICIV_2a_gdf.zip', 'r') as BCI_data:
    data_file_name = BCI_data.namelist()
    for fileName in data_file_name:
        print(fileName)
        gdf_file_name.append(fileName.split('.gdf')[0])

for file_name in gdf_file_name:
    make_csv_file(file=file_name)
