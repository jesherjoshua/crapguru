FROM python:3.8.9

RUN pip install --upgrade pip

WORKDIR /app

COPY requirements.txt .

RUN pip install --no-cache-dir -r  requirements.txt 


ENV PORT=


COPY crapguru.py . 
COPY mobilenet_finetune.h5 .
COPY builder.py .
RUN cp builder.py /usr/local/lib/python3.8/site-packages/google/protobuf/internal/

CMD streamlit run crapguru.py --server.port=${PORT}  --browser.serverAddress="0.0.0.0"
