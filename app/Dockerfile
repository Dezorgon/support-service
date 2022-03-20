FROM python:3.9

ENV PYTHONUNBUFFERED 1
ENV PYTHONDONTWRITEBYTECODE 1


COPY requirements.txt .
RUN pip install -r requirements.txt
RUN pip install gunicorn


RUN mkdir -p /app/static
RUN useradd -U user
RUN chown -R user:user /app/static
RUN chmod -R 755 /app/static
USER user


WORKDIR /app
COPY --chown=user:user . .