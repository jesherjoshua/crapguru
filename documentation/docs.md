# Documentation for Replication

1. ## Cloud Storage:

   - create standard bucket using cloud console
   - disable public access
   - create dir tfmodels
   - upload model inside tfmodels
2. ## Cloud Functions:

   - select python 3.8 as the runtime
   - copy the following in main.py:
     ```
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
     ```

- copy the following in requirements.txt

  ```
  # Function dependencies, for example:
  # package>=version

  tensorflow==2.10
  google-cloud-storage>=1.16.1
  ```
- allocate >1GB memory
- allow all ingress traffic
- create cloud functions
- under permissions click grant access: type: ` allUsers` in new pricipal select functions invoker in new role.
- check function using the following code:

  ```
  import tensorflow as tf
  import numpy as np
  import json
  import requests
  def pre_process(img):
      img = tf.keras.preprocessing.image.load_img(img, target_size=(96, 96))
      img = tf.keras.preprocessing.image.img_to_array(img)
      img = np.expand_dims(img, axis=0)
      return img
  img='image path'
  img=pre_process(img)
  url='https://us-central1-global-snow-372118.cloudfunctions.net/crapguru_func_v1'
  payload = json.dumps({"instances": img.tolist()})
  headers = {'Content-type': 'application/json'}
  response = requests.post(url, data=payload, headers=headers)
  result = response.json()
  predictions = result["predictions"]
  print("response code:", response)
  print(predictions)
  ```

3. # Cloud Run:


   - upload the app directory to GCP via cloud shell
   - cd to app directory which has the docker file
   - run the following snippet in cloud shell to create docker image:
     ` docker build -t crapguru:v1.0 .`
   - run the created docker container using the following:
     ` docker run --rm --name mytest -p 8900:${MYPORT} -e PORT=${MYPORT} crapguru:v1.0`
   - use the following cloud shell commands to config gcp:
     ```
     gcloud config set compute/region <YOUR-REGION>
     gcloud config set compute/zone <YOUR-ZONE>
     gcloud services enable run.googleapis.com containerregistry.googleapis.com 
     gcloud auth configure-docker 
     ```
   - tag and push the docker image:

   ```
     docker tag crapguru:v1.0 gcr.io/< YOUR GCP PROJECT ID > /crapguru:v1.0
     docker push gcr.io/< YOUR GCP PROJECT ID > /crapguru:v1.0 
   ```
   - use the cloud console to setup cloud run:
     **Note:**
     - supply product name(crapguru) as service name
     - allow unauthorized access(for public access)
     - set timeout to 900s
     - select your container image from container registry
   - Click to deploy and share the URL.
