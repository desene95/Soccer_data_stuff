# Use an official Jupyter Notebook base image
FROM jupyter/base-notebook:latest

# Install required Python packages
RUN pip install numpy pandas selenium beautifulsoup4 pydantic  mplsoccer seaborn sqlalchemy
# Install Chromedriver and its dependencies
USER root
RUN apt-get update && \
    apt-get install -y chromium-driver && \
    apt-get clean && \
    systemctl enable dbus && \
    apt-get install snapd && \
    systemctl start snapd && \
    rm -rf /var/lib/apt/lists/*
USER $NB_UID

#RUN apt install snapd
#RUN systemctl start snapd

# Expose the Jupyter Notebook port
EXPOSE 8888

# Start Jupyter Notebook upon container startup
CMD ["jupyter", "notebook", "--ip=0.0.0.0", "--port=8888", "--no-browser", "--allow-root"]