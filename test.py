import zipimport

importer = zipimport.zipimporter('shipData.zip')
nltk = importer.load_module('nltk')