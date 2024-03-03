# -*- coding: utf-8 -*-
"""text generator

Automatically generated by Colaboratory.

Original file is located at
    https://colab.research.google.com/drive/16XmT-GS7UAcS6Vt61wkPgDoPUB28yLf1
"""

import tensorflow as tf
from tensorflow.keras.layers import LSTM, Dense
from tensorflow.keras.models import Sequential
from tensorflow.keras.callbacks import LambdaCallback
import numpy as np
import random
import sys
import os

text_data=open('text_data.txt','r').read()

chars=sorted(list(set(text_data)))
char_to_index={char:i for i, char in enmerate(chars)}
index_to_char={i:char for i, char in enumerate(chars)}
max_length=40
sequence=[]
next_char=[]

for i in range(0,len(text_data)-max_length,1):
  sequence.append(text_data[i:i+max_length])
  next_char.append(text_data[i+max_length])

X=np.zeros((len(sequences), max_length, len(chars)), dtype=np.bool)
y=np.zeros((len(sequences), len(chars)), dtype=np.bool)

for i, sequence in enumerate(sequences):
  for t, char in enumerate(sequence):
    X[i, t, char_to_index[char]] = 1
    y[i, char_to_index[next_char[i]]] = 1

model = Sequential([LSTM(128, input_shape=(max_length, len(chars))),Dense(len(chars), activation='softmax')])
model.compile(loss='categorical_crossentropy', optimizer='adam')

def sample(preds, temperature=1.0):
  preds = np.asarray(preds).astype('float64')
  preds = np.log(preds) / temperature
  exp_preds = np.exp(preds)
  preds = exp_preds / np.sum(exp_preds)
  probas = np.random.multinomial(1, preds, 1)
  return np.argmax(probas)

def generate_text(seed_text, num_chars_to_generate=400, temperature=0.5):
  generated_text = seed_text
  for i in range(num_chars_to_generate):
    x_pred = np.zeros((1, max_length, len(chars)))
    for t, char in enumerate(seed_text):
      x_pred[0, t, char_to_index[char]] = 1.
      preds = model.predict(x_pred, verbose=0)[0]
      next_index = sample(preds, temperature)
      next_char = index_to_char[next_index]
      generated_text += next_char
      seed_text = seed_text[1:] + next_char
    return generated_text

def on_epoch_end(epoch, _):
  print('\nGenerating text after epoch %d' % epoch)
  seed_text = 'The meaning of life is'
  for temperature in [0.2, 0.5, 1.0]:
    print('\nTemperature:', temperature)
    generated_text = generate_text(seed_text, temperature=temperature)
    print(generated_text)

print_callback = LambdaCallback(on_epoch_end=on_epoch_end)
model.fit(X, y, batch_size=128, epochs=20, callbacks=[print_callback])