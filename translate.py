import os
import sys

from modules.img_translate import save_txt, get_translated_text_on_pic
from modules.pic_translate_selenium import PicGoogleTranslateParser
PROJECT_ID = 'img-translate-397007'


def main(folder_path):
    target_language_code = 'en'
    with PicGoogleTranslateParser() as placer:

        # file_path = os.path.join(folder_path, filename)
        filename = folder_path
        if os.path.isfile(filename):
            filename_format = filename.split('.')[-1]
            if filename_format in ('png', 'jpg', 'jpeg'):
                # Start translate picture to txt
                save_txt(filename,
                         # destination_path,
                         get_translated_text_on_pic(
                             file=filename,
                             project_id=PROJECT_ID,
                             target_language_code=target_language_code,
                         ))
                # Start translate picture to picture
                placer.placer_google_translate_parser(filename)

            else:
                print('Not supported format file')


if __name__ == "__main__":
    if len(sys.argv) != 2:
        print("Usage: python translate.py <file_path>")
        sys.exit(1)

    input_file = sys.argv[1]

    if not os.path.exists(input_file):
        print("The specified file does not exist.")
        sys.exit(1)

    main(input_file)
