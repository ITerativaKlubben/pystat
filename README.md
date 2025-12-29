This is the code used to get statistics for commits in ITKs Project Web. It is mostly written by ChatGPT and is not very well built, but it gets the job done.

To run, clone the repository in the same directory where you have your ITK Project Web fork:
.
├── itk_website
└── pystats

Make sure you have all the relevant python dependencies:
`pip install -r requirements.txt`

Run the main analyze code:
`python3 analyze.py`

Some values are hardcoded and might only meassure dates around 2024 and would have to be changed for future use

