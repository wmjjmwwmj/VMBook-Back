# Use the official Python image from the Docker Hub
FROM registry.cn-hangzhou.aliyuncs.com/base_mj/vmbook:python39

# Set the working directory in the container
WORKDIR /ws

# Copy the requirements file into the container
COPY ./requirements.txt /ws/requirements.txt

# Install the required dependencies
RUN pip install --no-cache-dir -r requirements.txt -i https://mirrors.aliyun.com/pypi/simple/

# Copy the rest of the application code into the container
COPY ./ /ws/

# Expose the port that the app runs on
EXPOSE 8000

# Command to run the application
CMD ["cd","/ws/app", "&&", "uvicorn", "main:app", "--host", "0.0.0.0", "--port", "8000"]