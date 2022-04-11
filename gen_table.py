import os
from argparse import ArgumentParser

midfix_str = r"""\midrule
"""

suffix_str = r"""\bottomrule
\end{tabular}
\end{document}"""


def get_plain_txt(fn):
    if os.path.isfile(fn):
        with open(fn, "r") as f:
            names = f.read().split(sep="\n")
            names = names[0:-1]  # last one is empty
            return names


def get_col_n(p):
    return len(p) + 2


def get_first_row(p):
    row1 = p.copy()  # deep copy
    row1.insert(0, "Name")
    row1.append(r"Total percentage \\")
    row1 = " & ".join(row1)
    return row1


def get_mid_rows(names, problems):
    n_col = get_col_n(problems)
    row = ''
    for name in names:
        row += name + (n_col - 1) * " & " + r" \\ " + "\n"

    return row


def get_prefix(p, hw_fn):
    hw_num = hw_fn.replace("hw", "")
    prefix_str = r"""\documentclass[11pt, a4paper, DIV=12]{scrartcl}
    \usepackage{booktabs}
    \title{Theoretical Astro-Particle Physics SS22 \\ Homework No.""" \
    + hw_num + r"""}
    \begin{document}
    \maketitle
    \renewcommand{\arraystretch}{1.5}
    \begin{tabular}{"""

    prefix_str3 = r"""}
    \toprule
    """
    prefix_str2 = get_col_n(p) * "c"
    prefix = prefix_str + prefix_str2 + prefix_str3
    #  print(prefix)
    return prefix


if __name__ == "__main__":
    parser = ArgumentParser(description='''This script generates a table with students as rows and problems as columns.
It automatically generates a LaTex file, compiles it with latexmk and
delete all the auxillary files from the compilation.
Student names and problems are defined in plain text files passed on
by command-line arguments.
'''
)
    parser.add_argument("-s", "--students", dest="names_fn", required=True,
                        help="plain text containing student names. One name for each line.")
    parser.add_argument("-p", "--problems", dest="probs_fn", required=True,
                        help="plain text containing problem numbers. One for each line.")
    args = parser.parse_args()
    #  name_fn = "student_list"
    #  hw_fn = "hw01"
    names = get_plain_txt(args.names_fn)
    problems = get_plain_txt(args.probs_fn)

    tex_fn = args.probs_fn + ".tex"
    with open(tex_fn, "w") as f:
        f.write(get_prefix(problems, args.probs_fn))
        f.write(get_first_row(problems))
        f.write(midfix_str)
        f.write(get_mid_rows(names, problems))
        f.write(suffix_str)

    os.system("latexmk")
    os.system("latexmk -c")
