
"""
About
=====

Outputs an XML with a list of countries; each country has a ISO 3166 code,
name, translated name, official name and translated official name.


How to use
==========

1. install the lxml package
   eg. http://pypi.python.org/pypi/lxml/2.3#downloads
2. download the iso-codes binary package from http://packages.ubuntu.com/oneiric/iso-codes
   eg. http://uk.archive.ubuntu.com/ubuntu/pool/main/i/iso-codes/iso-codes_3.27-1_all.deb
   NB you could try a recent package file by browsing
        http://uk.archive.ubuntu.com/ubuntu/pool/main/i/iso-codes/?C=M;O=D
3. unpack it to the current directory
4. modify the langs list variable bellow
5. run this script

NB you might need to fiddle with the encoding of sys.stdout...
"""

import os
import gettext
import codecs
import sys
from lxml import etree

if False and not sys.stdout.isatty():
	# force stdout to write utf8 encoded text.
	sys.stdout = codecs.getwriter("utf8")(sys.stdout)

langs = (
	"pt",
	"es",
	"zh_CN",
)
translations = [(lang, gettext.translation("iso_3166", "usr/share/locale", [lang])) for lang in langs]

countries = etree.TreeBuilder()
countries_root = countries.start("countries", {})

tree = etree.ElementTree()
tree.parse("usr/share/xml/iso-codes/iso_3166.xml")

for entry in tree.iter("iso_3166_entry"):
	if "date_withdrawn" in entry.attrib:
		continue

	country_code = entry.attrib["alpha_2_code"]
	countries.start("country", {"code":country_code})

	for attribute_name in ("name", "official_name"):
		if attribute_name not in entry.attrib:
			continue

		name = entry.attrib[attribute_name]
		countries.start(attribute_name, {"lang":"en"})
		countries.data(name)
		countries.end(attribute_name)

		for lang, t in translations:
			t_name = t.ugettext(name)
			countries.start(attribute_name, {"lang":lang})
			countries.data(t_name)
			countries.end(attribute_name)

	countries.end("country");

countries.end("countries")

print etree.tostring(countries_root, pretty_print=True, encoding="utf8")
