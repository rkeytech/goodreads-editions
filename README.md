# Goodreads Editions

A python script for finding other editions of a book on Goodreads, based on its ISBN or Name, and choosing other languages to filter editions.

---

#### <u>Requirements</u>

The requiments for the script to run are in the `requirements.txt` file. You can install all the requirements at once with `pip install -r requirements`. Obviously, you need first to check that you've got the Python version 3.8 on your system and you've got pip installed. The program was built with these versions of the required libraries but maybe it'll work with versions greater than the required.

#### <u>Usage</u>

```bash
python3 gr-editions.py {ISBN or Name} {language} {output-file}
```

- **ISBN or Name**: The ISBN number or the name of the book you are looking for other editions.

- **language**: The language in which you are looking for an edition of the book.

- **output-file**: The output file in which you want to write the URLs of the editions.
