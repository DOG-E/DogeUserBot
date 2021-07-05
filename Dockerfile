# Get Docker image
FROM teledoge/dogeuserbot:test

# Get requirements & install
RUN wget https://raw.githubusercontent.com/DOG-E/DogeUserBot/DOGE/requirements.txt -O requirements-temp.txt \
	&& pip3 install -U -r requirements-temp.txt

# Clone Doge repository
RUN git clone https://github.com/DOG-E/DogeUserBot.git /root/dogebot

# Work directory
WORKDIR /root/dogebot

# Minor adjustment
ENV PATH="/home/dogebot/bin:$PATH"

# Run Doge
CMD ["python3", "-m", "dogebot"]