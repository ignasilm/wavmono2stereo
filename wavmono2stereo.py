from pydub import AudioSegment
import argparse
import textwrap
from os import chdir
import glob

print(' ')
ap = argparse.ArgumentParser(add_help=False, 
                             description='Utilidad para convertir varios ficheros wav mono a estereo duplicando la canal. Para ficheros estereo con sonido solo en el canal izquierdo, se duplica este canal para generar el nuevo fichero estereo.',
                             formatter_class=argparse.RawDescriptionHelpFormatter,
                             epilog=textwrap.dedent('''\
                                Ejemplo de uso:
                                    Para convertir todos los wav dentro de un path: 
                                                    wavmono2stereo -i "C:\\videos\\Viaje Alicante\\voz\\" 
                                    ''' ))
ap.add_argument('-h', '--help', action='help', help='Muestra esta información y termina la ejecución.')
ap.add_argument('-i', '--input', required=True, help='Path que contiene los wav que hay que convertir')
args = vars(ap.parse_args())



if args['input'] is not None:
    path = args['input']

chdir(path)

#Recuperamos los ficheros de la carpeta que cumplen el patron
lista_ficheros = glob.glob('*.wav')

if len(lista_ficheros) < 1:
    print('No hay  ficheros *.wav para convertir.')
else:
    #Recorremos el resto de ficheros 
    for file_name in lista_ficheros:
        print('Procesando el fichero:', file_name)
        mono_sound = AudioSegment.from_file(file_name, format='wav')
        print('     Número de canales:', mono_sound.channels)
        print('     Bits por Sample:', mono_sound.sample_width * 8)
        print('     Frame rate:', mono_sound.frame_rate)
        print('     Duración (segundos):', mono_sound.duration_seconds)
        print(' ')

        if mono_sound.channels == 1:
            print('Duplicamos el canal mono para generar el stereo')
            stereo_sound = AudioSegment.from_mono_audiosegments(mono_sound, mono_sound)
        else:
            print('Como ya es estereo, duplicamos el canal izquierdo y descartamos el derecho, para generar el nuevo estereo')
            real_mono_sound = mono_sound.split_to_mono()[0]
            stereo_sound = AudioSegment.from_mono_audiosegments(real_mono_sound, real_mono_sound)
        new_file_name = path + '\\stereo_'+file_name
        stereo_sound.export(new_file_name, format='wav')
        print('Se ha generado el fichero',new_file_name)
        print(' - - - - - - - - - - - - - ')
print(' ')
print('Proceso finalizado!')