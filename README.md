Requirements:

1] davey
2] pynacl
3] yt-dlp
4] discord.py
5] ffmpeg

install them with pip before running the bot

in dev portal Enable these for the bot to work, 
<img width="1509" height="414" alt="Screenshot 2026-06-18 181511" src="https://github.com/user-attachments/assets/bf6fbb10-2e65-4f56-8524-fed21c2097a1" />

Note:
If you try to run this bot on termux like me, install rust and if you further encounter any issues with installing davey, try 
export ANDROID_API_LEVEL=$(getprop ro.build.version.sdk)
echo $ANDROID_API_LEVEL #try this and if you dont see any number being printed then add it manually
pip install -U davey

#adding version manually
export ANDROID_API_LEVEL=36 #this is for android 16 check for your versions
pip install -U davey
