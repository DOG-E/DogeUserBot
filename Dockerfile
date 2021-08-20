# Get Docker image
FROM mutlcc/dogebot:dogeuserbot

# Clone Doge repository + work directory + minor adjustment
RUN git clone https://github.com/DOG-E/DogeUserBot.git /usr/src/userbot
WORKDIR /usr/src/userbot
ENV PATH="/usr/src/userbot/bin:$PATH"

# Install requirements
RUN pip3 install -U -r requirements.txt

# Run Doge
RUN chmod a+x doger
CMD ["./doger"]