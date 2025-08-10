```bash
python3.11 -m venv venv_spam_classifier
source venv_spam_classifier/bin/activate


deactivate
```

## Setup
```bash
export PIP_INDEX_URL=https://pypi.org/simple
pip install google-api-python-client google-auth-httplib2 google-auth-oauthlib spacy
python -m spacy download en_core_web_sm
```

## Run
```bash
(venv_spam_classifier) {16:32}~/Documents/my-projects/prototypes/spam-classifier-using-probability:main ✗ ➭ python main_v2.py
> Testing 1146 emails. model: NaiveBayes(cat_counts=Counter({'ham': 3510, 'spam': 1072}), word_counts=[('ham', 18366), ('spam', 12605)], vocab=25559, total_docs=4582, total_words=601550)
> Correct Spam: 294, Total Spam: 296
> Accuracy Spam: 0.9932432432432432
> Correct Ham: 833, Total Ham: 850
> Accuracy Ham: 0.98
```
