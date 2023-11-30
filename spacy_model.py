import spacy
from spacy_entityruler import *
import json

# teams_pattern = ['AC Milan', 'Milan', 'ACF Fiorentina', 'Fiorentina', 'AS Roma', 'Roma', 'Atalanta BC', 
#          'Atalanta', 'Bologna FC 1909', 'Bologna FC', 'Bologna', 'FC Internazionale Milano', 
#          'Internazionale', 'Inter', 'Juventus FC', 'Juventus', 'Juve', 'SS Lazio', 'Lazio', 'SSC Napoli', 'Napoli', 
#          'Udinese Calcio', 'Udinese', 'Empoli FC', 'Empoli', 'Hellas Verona FC', 
#          'Hellas', 'US Salernitana 1919', 'US Salernitana', 'Salernitana', 'US Cremonese', 'Cremonese', 
#          'US Sassuolo Calcio', 'Sassuolo', 'Spezia Calcio', 'Spezia', 'UC Sampdoria', 'Sampdoria', 
#          'Torino FC', 'Torino', 'US Lecce', 'Lecce', 'AC Monza', 'Monza']

def model_creation():
    # nlp = spacy.load('it_core_news_lg')
    nlp = spacy.blank('it')
    team_names = json.load(open('data/teams_data.json'))['teams']
    add_labeled_entity_ruler_to_spacy_model(nlp, adjust_team_names_for_entity_ruler(team_names), 'TEAM')
    entity_ruler = nlp.get_pipe('entity_ruler')
    pattern_money = [  
    {'label': 'MONEY', 'pattern': [{'IS_DIGIT':1},{'lemma':'milione'}]}, 
    {'label': 'MONEY', 'pattern': [{'IS_DIGIT':1},{'lemma':'milione'},{'POS':'ADP'},{'lower':'euro'}]},
    {'label': 'MONEY', 'pattern': [{'IS_DIGIT':1},{'lemma':'milione'},{'POS':'ADP'},{'lower':'dollari'}]},
    {'label': 'MONEY', 'pattern': [{'IS_DIGIT':1},{'lemma':'milione'},{'ORTH':'€'}]},
    {'label': 'MONEY', 'pattern': [{'IS_DIGIT':1},{'lemma':'milione'},{'ORTH':'$'}]},
    {'label': 'MONEY', 'pattern': [{'IS_DIGIT':1},{'lemma':'milione'},{'POS':'ADP'},{'lower':'euro'}]},
    {'label': 'MONEY', 'pattern': [{'IS_DIGIT':1},{'lemma':'milione'},{'POS':'ADP'},{'lower':'dollari'}]},
    {'label': 'MONEY', 'pattern': [{'IS_DIGIT':1},{'lemma':'mila'},{'ORTH':'€'}]},
    {'label': 'MONEY', 'pattern': [{'IS_DIGIT':1},{'lemma':'mila'},{'ORTH':'$'}]},
    {'label': 'MONEY', 'pattern': [{'IS_DIGIT':1},{'lower':'mln'}]},
    {'label': 'MONEY', 'pattern': [{'IS_DIGIT':1},{'lemma':'mln'},{'ORTH':'€'}]},
    {'label': 'MONEY', 'pattern': [{'IS_DIGIT':1},{'lemma':'mln'},{'ORTH':'$'}]}]
    pattern_sponsor = [
        {'label': 'SPONSOR', 'pattern': [{'LOWER': 'sponsor'},{'POS': 'NOUN'}]},
        {'label': 'SPONSOR', 'pattern': [{'POS': 'NOUN'},{'LOWER': 'sponsor'}]},
        {'label': 'SPONSOR', 'pattern': [{'LOWER': 'sponsor'},{'POS': 'ADJ'}]},
        {'label': 'SPONSOR', 'pattern': [{'LOWER': 'sponsorizzazione'}]}
    ]

    entity_ruler.add_patterns(pattern_money)
    entity_ruler.add_patterns(pattern_sponsor)
    return nlp

def predict(input):
    nlp = model_creation()
    doc = nlp(input['string'])
    result = {}
    i = 1
    for sent in doc.sents:
        if any(ent.label_ == 'SPONSOR' for ent in sent.ents) & any(ent.label_ == 'MONEY' for ent in sent.ents):
            result_sent = {}
            for ent in sent.ents:
                result_sent[ent.label_] = ent.text
            result[f'sent_{i}'] = result_sent
            i += 1
    return result

