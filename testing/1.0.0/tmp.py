import json
import re

# This whole thing should be recursive.
basejson = [{'highlight_ranges': {}, 'message': {'Alert': 'Account  Manipulation', '_id': 'd097c6f2-f6b6-11ea-aaa1-0050569f425d', 'timestamp': '2020-09-14T18:19:24.427Z'}, 'index': 'test', 'decoration_stats': None}, {'highlight_ranges': {}, 'message': {'Alert': 'Account  Manipulation', '_id': 'd099c2c3-f6b6-11ea-aaa1-0050569f425d', 'timestamp': '2020-09-14T18:19:24.427Z'}, 'index': 'test', 'decoration_stats': None}, {'highlight_ranges': {}, 'message': {'Alert': 'Account  Manipulation', '_id': 'd097c6f2-f6b6-11ea-aaa1-0050569f425d', 'timestamp': '2020-09-14T18:19:24.427Z'}, 'index': 'mitre_0', 'decoration_stats': None}, {'highlight_ranges': {}, 'message': {'Alert': 'Account  Manipulation', '_id': 'd099c2c3-f6b6-11ea-aaa1-0050569f425d', 'timestamp': '2020-09-14T18:19:24.427Z'}, 'index': 'mitre_0', 'decoration_stats': None}, {'highlight_ranges': {}, 'message': {'Alert': 'Notepad  connecting  to  the  internet', '_id': 'c789d084-f6b6-11ea-aaa1-0050569f425d', 'timestamp': '2020-09-14T18:19:09.444Z'}, 'index': '1_207', 'decoration_stats': None}, {'highlight_ranges': {}, 'message': {'Alert': 'Notepad  connecting  to  the  internet', '_id': 'c789d084-f6b6-11ea-aaa1-0050569f425d', 'timestamp': '2020-09-14T18:19:09.444Z'}, 'index': 'mitre_0', 'decoration_stats': None}, {'highlight_ranges': {}, 'message': {'Alert': 'Obfuscating  Hacking  Commands', '_id': 'ae8ad8f5-f6b5-11ea-aaa1-0050569f425d', 'timestamp': '2020-09-14T18:11:17.202Z'}, 'index': 'mitre_0', 'decoration_stats': None}, {'highlight_ranges': {}, 'message': {'Alert': 'Account  Manipulation', '_id': '0f9d3001-f6b3-11ea-aaa1-0050569f425d', 'timestamp': '2020-09-14T17:52:31.810Z'}, 'index': 'test_201', 'decoration_stats': None}, {'highlight_ranges': {}, 'message': {'Alert': 'Account  Manipulation', '_id': '0f9d3000-f6b3-11ea-aaa1-0050569f425d', 'timestamp': '2020-09-14T17:52:31.810Z'}, 'index': 'test_201', 'decoration_stats': None}, {'highlight_ranges': {}, 'message': {'Alert': 'Account  Manipulation', '_id': '0f9d3001-f6b3-11ea-aaa1-0050569f425d', 'timestamp': '2020-09-14T17:52:31.810Z'}, 'index': 'mitre_0', 'decoration_stats': None}, {'highlight_ranges': {}, 'message': {'Alert': 'Account  Manipulation', '_id': '0f9d3000-f6b3-11ea-aaa1-0050569f425d', 'timestamp': '2020-09-14T17:52:31.810Z'}, 'index': 'mitre_0', 'decoration_stats': None}]
#basejson = json.loads(baseresult)

#ACTUAL:  [('$Start_node.#.message', 'Start_node.', 'message')]
input_data = "$Start_node.#4:max.message.Alert"


def recurse_loop(basejson, parsersplit):
    #parsersplit = input_data.split(".")

    match = "#(\d+):?-?([0-9a-z]+)?#?"
    print("Split: %s\n%s" % (parsersplit, basejson))
    try:
        outercnt = 0
        for value in parsersplit:
            print("VALUE: %s\n" % value)
            actualitem = re.findall(match, value, re.MULTILINE)
            if value == "#":
                newvalue = []
                for innervalue in basejson:
                    # 1. Check the next item (message)
                    # 2. Call this function again

                    try:
                        ret = recurse_loop(innervalue, parsersplit[outercnt+1:])
                    except IndexError:
                        print("INDEXERROR: ", parsersplit[outercnt])
                        #ret = innervalue
                        ret = recurse_loop(innervalue, parsersplit[outercnt:])

                    print(ret)
                    #exit()
                    newvalue.append(ret)

                return newvalue
            elif len(actualitem) > 0:
                # FIXME: This is absolutely not perfect.
                print("IN HERE: ", actualitem)

                newvalue = []
                firstitem = actualitem[0][0]
                seconditem = actualitem[0][1]
                if seconditem == "":
                    print("In first")
                    basejson = basejson[int(firstitem)]
                else:
                    if seconditem == "max":
                        seconditem = len(basejson)
                    if seconditem == "min":
                        seconditem = 0

                    newvalue = []
                    for i in range(int(firstitem), int(seconditem)):
                        # 1. Check the next item (message)
                        # 2. Call this function again
                        print("Base: %s" % basejson[i])

                        try:
                            ret = recurse_loop(basejson[i], parsersplit[outercnt+1:])
                        except IndexError:
                            print("INDEXERROR: ", parsersplit[outercnt])
                            #ret = innervalue
                            ret = recurse_loop(innervalue, parsersplit[outercnt:])

                        print(ret)
                        #exit()
                        newvalue.append(ret)

                    return newvalue
            else:
                #print("BEFORE NORMAL VALUE: ", basejson, value)
                if len(value) == 0:
                    return basejson

                if isinstance(basejson[value], str):
                    print(f"LOADING STRING '%s' AS JSON" % basejson[value])
                    try:
                        basejson = json.loads(basejson[value])
                    except json.decoder.JSONDecodeError as e:
                        print("RETURNING BECAUSE '%s' IS A NORMAL STRING" % basejson[value])
                        return basejson[value]
                else:
                    basejson = basejson[value]

            outercnt += 1

    except KeyError as e:
        print("Lower keyerror: %s" % e)
        #return basejson
        #return "KeyError: Couldn't find key: %s" % e

    return basejson

ret = recurse_loop(basejson, input_data.split(".")[1:])
print(ret)



                # FIXME - not recursive - should go deeper if there are more #
                #print("HANDLE RECURSIVE LOOP OF %s" % basejson)
                #returnlist = []
                #try:
                #    for innervalue in basejson:
                #        print("Value: %s" % innervalue[parsersplit[cnt+1]])
                #        returnlist.append(innervalue[parsersplit[cnt+1]])
                #except IndexError as e:
                #    print("Indexerror inner: %s" % e)
                #    # Basically means its a normal list, not a crazy one :)
                #    # Custom format for ${name[0,1,2,...]}$
                #    indexvalue = "${NO_SPLITTER%s}$" % json.dumps(basejson)
                #    if len(returnlist) > 0:
                #        indexvalue = "${NO_SPLITTER%s}$" % json.dumps(returnlist)

                #    print("INDEXVAL: ", indexvalue)
                #    return indexvalue
                #except TypeError as e:
                #    print("TypeError inner: %s" % e)

                ## Example format: ${[]}$
                #parseditem = "${%s%s}$" % (parsersplit[cnt+1], json.dumps(returnlist))
                #print("PARSED LOOP ITEM: %s" % parseditem)

                ## FIXME: Always only does one iter here :(
                #return parseditem
