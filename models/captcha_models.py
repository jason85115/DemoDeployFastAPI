import numpy as np
import tensorflow as tf
from tensorflow.keras.models import Model
from tensorflow.keras.layers import Input, Dense, Dropout, Flatten, Conv2D, MaxPooling2D

config = tf.compat.v1.ConfigProto()
config.gpu_options.allow_growth = True
session = tf.compat.v1.Session(config=config)

class captcha_model_id:
    def __init__(self):
        self.model = None
        self.load_model()

    def load_model(self):

        tensor_in = Input((60, 200, 3))
        out = tensor_in
        out = Conv2D(filters=32, kernel_size=(3, 3), padding='same', activation='relu')(out)
        out = Conv2D(filters=32, kernel_size=(3, 3), activation='relu')(out)
        out = MaxPooling2D(pool_size=(2, 2))(out)
        out = Conv2D(filters=64, kernel_size=(3, 3), padding='same', activation='relu')(out)
        out = Conv2D(filters=64, kernel_size=(3, 3), activation='relu')(out)
        out = MaxPooling2D(pool_size=(2, 2))(out)
        out = Conv2D(filters=128, kernel_size=(3, 3), padding='same', activation='relu')(out)
        out = Conv2D(filters=128, kernel_size=(3, 3), activation='relu')(out)
        out = MaxPooling2D(pool_size=(2, 2))(out)
        out = Conv2D(filters=256, kernel_size=(3, 3), activation='relu')(out)
        out = MaxPooling2D(pool_size=(2, 2))(out)
        out = Flatten()(out)
        out = Dropout(0.3)(out)
        out = [Dense(63, name='digit1', activation='softmax')(out),\
            Dense(63, name='digit2', activation='softmax')(out),\
            Dense(63, name='digit3', activation='softmax')(out),\
            Dense(63, name='digit4', activation='softmax')(out),\
            Dense(63, name='digit5', activation='softmax')(out),\
            Dense(63, name='digit6', activation='softmax')(out)]

        self.model = Model(inputs=tensor_in, outputs=out)
        # Define the optimizer
        self.model.compile(loss='categorical_crossentropy', optimizer='Adamax', metrics=['accuracy'])

    def load_weights(self, path):
        self.model.load_weights(path)

    def predict(self, image):
        def change_character(pred_prob):
            total_set = []
            for i in range(97, 123):
                total_set.append(chr(i))
            for i in range(65, 91):
                total_set.append(chr(i))
            for i in range(10):
                total_set.append(str(i))
            total_set.append('')
            for i in range(len(pred_prob)):
                if pred_prob[i] == max(pred_prob):
                    value = (total_set[i])

            return value

        train_set = np.ndarray((1, 60, 200, 3), dtype=np.uint8)
        # image = cv2.imread(image_name)
        train_set[0] = image

        result = self.model.predict(train_set)

        resultlist = ''
        for i in range(len(result)):
            resultlist += change_character(result[i][0])

        # os.chdir(os_path)
        return resultlist