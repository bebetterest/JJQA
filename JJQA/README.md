---
dataset_info:
- config_name: qa
  features:
  - name: q
    dtype: string
  - name: a
    dtype: string
  - name: rf
    dtype: string
  - name: song_title
    dtype: string
  - name: song_id
    dtype: string
  - name: id
    dtype: string
  splits:
  - name: train
    num_bytes: 67824
    num_examples: 648
  download_size: 134589
  dataset_size: 67824
- config_name: song
  features:
  - name: id
    dtype: string
  - name: title
    dtype: string
  - name: name
    dtype: string
  - name: lyric
    dtype: string
  splits:
  - name: train
    num_bytes: 253605
    num_examples: 181
  download_size: 276024
  dataset_size: 253605
- config_name: song_index
  features:
  - name: dic
    dtype: string
  splits:
  - name: train
    num_bytes: 2872
    num_examples: 1
  download_size: 4168
  dataset_size: 2872
---
