import spacy

# teams_pattern = ['AC Milan', 'Milan', 'ACF Fiorentina', 'Fiorentina', 'AS Roma', 'Roma', 'Atalanta BC', 
#          'Atalanta', 'Bologna FC 1909', 'Bologna FC', 'Bologna', 'FC Internazionale Milano', 
#          'Internazionale', 'Inter', 'Juventus FC', 'Juventus', 'Juve', 'SS Lazio', 'Lazio', 'SSC Napoli', 'Napoli', 
#          'Udinese Calcio', 'Udinese', 'Empoli FC', 'Empoli', 'Hellas Verona FC', 
#          'Hellas', 'US Salernitana 1919', 'US Salernitana', 'Salernitana', 'US Cremonese', 'Cremonese', 
#          'US Sassuolo Calcio', 'Sassuolo', 'Spezia Calcio', 'Spezia', 'UC Sampdoria', 'Sampdoria', 
#          'Torino FC', 'Torino', 'US Lecce', 'Lecce', 'AC Monza', 'Monza']

# nlp = spacy.load('it_core_news_sm')

def adjust_team_names_for_entity_ruler(team_names):
    '''
    Ripulisce i nomi delle squadre per l'entità TEAM creando alternative valide per identificare il nome della squadra.
    Params:
        team_names[list]: lista di nomi delle squadre
    Return:
        pattern_list[list]: lista di nomi delle squadre pronte per spacy
    '''
    pattern_list = list()
    for name in team_names:
        ents = name.split(' ')
        pattern_list.append(name)
        if len(ents) <= 2:
            if 'Calcio' in ents:
                ents.remove('Calcio')
            longest_word = max(ents, key=len)
            
            if longest_word not in pattern_list:
                pattern_list.append(longest_word)
        else:
            cleaned_ents = [ent for ent in ents if not ent.isdigit()]
            cleaned_name = ' '.join(cleaned_ents)
            if cleaned_name not in pattern_list:
                pattern_list.append(cleaned_name)
            longest_word = max(ents, key=len)
            if longest_word not in pattern_list:
                pattern_list.append(longest_word)
    return pattern_list

def add_labeled_entity_ruler_to_spacy_model(nlp, starting_patterns, label):
    '''
    Aggiunge l'entità TEAM al modello Spacy partendo da una lista di pattern.
    Params:
        nlp[spacy.model]: spacy modello a cui aggiungere l'entità TEAM
        teams_pattern[list]: lista di pattern da cui generare l'entità TEAM. 
        label[str]: etichetta dell'entità
    Return:
        None
    '''
    ruler = None 
    try:              
        ruler = nlp.get_pipe('entity_ruler')
    except KeyError:
        ruler = nlp.add_pipe('entity_ruler', before='ner')
    patterns = []
    for item in starting_patterns:
        patterns.append({"label": label, 'pattern': [{'ORTH':item}]})
    ruler.add_patterns(patterns)
    return 

