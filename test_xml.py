import xml.etree.ElementTree as ET
tree = ET.parse(r".\res\adventure_data.xml")
root = tree.getroot()

# for child in root.iter("item"):
#     print(child.find("id").text)
#     print(child.find("word").text)

for child in root.iter("room"):
    print(child.find("id").text)
    try:
        print(child.find("description").text)
    except AttributeError:
        print("keine Beschreibung")

    for exits in child.iter('exit'):
        print(exits.attrib)
        print(exits.attrib['name'])

