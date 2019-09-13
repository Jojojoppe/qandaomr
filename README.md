# OMR
![](https://github.com/Jojojoppe/OMR/workflows/Build/badge.svg)

This package can create a form which can be read in with OMR and can read those forms.

## Usage
### Creating an OMR form
To create an OMR enabled form you must make a form (with Word, LaTeX or similar software) and mark the first bullet points with a **red** background and the last with a **green** background. At last the corners should be marked: the bottom right corner must be marked with a black square and the three other corners with a QR code like corner. At this moment the user must do this themselfes (this may change in the future). The imput to OMR must be an image file.
![An empty OMR form](/img/empty_form_r.png)

Running the following will generate a printable output sheet with barcodes at the bottom which OMR uses to detect the settings
```
omr -c input_file output_file columns rows points_per_question questions_per_block
```
![Created omr form](/img/form_r.png)

### Reading an OMR form
To get the answers back from the form a scanned image can be the input to OMR. OMR will print the answers to the terminal in a CSV format.
```
omr -r input_file
```

### Generating intermediate files
For debug purposes the `-d` flag can be used. This will generate multiple images which are used in the steps within OMR. This can be useful if OMR does not react the way it should

## Installation
To install this package clone this repository and install via pip:
```
git clone https://github.com/Jojojoppe/OMR.git
cd OMR
pip install .
```

Uninstalling can be done via pip:
```
pip uninstall omr
```
*Note: this package is not (yet) registered ad PyPi meaning that other packages may exist with this name!*
