import os
os.environ['TF_CPP_MIN_LOG_LEVEL'] = '3' 
import tensorflow as tf
import keras_nlp

class Answer:
    def __init__(self, isAi, percentage):
        self.isAi = isAi
        self.percentage = percentage
    def to_dict(self):
        return {'isAi': self.isAi, 'percentage': self.percentage}

loaded_model = None

# Adding preprocessor and encoders

text_input = tf.keras.layers.Input(shape=(), dtype=tf.string)
preprocessor = keras_nlp.models.BertPreprocessor.from_preset("bert_base_en_uncased")
encoder_inputs = preprocessor(text_input)
encoder = keras_nlp.models.BertBackbone.from_preset("bert_base_en_uncased",trainable=True )
outputs = encoder(encoder_inputs)
pooled_output = outputs["pooled_output"]      # [batch_size, 768].
sequence_output = outputs["sequence_output"]  # [batch_size, seq_length, 768].

# Defining model
dropout = tf.keras.layers.Dropout(0.51 , name="dropout1")(pooled_output)
dense_2 = tf.keras.layers.Dense(64 , activation='relu')(dropout)
dropout = tf.keras.layers.Dropout(0.3 , name="dropout2")(dense_2)

dense_out = tf.keras.layers.Dense(1 , activation='sigmoid', name='output')(dropout)

loaded_model = tf.keras.Model(inputs=text_input, outputs=dense_out)


loaded_model.compile(optimizer=tf.keras.optimizers.Adam(learning_rate=1e-6),
            loss='binary_crossentropy',
            metrics=["acc"])
    
loaded_model.load_weights("models/explicitly_saved_model.weights.h5")


def run_model(data):
    text_sample = []
    text_sample.append(data["text"])

    test_result = loaded_model.predict(text_sample)

    predicted_result_class = [1 * (x[0] >= 0.5) for x in test_result]
    answer = "human" if predicted_result_class[0] == 0 else "ai"

    return Answer(answer, int(test_result.item() * 100)).to_dict()