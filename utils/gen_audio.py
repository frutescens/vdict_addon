import csv
from vieneu import Vieneu

vieneu = Vieneu() 

print("🔊 Generating speech...")

terms = []
with open('FILE_NAME.csv', mode='r', encoding='utf-8', newline='') as file:
    reader = csv.reader(file, delimiter='\t')
    for row in reader:
        terms.append(row[0])
speakers = {'southern':'Adam', 'central':'Quang Sơn', 'northern':'Phạm Tuyên'}
main_directory = "audio_packs/"
for t in terms:
    print(t)
    audio = vieneu.infer(t, voice=speakers['southern'])
    vieneu.save(audio, main_directory+"southern/"+t+".mp3")
    audio = vieneu.infer(t, voice=speakers['central'])
    vieneu.save(audio, main_directory+"central/"+t+".mp3")
    audio = vieneu.infer(t, voice=speakers['northern'])
    vieneu.save(audio, main_directory+"northern/"+t+".mp3")
    