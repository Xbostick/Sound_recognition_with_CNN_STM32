import numpy as np
import tensorflow as tf
import matplotlib.pyplot as plt


def convert_to_tflite(x_test, tf_model, model_name = "model_full_integer_quantized.tflite"):
    """
    Convert a TensorFlow Keras model to a fully quantized TFLite model.
    
    :param x_test: Test dataset used for representative dataset generation.
    :param tf_model: Trained TensorFlow Keras model.
    :param model_name: Name to save the converted TFLite model.
    :return: Path of the saved TFLite model.
    """
    x_test = np.array(x_test, dtype = np.float32)
    def __representative_dataset_gen():
        for i in range(len(x_test)-1) :
                # This should be a generator yielding batches of input data.
                # The input shape should match the shape of the model's input.
                yield [x_test[i:i+1]]


    converter = tf.lite.TFLiteConverter.from_keras_model(tf_model)
    converter.optimizations = [tf.lite.Optimize.DEFAULT]
    converter.representative_dataset = __representative_dataset_gen
    tflite_quant_model = converter.convert()


    # Save the fully quantized TFLite model to a file
    with open(model_name, "wb") as f:
        f.write(tflite_quant_model)

    print("Model successfully quantized to full integer precision and saved as '{model_name}'")
    return save_path         

def convertCheck(tf_model, tf_lite_model_path, x_test):
    # Load TFLite model and allocate tensors.
    interpreter = tf.lite.Interpreter(model_path = "model_full_integer_quantized.tflite", visualise = True)
    interpreter.allocate_tensors()

    # Get input and output tensors.
    input_details = interpreter.get_input_details()
    output_details = interpreter.get_output_details()

    model_ouput = np.argmax(model(x_test), axis = 1)
    quant_output = []
    GT_output = np.argmax(y_test, axis = 1)

    for sample in x_test:
        interpreter.set_tensor(input_details[0]['index'], [sample])
        interpreter.invoke()
        output_data = interpreter.get_tensor(output_details[0]['index'])
        quant_output.append(np.argmax(output_data))
    if visualise:                  
        plt.hist(model_ouput,ls='dashed', lw=3, fc=(0, 0, 1, 0.5), color = 'b', label = "original model")
        plt.hist (quant_output, ls='dotted', lw=3, fc=(1, 0, 0, 0.5), color = 'g', label = "quantize model")
        plt.hist(GT_output, fc=(0, 1, 0, 0.5), color = 'r', label = "ground truth")
        plt.legend()
        plt.show()
    return {
        "Original_model_results": model_ouput,
        "Converted_model_output" : quant_output,
        "X_test": GT_output
            }