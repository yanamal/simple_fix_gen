# A simple demo of using Fix Explainer

This is a very simple demo that uses the Fix Explainer library:

- the `generate.py` file is a short end-to-end demo of using the library to generate fixes to incorrect student code, and outputing the generated data into a useable html file
  - this example generates the appropriate files in the `html` and `json` folders
- the `html` folder contains some sample generated html files,
  - it also contains the hand-made files `fixes.css` and `fixes.js`, which are automatically imported by the html generated by `generate.py` and demonstrate one way of using the fix data to create an interactive interface
    - with this file structure, you can just open any of the html files in the browser and they should work interactively as intended 
- the `json` folder contains `.json` files with the dump of the output as generated by the fix explainer.
