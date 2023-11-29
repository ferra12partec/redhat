import spacy

# teams_pattern = ['AC Milan', 'Milan', 'ACF Fiorentina', 'Fiorentina', 'AS Roma', 'Roma', 'Atalanta BC', 
#          'Atalanta', 'Bologna FC 1909', 'Bologna FC', 'Bologna', 'FC Internazionale Milano', 
#          'Internazionale', 'Inter', 'Juventus FC', 'Juventus', 'Juve', 'SS Lazio', 'Lazio', 'SSC Napoli', 'Napoli', 
#          'Udinese Calcio', 'Udinese', 'Empoli FC', 'Empoli', 'Hellas Verona FC', 
#          'Hellas', 'US Salernitana 1919', 'US Salernitana', 'Salernitana', 'US Cremonese', 'Cremonese', 
#          'US Sassuolo Calcio', 'Sassuolo', 'Spezia Calcio', 'Spezia', 'UC Sampdoria', 'Sampdoria', 
#          'Torino FC', 'Torino', 'US Lecce', 'Lecce', 'AC Monza', 'Monza']

nlp = spacy.load('model')

def predict(input):
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

print(predict({"string":"Il Manchester United ha annunciato un'estensione decennale della sponsorizzazione di Adidas che vale oltre 1 miliardo di euro"}))