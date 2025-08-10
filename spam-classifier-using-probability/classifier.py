import math, collections, os, json, heapq

class NaiveBayes:
    def __init__(self, cat_counts=None, word_counts=None, vocab=None, total_docs=0, total_words=0): 
        self.cat_counts = collections.Counter(cat_counts) if cat_counts else collections.Counter()
        self.word_counts = collections.defaultdict(collections.Counter, word_counts) if word_counts else collections.defaultdict(collections.Counter)
        self.vocab = set(vocab) if vocab else set()
        self.total_docs=total_docs
        self.total_words=total_words
    
    def __str__(self) -> str:
        return f"NaiveBayes(cat_counts={self.cat_counts}, \
        word_counts={[(k, len(v)) for k, v in self.word_counts.items()]}, \
        vocab={len(self.vocab)}, total_docs={self.total_docs}, total_words={self.total_words})"

    def train(self, docs):
        for words, cat in docs: 
            self.cat_counts[cat]+=1
            self.total_docs+=1
            self.total_words+=len(words)
            for w in words:
                self.word_counts[cat][w]+=1
                self.vocab.add(w)
        self.dump_model_in_json_file()
        
    def dump_model_in_json_file(self):
        import json
        with open('model.json', 'w') as f:
            json.dump({
                'cat_counts': self.cat_counts,
                'word_counts': self.word_counts,
                'vocab': list(self.vocab),
                'total_docs': self.total_docs,
                'total_words': self.total_words
            }, f)
       
    def predict(self, words):
        best, best_score = None, -1e99
        V = len(self.vocab)
        for c, cnt in self.cat_counts.items():
            log_prob = math.log(cnt/self.total_docs) # probability of category, i.e number of docs in category / total number of docs
            total_words_in_cat = sum(self.word_counts[c].values())
            for w in words:
                wc = self.word_counts[c].get(w, 0)
                """
                what if our test document contains a word we never saw in training for that category?
                wc=0, i.e P(w∣c)=0, math.log(0) = -inf
                Laplace smoothing: Pretend we’ve seen every possible word at least once in each category. 
                Its an approximation, but it helps avoid zero probabilities.
                """
                log_prob += math.log((wc+1)/(total_words_in_cat+V)) # add 1 to wc and V to total_words_in_cat to avoid zero probability
            if log_prob>best_score:
                best, best_score = c, log_prob
        return best

def get_model():
    if os.path.exists('model.json'):
        with open('model.json', 'r') as f:
            data = json.load(f)
            nb=NaiveBayes(
              cat_counts=data['cat_counts'],
              word_counts=data['word_counts'],
              vocab=set(data['vocab']),
              total_docs=data['total_docs'],
              total_words=data['total_words']
            )
            return nb
    return None

if __name__ == '__main__':
    nb = get_model()
    if nb:
        # print most frequent words in each category using max heap
        for cat, word_counts in nb.word_counts.items():
            heap = []
            for word, count in word_counts.items():
                if len(heap)<5:
                    heapq.heappush(heap, (count, word))
                else:
                    if count>heap[0][0]:
                        heapq.heappop(heap)
                        heapq.heappush(heap, (count, word))
            print(f"Most frequent words in {cat}: {heap}")
        
        sent_to_predict = [
          'Final call to claim your GGU MBA scholarship',
          'New device added to account',
          'Kotak Fund Transfer Transaction',
          'Last chance to share your thoughts & win a creator pack',
          'One Time Password',
          'Cash withdrawal- Successful',
          'Security alert',
          'Someone added you as their recovery email',
          'IMPS Transaction - Success'
        ] 
        for words in sent_to_predict:
            print(f"For words: {words}, Category: {nb.predict(words.split())}")