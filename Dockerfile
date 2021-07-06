# Get Docker image
FROM teledoge/dogeuserbot:latest

# Clone Doge repository
RUN git clone https://github.com/DOG-E/DogeUserBot.git /root/dogebot

# Work directory
WORKDIR /root/dogebot

# Minor adjustment
ENV PATH="/home/dogebot/bin:$PATH"

# Run Doge
CMD ["python3", "doger"]