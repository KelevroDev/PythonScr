#!/usr/bin/env python
import xml.etree.ElementTree as ET
from xml.etree.ElementTree import ParseError
try:
   x = ET.fromstring('/etc/Toyota_CY17.XML')
   print "XML was parsed properly"
except ParseError:
   print "XML could not be parsed (ParseError)"
