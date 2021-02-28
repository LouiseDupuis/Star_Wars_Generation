

# transforming the data (text files) into a dataframe of training example
import pandas as pd
import re
from sklearn.model_selection import train_test_split
import random

"""
import nlpaug.augmenter.char as nac
import nlpaug.augmenter.word as naw
import nlpaug.augmenter.sentence as nas
import nlpaug.flow as nafc

from nlpaug.util import Action
"""
from googletrans import Translator

from google_trans_new import google_translator

random.seed(42)

def extract_paragraphs(file_path):
    """
    This function separates a file into paragraphs defined by the delimitations of a
    :param file_path:
    :return:
    """
    paragraphs = []
    current_paragraph = ''
    file1 = open(file_path, 'r',encoding='latin-1')
    flag = True
    while flag:
        new_line = file1.readline()
        if not new_line == '\n':
            new_line = re.sub(r"Ò", " ", new_line)  #enlever caractères spéciaux
            new_line = re.sub(r"â", "'", new_line)  # enlever caractères spéciaux
            current_paragraph += new_line
        else:
            if random.randint(0, 30) == 15:
                paragraphs += [ current_paragraph]
                current_paragraph = ''
        if new_line == '':
            flag = False
    return paragraphs



def data_augmentation(paragraphs):

    print(paragraphs[0])
    #translator = Translator(service_urls=['https://translation.googleapis.com'])
    translator = google_translator()

    back_translations = []

    def translation(paragraph, src, dest):
        """ recursive translation function to avoid hitting the API's 5000 character limit"""

        """ line by line translation to keep the structure of the document """

        lines = paragraph.split('\n')
        trans_result = ''

        for line in lines:
            if len(line) >= 4000 : # the limit for traduction with google's api is 5000 characters
                    par_1 = line[0:len(line)//2]
                    par_2 = line[ len(line) // 2 if len(line)%2 == 0 else len(line) //2 + 1 : ]
                    trans = translation(par_1, src, dest) + translation(par_2, src, dest)
            else:
                    trans = translator.translate(line, lang_src= src, lang_tgt= dest)
            trans_result += trans + '\n'

        return trans_result


    def back_to_back_translation(paragraph):

        en_to_other_translation = translation(paragraph, 'en', 'fr')
        back_translation = translation(en_to_other_translation, 'fr', 'en')
        return back_translation


    for paragraph in paragraphs:

        back_translation = back_to_back_translation(paragraph)

        back_translations += [back_translation]

    """translations = [ translator.translate(par, lang_src='en', lang_tgt='fr') for par in paragraphs]
    print(translations)

    back_translations = [ translator.translate(trans, lang_src='fr', lang_tgt='en') for trans in translations]
    print(back_translations)"""
        
    return back_translations



def df_to_txt(df, filepath):
    text_file = open(filepath, 'w', encoding='utf-8')
    data = ''
    for p in df:
        p = str(p)
        data += p + '\n'
        data.encode('utf-8')
    text_file.write(data)
    return None




paragraphs = extract_paragraphs('StarWars_EpisodeIV_script.txt')
paragraphs += extract_paragraphs('StarWars_EpisodeVI_script.txt')
paragraphs += extract_paragraphs('StarWars_EpisodeV_script.txt')

paragraphs += extract_paragraphs('StarWars-EpisodeI_script.txt')
paragraphs += extract_paragraphs('StarWars_EpisodeII_script.txt')
paragraphs += extract_paragraphs('StarWars_EpisodeIII_script.txt')

paragraphs += extract_paragraphs('StarWars_EpisodeVII_script.txt')
paragraphs += extract_paragraphs('StarWars_EpisodeVIII_script.txt')
paragraphs += extract_paragraphs('StarWars_EpisodeIX_script.txt')

print(len(paragraphs))

train_test_ratio = 0.9
train_valid_ratio = 0.9
df_full_train, df_test = train_test_split(paragraphs, train_size = train_test_ratio, random_state = 1)
df_train, df_valid = train_test_split(df_full_train, train_size = train_valid_ratio, random_state = 1)

print(len(df_train), len(df_valid), len(df_test))

test_data = [df_train[18][:1000]]


new_train_data = data_augmentation(test_data)
print(new_train_data[0])

print()

test_data = [df_train[2][:1000]]


new_train_data = data_augmentation(test_data)
print(new_train_data[0])





#df_to_txt(new_train_data, 'star_wars_trans_train.txt')


"""df_to_txt(df_train, 'star_wars_train.txt')
df_to_txt(df_valid, 'star_wars_valid.txt')
df_to_txt(df_test, 'star_wars_test.txt')
df_to_txt(df_full_train, 'star_wars_full_train.txt')"""
















