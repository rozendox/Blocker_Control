from moviepy.editor import *
from moviepy.video.VideoClip import TextClip


def texto_clip(texto, duracao, fontsize=70, color='white'):
    return TextClip(texto, fontsize=fontsize, color=color, font='Arial-Bold').set_duration(duracao).set_position(
        'center')


duracao_b = 1  # in this case 1 sec to finz.
duracao_c = 1  # "                    "
duracao_bcinc = 2

clipe_b = texto_clip("B", duracao_b)
clipe_c = texto_clip("C", duracao_c)
clipe_bcinc = texto_clip("B.C inc", duracao_bcinc)

clipe_b = clipe_b.crossfadein(0.5).crossfadeout(0.5)
clipe_c = clipe_c.crossfadein(0.5).crossfadeout(0.5)
clipe_bcinc = clipe_bcinc.crossfadein(0.5)

#bora conct?
video_final = concatenate_videoclips([clipe_b, clipe_c, clipe_bcinc])

video_final = video_final.on_color(size=(640, 480), color=(0, 0, 0))

video_final.write_videofile("bc_inc.mp4", fps=24)
