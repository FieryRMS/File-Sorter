from defusedxml import ElementTree
from pathlib import Path
from subprocess import run  #nosec
ui_dir = "ui/"
output_dir = "src/builds/"

InputFiles = Path(ui_dir).glob('*.[uq][ir]*')
for InputFile in InputFiles:
    OutputFileName=""
    if(str(InputFile).endswith('.ui')):
        ClassName = ElementTree.parse(InputFile).getroot()[0].text
        OutputFileName = "ui_" + ClassName.lower() + ".py"
        run(["pyuic5", '-x', InputFile, "-o", output_dir+OutputFileName])
    elif(str(InputFile).endswith('.qrc')):
        OutputFileName=InputFile.name[:-4]+'_rc.py'
        run(["pyrcc5", InputFile, "-o", output_dir+OutputFileName])

    print(OutputFileName)
    
