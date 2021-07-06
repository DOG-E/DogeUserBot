# Get Docker image
FROM sandy1709/catuserbot:alpine

# Clone Doge repository
RUN git clone https://github.com/DOG-E/DogeUserBot.git /root/userbot

# Work directory
WORKDIR /root/userbot

# Install requirements
RUN pip3 install -U -r requirements.txt

# Minor adjustment
ENV PATH="/home/userbot/bin:$PATH"

# Run Doge
CMD ["python3", "doger.py"]