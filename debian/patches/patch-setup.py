Index: Electrum-SPARKS-3.2.3/setup.py
===================================================================
--- Electrum-SPARKS-3.2.3.orig/setup.py
+++ Electrum-SPARKS-3.2.3/setup.py
@@ -77,6 +77,7 @@ setup(
         'electrum_sparks',
         'electrum_sparks.gui',
         'electrum_sparks.gui.qt',
+        'electrum_sparks.plugins',
     ] + [('electrum_sparks.plugins.'+pkg) for pkg in find_packages('electrum_sparks/plugins')],
     package_dir={
         'electrum_sparks': 'electrum_sparks'
