"""Quiet Queue: a local, review-only task sorter. Synthetic training data only."""
import json, re, time
from http.server import BaseHTTPRequestHandler, HTTPServer
from pathlib import Path
import numpy as np
from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.linear_model import LogisticRegression

EXAMPLES = {
 'Reply': ['reply to the club email','answer the invitation','respond to the organiser message','send a thank you reply','answer the question in the email','write back to the reading group','reply with a suitable date','respond to the request for feedback'],
 'Read': ['read the article about gardens','read the newsletter','review the document before the meeting','look through the book chapter','read the club notes','study the guide to local history','read the instructions carefully','review the essay draft'],
 'Arrange': ['arrange a meeting with the club','schedule a date for the visit','book a time for a call','set a reminder for the exhibition','organise next week calendar','choose a time for the group meeting','schedule the library visit','arrange a call with the organiser']}
VEC=TfidfVectorizer(ngram_range=(1,2), sublinear_tf=True)
texts=[t for group in EXAMPLES.values() for t in group]
labels=[label for label,group in EXAMPLES.items() for _ in group]
X=VEC.fit_transform(texts)
MODEL=LogisticRegression(C=12,random_state=7,max_iter=1000).fit(X,labels)

def sort_tasks(text):
    if not isinstance(text,str) or len(text)>12000: raise ValueError('Use at most 12,000 characters.')
    lines=[s.strip() for s in text.splitlines() if s.strip()]
    if len(lines)>60: raise ValueError('Use at most 60 tasks.')
    started=time.perf_counter()
    if not lines: return {'tasks':[], 'elapsed_ms':0}
    features=VEC.transform(lines)
    probs=MODEL.predict_proba(features)
    rows=[]
    for i,line in enumerate(lines):
        score=float(probs[i].max())
        suggestion=str(MODEL.classes_[int(probs[i].argmax())])
        if features[i].nnz==0 or score<0.57: suggestion='Review'
        duplicate=next((j+1 for j in range(i) if re.sub(r'\W+','',lines[j]).lower()==re.sub(r'\W+','',line).lower()),None)
        rows.append({'number':i+1,'text':line,'suggestion':suggestion,'possible_duplicate_of':duplicate})
    return {'tasks':rows,'elapsed_ms':round((time.perf_counter()-started)*1000,3)}

class Handler(BaseHTTPRequestHandler):
    def log_message(self,*_): pass
    def do_GET(self):
        if self.path!='/': self.send_error(404); return
        payload=Path(__file__).with_name('index.html').read_bytes()
        self.send_response(200); self.send_header('Content-Type','text/html; charset=utf-8'); self.end_headers(); self.wfile.write(payload)
    def do_POST(self):
        if self.path!='/sort': self.send_error(404); return
        origin=self.headers.get('Origin','')
        if origin and origin!='http://'+self.headers.get('Host',''): self.send_error(403); return
        try:
            size=int(self.headers.get('Content-Length','0'))
            if not 0<size<=50000: raise ValueError('Request too large or empty.')
            result=sort_tasks(json.loads(self.rfile.read(size)).get('text'))
            payload=json.dumps(result).encode()
            self.send_response(200); self.send_header('Content-Type','application/json'); self.end_headers(); self.wfile.write(payload)
        except (ValueError,TypeError,AttributeError): self.send_error(400,'Invalid task list')

if __name__=='__main__':
    print('Quiet Queue: http://127.0.0.1:8771',flush=True)
    HTTPServer(('127.0.0.1',8771),Handler).serve_forever()
