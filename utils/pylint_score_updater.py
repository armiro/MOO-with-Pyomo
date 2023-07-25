import subprocess
import re

# run Pylint and get the output
pylint_output = subprocess.check_output(['pylint', '--exit-zero', '$(git ls-files "*.py")'])

# extract the Pylint score using regex
score_match = re.search(r'Your code has been rated at (\d+.\d+)/10', pylint_output.decode())
pylint_score = score_match.group(1) if score_match else "N/A"

# update README.md with the Pylint badge and score
with open("README.md", "r") as readme_file:
    readme_content = readme_file.read()

with open("README.md", "w") as readme_file:
    updated_content = re.sub(pattern=r"!\[Pylint Score\].*",
                             repl=f"![Pylint Score](https://img.shields.io/badge/PyLint-{pylint_score}/10-brightgreen)",
                             string=readme_content)
    readme_file.write(updated_content)
