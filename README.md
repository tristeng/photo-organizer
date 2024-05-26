# Photo Organizer
A small command line utility to help a photographer organize photos

## How to use
This application runs in pure Python 3.9. It does not require any external libraries. To run the application, simply 
run the following command in the terminal to see the required and optional arguments:
```bash
python main.py -h
```

## Example
To organize photos in the directory `photos` based on the CSV file `test.csv`, run the following command in the 
terminal:
```bash
python main.py python main.py sample/test.csv sample/photos
```

This will automatically create directories based on the student's first and last names and move the photos to the 
appropriate directories.