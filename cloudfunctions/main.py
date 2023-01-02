import numpy
import tensorflow

from google.cloud import storage




# We keep model as global variable so we don't have to reload it in case of warm invocations
model = None

def download_blob(bucket_name, source_blob_name, destination_file_name):
    """Downloads a blob from the bucket."""
    storage_client = storage.Client()
    bucket = storage_client.get_bucket(bucket_name)
    blob = bucket.blob(source_blob_name)

    blob.download_to_filename(destination_file_name)

    print('Blob {} downloaded to {}.'.format(
        source_blob_name,
        destination_file_name))

def handler(request):
    global model
    

    # Model load which only happens during cold starts
    if model is None:
        download_blob('thecrapbucket', 'tfmodels/mobilenet_finetune.h5', '/tmp/mobilenet_finetune.h5')
        model = tensorflow.keras.models.load_model('/tmp/mobilenet_finetune.h5')
    
    request_json = request.get_json()
    predictions = int(tensorflow.round(tensorflow.nn.sigmoid(model.predict(request_json['instances']))))
    
    result = {
        "predictions": predictions
    }
    
    return result