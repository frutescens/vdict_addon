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

## Sources
- Basis for Beginnner Sample Deck: https://www.reddit.com/r/learnvietnamese/comments/b039ha/7700_word_vietnamese_anki_deck/
- Audio Files from Lightspeed Vietnamese TTS Python Library: https://huggingface.co/spaces/ntt123/Vietnam-female-voice-TTS 
(Note: Although Lightspeed Vietnamese TTS does use what is popularly known as 'Generative AI', the model it uses can be trained on a single computer with minimal environmental consequences.)