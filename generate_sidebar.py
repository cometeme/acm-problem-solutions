import os

content = """-   About me
    -   [ACM templates](https://www.adelardcollins.com/algorithms-and-templates/)
    -   [My technology blog](https://www.adelardcollins.com)
    -   [My GitHub](https://github.com/cometeme)
"""

with open("docs/_sidebar.md", "w") as f:
    for oj in sorted(filter(lambda x: "." not in x, os.listdir("docs"))):
        f.write("-  {}\n".format(oj))

        problems = sorted(
            filter(lambda x: ".md" in x, os.listdir("docs/{}".format(oj))),
            key=lambda x: (x[:-3] if x[-4].isdigit() else x[:-3] + "0").rjust(20, "0"),
        )

        for problem in problems:
            with open("docs/{}/{}".format(oj, problem)) as p:
                f.write(
                    "   -   [{}]({})\n".format(
                        p.readline().strip(" #\n"), "/{}/{}".format(oj, problem)
                    )
                )

        f.write("\n")

    f.write(content)
