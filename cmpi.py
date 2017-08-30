import subprocess 
import argparse
import re

def compare_images(ref_img, cmp_img, method = 'psnr'):
    p = subprocess.Popen(['ffmpeg.exe', '-loglevel', 'error', '-i', ref_img, '-i', cmp_img, '-filter_complex', '{}=stats_file=-'.format(method), '-f', 'null', '-'], stdout = subprocess.PIPE, stderr = subprocess.PIPE)
    p.wait()
    outs, _ = p.communicate()
    if method == 'ssim':
        return float(re.search(r'\bAll:(\d+(?:\.\d+)?)\s', outs.decode('utf-8')).group(0)[4:])
    elif method == 'psnr':
        return float(re.search(r'\bpsnr_avg:[-+]?[0-9]*\.?[0-9]+', outs.decode('utf-8')).group(0)[9:])
    else:
        raise Exception('RegExp to match "{}" value not implemented yet, sorry...'.format(method))

def get_args():
    parser = argparse.ArgumentParser(description = "С помощью ffmpeg рассчитывает ssim и psnr двух изображений") 
    requiredNamed = parser.add_argument_group('required named arguments')
    requiredNamed.add_argument("-ref", required = True, help = "Путь к файлу-образцу")
    requiredNamed.add_argument("-c", required = True, help = "Путь к файлу, что будет сравниваться с образцом")
    return parser.parse_args()

if __name__ == '__main__':
    args = vars(get_args())
    print('PSNR: {}\nSSIM: {}'.format(compare_images(args['ref'], args['c']), compare_images(args['ref'], args['c'], 'ssim')))