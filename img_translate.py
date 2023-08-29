import os
from pathlib import Path

from google.cloud import translate_v3beta1 as translate
from google.cloud import vision

os.environ["GOOGLE_APPLICATION_CREDENTIALS"] = 'img-translate-397007-286075ddcaa5.json'
PROJECT_ID = 'img-translate-397007'
file = 'input.png'
target_language_code = 'ru'


def pic_to_text(infile: str) -> dict:
    """Detects text in an image file

    Args:
    infile: path to image file

    Returns:
    dict withe all needed info (text, font_size, language_code, start_paragraphs)
    """

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
    infile = f'images/{file}'

    # photo -> detected text
    text_on_pic = pic_to_text(infile)
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


def save_txt(text):
    if not os.path.exists('output'):
        os.makedirs('output')

    output = f'{Path.cwd()}/output'
    for f in os.listdir(output):
        os.remove(os.path.join(output, f))

    with open('output/output.txt', 'w') as file:
        file.write(text)


if __name__ == '__main__':
    print(get_translated_text_on_pic(file=file,
                                     project_id=PROJECT_ID,
                                     target_language_code=target_language_code))
    save_txt(get_translated_text_on_pic(file=file,
                                        project_id=PROJECT_ID,
                                        target_language_code=target_language_code))