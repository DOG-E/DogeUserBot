# @DogeUserBot - < https://t.me/DogeUserBot >
# Copyright (C) 2021 - DOG-E
# All rights reserved.
#
# This file is a part of < https://github.com/DOG-E/DogeUserBot >
# Please read the GNU Affero General Public License in;
# < https://www.github.com/DOG-E/DogeUserBot/blob/DOGE/LICENSE/ >
# ================================================================
# Get Docker image
FROM sandy1709/catuserbot:slim-buster

# Clone Doge repository + work directory + minor adjustment
RUN git clone https://github.com/DOG-E/DogeUserBot.git /root/DogeUserBot
WORKDIR /root/DogeUserBot
ENV PATH="/root/DogeUserBot/bin:$PATH"

# Install requirements
RUN pip3 install --no-cache-dir -U -r requirements.txt

# Run Doge
RUN chmod a+x doger
CMD ["./doger"]