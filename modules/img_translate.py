import os

from google.cloud import translate_v3beta1 as translate
from google.cloud import vision
from langdetect import detect, LangDetectException


# file = 'input.jpg'
# target_language_code = 'en'


def pic_to_text(infile: str, target_language_code) -> dict:
    """Detects text in an image file

    Args:
    infile: path to image file

    Returns:
    dict withe all needed info (text, font_size, language_code, start_paragraphs)
    """
    os.environ["GOOGLE_APPLICATION_CREDENTIALS"] = 'img-translate-397007-286075ddcaa5.json'
    # Instantiates a client
    client = vision.ImageAnnotatorClient()

    # Opens the input image file
    with open(infile, "rb") as image_file:
        content = image_file.read()

    image = vision.Image(content=content)

    # For dense text, use document_text_detection
    # For less dense text, use text_detection
    response = client.document_text_detection(image=image)
    text = response.full_text_annotation.text

    word_bounding_box = response.full_text_annotation.pages[0].blocks[0].paragraphs[0].words[0].bounding_box
    font_size = word_bounding_box.vertices[-1].y - int(word_bounding_box.vertices[0].y)
    language_code = response.full_text_annotation.pages[0].property.detected_languages[0].language_code

    paragraphs = response.full_text_annotation.pages[0].blocks[0].paragraphs[0]
    start_paragraphs = paragraphs.bounding_box.vertices[0]

    if language_code == target_language_code:
        parts = text.split('\n')
        filtered_parts = []

        for part in parts:
            try:
                if part and detect(part) != 'en':
                    filtered_parts.append(detect(part))
            except LangDetectException:
                continue
        language_code = max(filtered_parts, key=filtered_parts.count)

    return {'text': text, 'font_size': font_size, 'language_code': language_code, 'start_paragraphs': start_paragraphs}


def translate_text(
        text: str,
        source_language_code: str,
        target_language_code: str,
        project_id: str,
) -> str:
    """Translates text to a given language using a glossary

    Args:
    text: String of text to translate
    source_language_code: language of input text
    target_language_code: language of output text
    project_id: GCP project id

    Return:
    String of translated text
    """

    # Instantiates a client
    client = translate.TranslationServiceClient()

    parent = project_id

    result = client.translate_text(
        request={
            "parent": parent,
            "contents": [text],
            "mime_type": "text/plain",  # mime types: text/plain, text/html
            "source_language_code": source_language_code,  # , 'en'),
            "target_language_code": target_language_code,
        }
    )

    return result.translations[0].translated_text


def get_translated_text_on_pic(file, project_id, target_language_code):
    """This method is called when the tutorial is run in the Google Cloud
    Translation API. It creates a glossary, translates text to
    French, and speaks the translated text.

    Args:
    None

    Returns:
    None
    """
    # Photo from which to extract text
    infile = file

    # photo -> detected text
    text_on_pic = pic_to_text(infile, target_language_code)

    # detected text -> translated text
    result_text = translate_text(
        ' '.join(text_on_pic.get('text').split('\n')), text_on_pic.get('language_code'),
        target_language_code=target_language_code,
        project_id=f'projects/{project_id}'
    )
    # result_text = translate_text(
    #     text_on_pic.get('text'), text_on_pic.get('language_code'), "ru",
    # )

    return result_text


def save_txt(filename, text):
    filename = filename.split('.')
    with open(f'{filename[0]}-EN.txt', 'w') as file:
        file.write(text)


if __name__ == '__main__':
    destination_path = '../Output'
    PROJECT_ID = 'img-translate-397007'
    target_language_code = 'en'
    folder_path = '../Input'
    for filename in os.listdir(folder_path):
        file_path = os.path.join(folder_path, filename)
        if os.path.isfile(file_path):
            filename_format = filename.split('.')[1]
            if filename_format in ('png', 'jpg', 'jpeg'):
                save_txt(filename,
                         # destination_path,
                         get_translated_text_on_pic(file=filename,
                                                    project_id=PROJECT_ID,
                                                    target_language_code=target_language_code))

            else:
                print('Not supported format file')
