# PDF Text Extraction Test

Trying to figure out which library to use for the future `pdf2dict` function in [doc2dict](https://github.com/john-friedman/doc2dict). Main concern is how fast can we extract text with attributes like **bold** and coordinates to construct the text into lines.

HTML parsing is at ~ 57 pages in 150ms, so would be nice to get a library with that as the upper bound.

## Benchmarks

Benchmarks based on the Microsoft ARS pdf ~ 60 pages

| Package | Speed |
| -------- | -------- |
| pdftotext  | would not install   |
| pdfplumber | 5430 ms |
| pdfminer6 | 1930 ms |
| pypdfium2 | 140 ms |

Great, looks like we'll try building on pypdfium2.

Note: pypdfium2 IS NOT SAFE AS OF 5/25 FOR MULTITHREADING. This is going to come back to bite me at some point.

## pypdfium2

Great! Got what I need. Looks like ~300ms to parse the ars pdf with all features which is fine.
