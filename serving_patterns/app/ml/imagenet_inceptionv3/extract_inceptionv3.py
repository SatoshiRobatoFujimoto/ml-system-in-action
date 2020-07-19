import os
import tensorflow as tf
import tensorflow_hub as hub
from PIL import Image
import numpy as np

from app.constants import PREDICTION_TYPE, MODEL_RUNTIME, DATA_TYPE
from app.ml.save_helper import save_interface, load_labels
from app.ml.transformers import TFImagePreprocessTransformer, SoftmaxTransformer
from app.ml.extract_from_tfhub import get_model

MODEL_DIR = './models/'
MODEL_FILE_DIR = 'savedmodel/inceptionv3'
SAVEDMODEL_DIR = os.path.join(MODEL_DIR, MODEL_FILE_DIR)
SAMPLE_IMAGE = os.path.join('./app/ml/data', 'good_cat.jpg')
LABEL_FILE = os.path.join(MODEL_DIR, 'imagenet_labels_1001.json')
LABELS = load_labels(LABEL_FILE)


def validate(image, preprocess, predictor, postprocess):
    np_image = preprocess.transform(image)
    result = predictor.predict(np_image)
    result_proba = postprocess.transform(result)
    print(result_proba)
    top1_index = np.argmax(result_proba[0], axis=-1)
    print(top1_index)
    print(LABELS[top1_index])


def main():
    os.makedirs(SAVEDMODEL_DIR, exist_ok=True)

    hub_url = 'https://tfhub.dev/google/imagenet/inception_v3/classification/4'
    model = get_model(hub_url, (299, 299, 3))
    preprocess = TFImagePreprocessTransformer()
    postprocess = SoftmaxTransformer()

    image = Image.open(SAMPLE_IMAGE)

    validate(image, preprocess, model, postprocess)

    tf.saved_model.save(model, SAVEDMODEL_DIR)

    modelname = 'imagenet_inceptionv3'
    interface_filename = f'{modelname}.yaml'
    preprocess_filename = f'{modelname}_preprocess_transformer.pkl'
    postprocess_filename = f'{modelname}_softmax_transformer.pkl'

    save_interface(MODEL_DIR,
                   modelname,
                   interface_filename,
                   [1, 299, 299, 3],
                   'float32',
                   [1, 1001],
                   'float32',
                   DATA_TYPE.IMAGE,
                   [{preprocess_filename: MODEL_RUNTIME.SKLEARN},
                    {MODEL_FILE_DIR: MODEL_RUNTIME.TF_SERVING},
                    {postprocess_filename: MODEL_RUNTIME.SKLEARN}],
                   PREDICTION_TYPE.CLASSIFICATION,
                   'app.ml.imagenet_inceptionv3.imagenet_inceptionv3_predictor',
                   label_filepath=LABEL_FILE)

if __name__ == '__main__':
    main()
