# hallom/__init__.py

# Dieses Verzeichnis ('hallom') wird durch das Vorhandensein dieser __init__.py-Datei
# als Python-Paket (Package) definiert. Dies ermöglicht es, Module aus diesem
# Ordner zu importieren, z.B. 'from hallom import datei'.

# ---
# Steuerung des Stern-Imports (from hallom import *)
# Die Variable __all__ definiert, welche Module öffentlich verfügbar sind,
# wenn ein "Stern-Import" (z.B. 'from hallom import *') für dieses Paket verwendet wird.
# In diesem Fall wird nur das Modul 'datei' exponiert.
__all__ = ["datei"]

# ---
# Bereitstellung von Modulen und Funktionen auf Paketebene
# Dieser Import macht das Modul 'datei' direkt über das Paket 'hallom' zugänglich.
# Das bedeutet, du kannst es entweder als 'from hallom import datei' oder
# 'import hallom' und dann 'hallom.datei.f()' verwenden.
# Der Punkt '.' vor 'datei' ist ein relativer Import und bezieht sich auf das
# aktuelle Paket.
from . import datei