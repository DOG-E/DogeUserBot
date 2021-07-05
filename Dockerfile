# Get Docker image
FROM teledoge/dogeuserbot:test

# Clone Doge repository
RUN git clone https://github.com/DOG-E/DogeUserBot.git /DogeUserBot

# Work directory
WORKDIR /DogeUserBot

# Minor adjustment
ENV PATH="/home/dogebot/bin:$PATH"

# Run Doge
CMD ["python3", "-m", "dogebot"]