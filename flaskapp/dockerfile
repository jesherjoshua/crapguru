FROM python:3.8-slim

WORKDIR /Crap_guru
COPY . .

RUN pip install -r requirements.txt

ENTRYPOINT [ "python" ]
CMD ["app.py"]

# To create image: docker build {directory/folder of application} --tag {name of image}
# To run the image: docker run -p 8080:8080 {name of image}
# To open the website use port 8080