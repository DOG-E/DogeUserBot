# Get Docker image
FROM teledoge/dogeuserbot:latest

# Clone Doge repository
RUN git clone https://github.com/DOG-E/DogeUserBot.git /root/DogeUserBot

# Work directory
WORKDIR /root/DogeUserBot

# Minor adjustment
ENV PATH="/home/dogebot/bin:$PATH"

# Run Doge
CMD ["python3", "-m", "dogebot"]