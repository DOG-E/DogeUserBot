# Get Docker image
FROM teledoge/dogeuserbot:doger

# Clone Doge repository
RUN git clone https://github.com/DOG-E/DogeUserBot.git /root/userbot

# Work directory
WORKDIR /root/userbot

# Install requirements
RUN pip3 install --no-cache-dir -U -r requirements.txt

# Minor adjustments
ENV PATH="/home/userbot/bin:$PATH"
RUN chmod -R 755 bin

# Run Doge
CMD ["python3", "doger.py"]