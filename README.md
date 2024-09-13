# Picker

Picker is a scraper.
It takes instructions from a `.csv` file and writes the output to either a `.csv` or an `.xlsx` file.

To use it, run the main script using Python:
```
python main.py
```
For more instructions, [see the section on how to use this program](#how-to-use).



## Dependecies

### Python

This project requires Python 3.9 or newer to run.
[You can download Python here.](https://www.python.org/downloads/)

### Packages

This project also requires a few packages to run.
With Python installed, run the following command to install them:
```
pip install -r requirements.txt
```


# How To Use

## Script Parameters

The main script accepts a few optional arguments.

### Input File

First, you can tell the scraper to look for a specific input file.
By default, if no file is specified, it will look for `input.csv`.
The file name ***must be a csv file*** whose name ***must end in*** `.csv`.
```
python main.py something.csv
```

### Output Format

You can also tell the scraper which file format to output to.
The default, if none is provided, is `.csv`, but `.xlsx` is also supported.
You ***must provide an input file name*** if you want to use this flag.
```
python main.py something.csv .xlsx
```

### Delay Between Requests

Lastly, you can apply a random delay between requests to avoid bot detection measures,
though in current year, the effectiveness of this feature is debatable.
By default, this feature is disabled.
To enable it, set the last flag to `T`, `True`, `Y`, `Yes` or `Slow`.
You ***must provide all other arguments*** if you want to use this flag.
```
python main.py something.csv .xlsx T
```

## Input File

The input file is a csv file that follows a specific format.

### Header

The first row must be formatted as follows:
```
url,tags,filename,args
```

### Rows

All other rows each describe a separate task to be executed by the scraper.
They must each contain 4 cells which, from left to right, are the
[`url`](#url), [`tags`](#tags), [`filename`](#filename) and [`args`](#args)
arguments respectively.

See their individual sections for further explanations.

### URL

The first cell in a row is the url that the scraper will visit:
```
https://example.com/
```

### Tags

The second cell contains the HTML tags that the scraper will look for.
You only need to provide the opening tag.
For example, if you want to scrape the text from the following `h2` element,
```
...
    <modal>
        <article>
            <h2>
                Text to scrape
            </h2>
            ...
        </article>
        ...
    </modal>
...
```
You only need to write `<modal><article><h2>` in the cell.

### Filename

The third cell contains the name of the file that the scraper will write to.
You can name it anything as long as it ends in `.csv` or `.xlsx`,
or if it doesn't end in either, the parser will use [the default extension set earlier](#output-format).

The following are all valid inputs:
```
<nothing>
output
output.csv
output.xslx
output.other
```

### Args

The last cell in a row contains some optional arguments for the scraper.
If any are used, they must be provided in Python [`dict`](https://docs.python.org/3/tutorial/datastructures.html#dictionaries) format.
[See the section on input arguments](#input-arguments) for more details. [Also see the examples](#examples).

## Input Arguments

### Append

The `append` argument is a string that is appended at the end of [`url`](#url).
Not very useful in and of itself, but it is required if you provide a [`range`](#range) argument.

### Range

The `range` argument is an array of **one** or **two** integers, formatted as a Python [`list`](https://docs.python.org/3/tutorial/introduction.html#lists).

If you use the `range` argument, you must also provide a string that contains the sequence `"^R"` for the [`append`](#append) argument.

If you provide **two** integers, for **each** integer `x` between the **first** and the **second** integer inclusively, the scraper will replace the `"^R"` sequence in `append` by the integer `x` and re-run the task with this new `append` string.

If you provide only **one** integer, the scraper will run the task with `"^R"` replaced by this integer, and then keep re-running the same task with integer increased by `1` each time, until it encounters an address which does not exist.

This argument is especially useful if you're scraping directories with multiple "pages" which can be accessed using a query parameter like `?page=0`.

### Examples

The following are all valid inputs for `args`:
```
<nothing>
{}
{ append: '' }
{ append: '?q=query&p=param' }
{ append: '/nested/url' }
{ append: '?page=^R', range: [1, 100] }
{ append: '/^R/nested/pages', range: [1, 100] }
{ append: '/item-^R', range: [0] }
```
