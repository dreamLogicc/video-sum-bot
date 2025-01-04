import ffmpeg


def convert_to_audio(file_path):
    '''
        Function converts video file to audio and writes it into temporary folder
        :param file_path: Path to video file
        :return: Path to audio file
    '''
    stream = ffmpeg.input(file_path)
    audio_track = stream.audio
    filename = ".temp/audio.mp3"
    stream = ffmpeg.output(audio_track, filename)
    ffmpeg.run(stream)
    return filename
