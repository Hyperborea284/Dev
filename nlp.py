from summarizer import Summarizer
from spacy import displacy
import spacy
from goose3 import Goose

@staticmethod
def url_extractor(url_article):
    g = Goose()
    article = g.extract(url_article)
    article_lang = article.meta_lang
    article_text = article.cleaned_text
    return article, article_lang, article_text

@staticmethod
def bert_sumarizar(texto):
    sumarizador = Summarizer()
    resumo = sumarizador(texto)
    return resumo

@staticmethod
def entities(texto,  lang_code):

    if lang_code == 'en':
        lang_code = 'english'
    elif lang_code == 'pt':
        # lang_code = 'portuguese'
        lang_code = 'pt_core_news_sm'
    else:
        pass

    ent_list = []
    pln = spacy.load(lang_code)
    documento = pln(texto)
    for entidade in documento.ents:
        ent_list.append([entidade.text, entidade.label_])

    return ent_list

#article, article_lang, article_text = url_extractor(url_port)
