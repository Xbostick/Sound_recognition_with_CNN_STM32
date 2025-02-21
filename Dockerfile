FROM tensorflow/tensorflow:2.13.0-jupyter

LABEL project="STM32_model_creating"

WORKDIR /usr/src/app

# Copy project files
COPY ./ModelCreating_python ./

# Update and install necessary packages
RUN apt update && apt upgrade -y && \
    apt install -y wget

# Install Python dependencies
COPY requirements.txt ./
RUN python -m pip install --upgrade pip && \
    pip install --no-cache-dir -r requirements.txt

# Set up Jupyter notebook theme (optional, consider removing if not needed)
RUN jt -t monokai -f fira -fs 10 -nf ptsans -nfs 11 -N -kl -cursw 2 -cursc r -cellw 95% -T || true

# Expose Jupyter Notebook port
EXPOSE 8888

# Define entry point and default command
ENTRYPOINT ["python3", "-m"]
CMD ["jupyter", "notebook", "--port=8888", "--no-browser", "--ip=0.0.0.0", "--allow-root"]
