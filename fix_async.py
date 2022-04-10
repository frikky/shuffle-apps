import os

basedir = "."
folders = os.listdir(basedir)
for folder in folders:
    try:
        subfolders = os.listdir(f"{basedir}/{folder}")
    except:
        continue

    for subfolder in subfolders:
        filename = f"{basedir}/{folder}/{subfolder}/src/app.py"
        data = ""

        try:
            with open(f"{filename}", "r") as tmp:
                data = tmp.read()
                data = data.replace("async def", "def", -1)
                data = data.replace("await ", "", -1)
                data = data.replace("asyncio.run(", "", -1)
                data = data.replace(", debug=True)", "", -1)
                data = data.replace(", debug=False)", "", -1)
                data = data.replace(",debug=True)", "", -1)
                data = data.replace(",debug=False)", "", -1)

            if len(data) > 0:
                with open(f"{filename}", "w+") as tmp:
                    tmp.write(data)

            print("Fixed: %s" % filename)
        except:
            print("Skipped: %s" % filename)


    #break
