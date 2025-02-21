from tensorflow import keras
from .dataPreprocess import numOfDctOutputs

def get_model(input_shape, output_shape):
    model = keras.Sequential(layers=[
            keras.layers.InputLayer(input_shape=input_shape),
            keras.layers.Reshape(target_shape = (-1,numOfDctOutputs)),
            keras.layers.Conv1D(32, 5, padding='same', activation=keras.activations.relu, name="Conv_1"),
            keras.layers.MaxPooling1D(name="MaxPooling_1"),
            keras.layers.Conv1D(64, 5, padding='same', activation=keras.activations.relu, name="Conv_2"),
            keras.layers.MaxPooling1D( name="MaxPooling_2"),
            keras.layers.Conv1D(128, 5, padding='same', activation=keras.activations.relu, name="Conv_3"),
            keras.layers.MaxPooling1D( name="MaxPooling_3"),
            keras.layers.Conv1D(256, 5, padding='same', activation=keras.activations.relu, name="Conv_4"),
            keras.layers.MaxPooling1D( name="MaxPooling_4"),
            keras.layers.Conv1D(512, 3, padding='same', activation=keras.activations.relu, name="Conv_5"),
            keras.layers.MaxPooling1D( name="MaxPooling_5"),
            keras.layers.Conv1D(1024, 3, padding='same', activation=keras.activations.relu, name="Conv_6"),
            keras.layers.MaxPooling1D( name="MaxPooling_6"),
            keras.layers.Flatten(name="Flatten"), # this layer "converts matrix to single array"
            keras.layers.Dropout(0.5, name="Dropout"),
            keras.layers.Dense(128, activation=keras.activations.relu, name="Dense_1"),
            keras.layers.Dense(32, activation=keras.activations.relu, name="Dense_2"),
            keras.layers.Dense(output_shape, activation=keras.activations.softmax, name="Dense_final")
        # keras.layers.Dense(classes_quantity, name="Dense_final")
        ], name ="Convolutional_Model")
    model.compile(optimizer=keras.optimizers.Adam(), loss=keras.losses.BinaryCrossentropy(), metrics=['accuracy'])
    return model