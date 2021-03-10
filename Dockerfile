FROM python:3.7
LABEL maintainer=duke.lv@hotmail.com
# RUN apk update && apk add build-base
# RUN apk update && apk add --no-cache gcc musl-dev libxslt-dev

WORKDIR /app
COPY . .
RUN python -m pip install --upgrade pip && pip install -r requirements.txt -i https://pypi.tuna.tsinghua.edu.cn/simple
RUN pip install uvicorn  -i https://pypi.tuna.tsinghua.edu.cn/simple



EXPOSE 8000

CMD ["uvicorn", "app:app", "--host", "0.0.0.0", "--port", "8000"]