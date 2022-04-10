import asyncio
import getopt
import json
import random
import socket
import sys
import time
from operator import itemgetter
from shutil import copyfile

import classification_tools as clt
import classification_tools.postprocessing as pop
import classification_tools.preprocessing as prp
import classification_tools.save_results as sr
import joblib
from colorama import Back
from colorama import Fore
from colorama import init
from colorama import Style
from walkoff_app_sdk.app_base import AppBase

# 1. Generate the api.yaml based on downloaded files
# 2. Add a way to choose the rule and the target platform for it
# 3. Add the possibility of translating rules back and forth

# 4. Make it so you can start with Mitre Att&ck techniques
# and automatically get the right rules set up with your tools :O
class rcATT(AppBase):
    __version__ = "1.0.0"
    app_name = "attack-predictor"  # this needs to match "name" in api.yaml

    def __init__(self, redis, logger, console_logger=None):
        """
        Each app should have this __init__ to set up Redis and logging.
        :param redis:
        :param logger:
        :param console_logger:
        """
        super().__init__(redis, logger, console_logger)


    def save_stix_file(report, title, date, ttps, output_file):
        """
        Save prediction in a JSON file under STIX format
        """
        if(date == ''):
                date = "1970-01-01"
        references = []
        for key in ttps:
                if key in clt.ALL_TTPS:
                        references.append(clt.STIX_IDENTIFIERS[clt.ALL_TTPS.index(key)])
        file_to_save = sr.save_results_in_file(report, title, date, references)
        copyfile(file_to_save, output_file)


        report_to_predict = ""

    def get_prediction(self, data):
        report_to_predict = prp.remove_u(data)

        # load postprocessingand min-max confidence score for both tactics and techniques predictions
        parameters = joblib.load("classification_tools/data/configuration.joblib")
        min_prob_tactics = parameters[2][0]
        max_prob_tactics = parameters[2][1]
        min_prob_techniques = parameters[3][0]
        max_prob_techniques = parameters[3][1]

        pred_tactics, predprob_tactics, pred_techniques, predprob_techniques = clt.predict(report_to_predict, parameters)

        # change decision value into confidence score to display
        for i in range(len(predprob_tactics[0])):
            conf = (predprob_tactics[0][i] - min_prob_tactics) / (max_prob_tactics - min_prob_tactics)
            if conf < 0:
                conf = 0.0
            elif conf > 1:
                conf = 1.0
                predprob_tactics[0][i] = conf*100
        for j in range(len(predprob_techniques[0])):
            conf = (predprob_techniques[0][j] - min_prob_techniques) / (max_prob_techniques - min_prob_techniques)
            if conf < 0:
                conf = 0.0
            elif conf > 1:
                conf = 1.0
                predprob_techniques[0][j] = conf*100

        #prepare results to display
        ttps = []
        to_print_tactics = []
        to_print_techniques = []
        for ta in range(len(pred_tactics[0])):
            if pred_tactics[0][ta] == 1:
                ttps.append(clt.CODE_TACTICS[ta])
                to_print_tactics.append([1, clt.NAME_TACTICS[ta], predprob_tactics[0][ta]])
            else:
                to_print_tactics.append([0, clt.NAME_TACTICS[ta], predprob_tactics[0][ta]])
        for te in range(len(pred_techniques[0])):
            if pred_techniques[0][te] == 1:
                ttps.append(clt.CODE_TECHNIQUES[te])
                to_print_techniques.append([1, clt.NAME_TECHNIQUES[te], predprob_techniques[0][te]])
            else:
                to_print_techniques.append([0, clt.NAME_TECHNIQUES[te], predprob_techniques[0][te]])
        to_print_tactics = sorted(to_print_tactics, key = itemgetter(2), reverse = True)
        to_print_techniques = sorted(to_print_techniques, key = itemgetter(2), reverse = True)
        print("Predictions for the given report are : ")
        print("Tactics :")
        for tpta in to_print_tactics:
            if tpta[0] == 1:
                print(Fore.YELLOW + '' + tpta[1] + " : " + str(tpta[2]) + "% confidence")
            else:
                print(Fore.CYAN + '' + tpta[1] + " : " + str(tpta[2]) + "% confidence")
        print(Style.RESET_ALL)
        print("Techniques :")
        for tpte in to_print_techniques:
            if tpte[0] == 1:
                print(Fore.YELLOW + '' + tpte[1] + " : "+str(tpte[2])+"% confidence")
            else:
                print(Fore.CYAN + '' + tpte[1] + " : "+str(tpte[2])+"% confidence")
        print(Style.RESET_ALL)
        #if output_file != '':
        #    save_stix_file(report_to_predict, title, date, ttps, output_file)
        #    print("Results saved in " + output_file)

        return ttps


    # Write your data inside this function
    def predict_file_content(self, file_id):
        file_data = self.get_file(file_id)

        prediction = self.get_prediction(file_data["data"])
        return prediction

    # Write your data inside this function
    def predict(self, data):
        prediction = self.get_prediction(data)
        return prediction

if __name__ == "__main__":
    rcATT.run()
