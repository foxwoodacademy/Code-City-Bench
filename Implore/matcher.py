import sqlite3
import math
from collections import Counter

class SimpleSemanticMatcher:
    def __init__(self):
        self.conn = sqlite3.connect(':memory:')
        self.cursor = self.conn.cursor()
        self.cursor.execute('CREATE TABLE grants (id TEXT, title TEXT, region TEXT)')

    def add_grant(self, id, title, region='federal'):
        self.cursor.execute('INSERT INTO grants VALUES (?, ?, ?)', (id, title, region))

    def get_candidate_grants(self, target_region=None):
        query = 'SELECT id, title FROM grants'
        params = []
        if target_region and target_region != 'federal':
            query += ' WHERE region = ?'
            params.append(target_region)
        self.cursor.execute(query, params)
        return self.cursor.fetchall()

    def _tfidf(self, doc, corpus):
        # Extremely lightweight pure-python TF-IDF
        words = doc.lower().split()
        word_counts = Counter(words)
        
        # Calculate IDF
        idf = {}
        total_docs = len(corpus)
        all_words = set(word for doc in corpus for word in doc.lower().split())
        for word in all_words:
            count = sum(1 for doc in corpus if word in doc.lower().split())
            idf[word] = math.log(total_docs / (1 + count))
            
        # Calculate TF-IDF
        tfidf = {word: word_counts[word] * idf.get(word, 0) for word in words}
        return tfidf

    def find_best_match(self, project_summary, target_region=None):
        grants = self.get_candidate_grants(target_region=target_region)
        if not grants:
            return None
            
        titles = [grant[1] for grant in grants]
        
        # Calculate similarity (simple overlapping sum of TF-IDF scores)
        project_tfidf = self._tfidf(project_summary, titles)
        
        best_match = None
        best_score = -1
        
        for id, title in grants:
            title_tfidf = self._tfidf(title, titles)
            # Similarity measure
            score = sum(project_tfidf.get(word, 0) * title_tfidf.get(word, 0) for word in project_tfidf)
            if score > best_score:
                best_score = score
                best_match = id
                
        return best_match
