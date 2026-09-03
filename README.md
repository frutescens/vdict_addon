# VDict Assistant Addon
VDict Assistant Addon helps learners create immersive, memorable flashcards with information from VDict.com, a French-English-Vietnamese dictionary. As learners develop their Vietnamese and grow more confident in their knowledge, they can incorporate more and more Vietnamese in their learning progress. 

## Instructions
### For Singular Cards
1. Right click on the 'Expression' field of a card and select 'VDict Card Generation'

### For Multiple Cards
1. Create a deck with these fields: 'Expression', 'Meaning', 'VMeaning', 'Synonyms', 'Notes', 'Visual Media', 'Audio' (or their equivalents)
2. Set the "target_deck_name" field with the target deck. In addition, you can change "addon_native_language" to either 'FRENCH' or 'ENGLISH' to get definitions in the specified language. 
3. Go to Tools > VDictGenerator and select the option that best suits your need.

Please note that there will be a two second delay per query to not overwhelm VDict Servers

## Deck Information
Learners can change the note type of the provided sample decks to increase or decrease the challenge provided by cards. 
### Audio Files
Sample decks can use audio files of Northern, Central, and Southern speakers. Go to sampples/audio_packs and download the compressed .zip file of your choosing. After unzipping it, drag the contents into your Anki's collection.media folder. If you wish to generate other audio files, please take a look at utils/audio_gen.py.
### Beginner Deck
Learners focus on linking EN/FR definitions to the expression and improving their spelling abilities. 
The Vietnamese meaning and synonyms of the studied expression are hidden by default and can be revealed by the learner.   
- Meaning: Vietnamese Expression + Visual --> EN/FR Meaning + Usage
- Sound (Typing): Audio + Visual --> Expression
- Identity (Typing): EN/FR Meaning + Visual --> Vietnamese Expression 
### Intermediate Deck
The EN/FR defintions are still available, but now learners can now choose to use the Vietnamese definitions to learn new expressions. Example translations are now spoilered. Learners can choose to reveal the EN/FR definition or the Vietnamese definitions.
- Meaning: Vietnamese Expression + Visual --> Viet Meaning + Usage
- Identity (Typing): EN/FR/VT Meaning + Visual --> Vietnamese Expression
### Advanced Deck
Learners are now expected to use only Vietnamese to learn new expressions. Non-'Usage' EN/FR hidden by default.
- Meaning: Vietnamese Expression + Visual -> Viet Meaning
- Identity (Typing): VT Meaning + Synonyms + Visual --> Vietnamese Expression

## To-Do
- Write HTML for Intermediate/Advanced Cards
- Incorporate Sino-Vietnamese characters into cards. 
- Improve audio_gen.py and provide better instructions for its usage. 

## Sources
- Basis for Beginnner Sample Deck: https://www.reddit.com/r/learnvietnamese/comments/b039ha/7700_word_vietnamese_anki_deck/
- Audio files generated with VieNeu-TTS: https://github.com/pnnbao97/VieNeu-TTS/tree/main 

@misc{vieneutts2026,
  title        = {VieNeu-TTS-v2: Advanced Vietnamese Text-to-Speech with Podcast and Code-Switching Support},
  author       = {Pham Nguyen Ngoc Bao},
  year         = {2026},
  publisher    = {Hugging Face},
  howpublished = {\url{https://huggingface.co/pnnbao-ump/VieNeu-TTS}}
}