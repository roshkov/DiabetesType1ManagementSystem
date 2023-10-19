# 
FROM python:3.9

# 
WORKDIR /code

# 
COPY ./external/requirements.txt /code/requirements.txt

# 
RUN pip install --no-cache-dir --upgrade -r /code/requirements.txt

# 
COPY ./external/external /code/external

# 
CMD ["uvicorn", "external.main:app", "--host", "0.0.0.0", "--port", "80"]