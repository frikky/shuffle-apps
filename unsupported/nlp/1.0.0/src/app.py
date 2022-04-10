import asyncio
import json
import random
import socket
import time

import spacy
from cyberspacy import *
from spacy.lang.en import English
from walkoff_app_sdk.app_base import AppBase

class NLP(AppBase):
    __version__ = "1.0.0"
    app_name = "NLP"

    def __init__(self, redis, logger, console_logger=None):
        super().__init__(redis, logger, console_logger)
        self.nlp = spacy.load("en_core_web_lg")
        self.nlp.add_pipe(IPDetector(self.nlp))
        self.nlp.add_pipe(EmailDetector(self.nlp))
        self.nlp.add_pipe(URLDetector(self.nlp))

    def get_ipv4s(self, data):
        doc = self.nlp(data)
        resp = []
        if doc._.has_ipv4 == True:
            for i in doc._.ipv4:
                resp.append(i[1])
        return resp

    def get_urls(self, data):
        doc = self.nlp(data)
        resp = []
        if doc._.has_url == True:
            for i in doc._.url:
                resp.append(i[1])
        return resp

    def get_emails(self, data):
        doc = self.nlp(data)
        resp = []
        if doc._.has_email_addr == True:
            for i in doc._.email_addr:
                resp.append(i[1])
        return resp

    def get_entities(self, data):
        doc = self.nlp(data)
        resp = []
        for ent in doc.ents:
            if (ent.label_ == 'PERSON') or (ent.label_ == 'ORG'):
                resp.append({'ent':ent.text, 'label':ent.label_})
        return resp

    def get_content(self, data):
        import tika
        tika.initVM()
        try:
            parsed = tika.parser.from_file('/path/to/file')
            print(parsed["metadata"])
            return parsed["content"]
        except:
            return "Error parsing content"

    def extract(self, data, extract):
        switcher = {
            "get_ipv4s" : self.get_ipv4s,
            "get_urls" : self.get_urls,
            "get_emails" : self.get_emails,
            "get_entities" : self.get_entities,
        }

        func = switcher.get(extract, lambda: "Invalid extract")
        return func(data)

if __name__ == "__main__":
    NLP.run()
