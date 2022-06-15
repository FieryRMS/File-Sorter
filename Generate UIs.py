from xml.etree import ElementTree
from pathlib import Path
from subprocess import run
base_dir = "ui/"
output_dir = "src/"

InputFiles = Path(base_dir).glob('*.ui')
for InputFile in InputFiles:
    ClassName = ElementTree.parse(InputFile).getroot()[0].text
    OutputFileName = "ui_" + ClassName.lower() + ".py"
    print(OutputFileName)
    run(["pyuic5", '-x', InputFile, "-o", output_dir+OutputFileName])
