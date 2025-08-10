```bash
python3.11 -m venv venv_spam_classifier
source venv_spam_classifier/bin/activate


deactivate
```

## Setup
```bash
export PIP_INDEX_URL=https://pypi.org/simple
pip install -r requirements.txt
# For building a nlp stemmer, basically part of nlp_utils.py
python -m spacy download en_core_web_sm
```

## Run
Run the main_v2.py file to build the model and test it on emails.csv dataset from kaggle
Run the main.py file to build the model and test it on gmail client
```bash
(venv_spam_classifier) {16:32}~/Documents/my-projects/prototypes/spam-classifier-using-probability:main ✗ ➭ python main_v2.py
> Testing 1146 emails. model: NaiveBayes(cat_counts=Counter({'ham': 3510, 'spam': 1072}), word_counts=[('ham', 18366), ('spam', 12605)], vocab=25559, total_docs=4582, total_words=601550)
> Correct Spam: 294, Total Spam: 296
> Accuracy Spam: 0.9932432432432432
> Correct Ham: 833, Total Ham: 850
> Accuracy Ham: 0.98
```
