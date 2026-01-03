This script searches the current folder and will combine multiple .vtt files, into a text file with transcription format.
> Speaker1: [HH:MM:SS:mmm] Text that is spoken.
> 
> Speaker2: [HH:MM:SS:mmm] Other text that is spoken.

The primary use of this is to combine .vtt files from TTRPG sessions played through [Discord](https://discord.com/), and recorded using [Craig](https://github.com/CraigChat/craig).

The script will prompt the user to clarify the names of each speaker. If nothing is entered, it will use the filename of the .vtt file as the speaker.
The script also searches for phrases or repetitions which are common hallucinations from [Whisper AI](https://github.com/openai/whisper) and filters them out.

The python file can be saved in the directory of .vtt files, and will create the transcript by entering `python3 combine_vtt.py` into the a terminal window. Remember to change the current directory to the location of the .vtt and .py files, otherwise it will not work.
