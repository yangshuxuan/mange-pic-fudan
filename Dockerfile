FROM continuumio/miniconda3
RUN apt-get update
RUN apt-get -y upgrade
RUN apt install -y libmariadbd-dev
RUN apt install -y gcc
WORKDIR /app

# Create the environment:
COPY environment.yml .

SHELL ["/bin/bash", "--login", "-c"]
# RUN ["conda","env", "create", "-f", "environment.yml"]
RUN conda env create -f environment.yml

# Make RUN commands use the new environment:
RUN echo "conda activate django" >> ~/.bashrc
COPY . .
RUN apt-get -y install netcat
EXPOSE 9001
# The code to run when container is started:
ENTRYPOINT ["./entrypoint.sh"]