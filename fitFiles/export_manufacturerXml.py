import os
import xml.etree.ElementTree as ET
import fitparse.profile

# Profil-Verzeichnis ermitteln
profile_dir = os.path.dirname(fitparse.profile.__file__)
manufacturers_xml = os.path.join(profile_dir, 'Manufacturers.xml')

# XML parsen
tree = ET.parse(manufacturers_xml)
root = tree.getroot()

# Mapping Code → Name
MANUFACTURER_CODES = {
    int(m.find('number').text): m.find('name').text
    for m in root.findall('manufacturer')
}

# Test: Werte für Coros, Peaksware, Garmin ausgeben
for code, name in MANUFACTURER_CODES.items():
    if name in ('Coros', 'Peaksware', 'Garmin'):
        print(code, '→', name)
