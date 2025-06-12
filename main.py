import oyaml as yaml
import os
from os import path

# TODO: is there some way to make sure that the change method has the right shape
# and arguments? Maybe by using classes?

class Vault():
    def __init__(self, root_path):
        self.ROOT_PATH = root_path

    # TODO: add support for changing file name and location:
    # Add a paramater `filename` to the change method (and the value it returns).
    def make_change(self, change):
        self.apply_change(change, save=True)

    def preview_change(self, change, limiting_amount=None):
        self.apply_change(change, save=False)

    def apply_change(self, change, save):
        for dirpath, _, filenames in os.walk(self.ROOT_PATH):
            for filename in filenames:
                if filename.endswith('.md'):
                    file_path = path.join(dirpath, filename)
                    with open(file_path, 'r', encoding='utf-8') as file:
                        content = file.readlines()

                    frontmatter, content = Vault._extract_frontmatter(content, filename)
                    new_frontmatter, new_content = change(frontmatter, content)

                    if save:
                        Vault._save_file(file_path, new_frontmatter, new_content)
                    else:
                        try:
                            width, _ = os.get_terminal_size()
                        except:
                            width = 80

                        title = "*"
                        title += " " * int(((width / 2) - (len(filename) / 2)))
                        title += filename
                        title += " " * int((width - len(title) - 1))
                        title += "*"

                        print("*" * width)
                        print(title)
                        print("*" * width)

                        Vault._print_preview(new_frontmatter, new_content)

    def _extract_frontmatter(content, filename):
        if not content:
            return ({}, [])

        frontmatter_lines = []
        content_lines = []
        
        # does the file have a frontmatter?
        if content[0].strip() == '---':
            valid_frontmatter = False
            for line in content[1:]:
                if line.strip() == '---':
                    valid_frontmatter = True
                    break

                frontmatter_lines.append(line)
            
            if not valid_frontmatter:
                raise ValueError("Invalid frontmatter definition!")
            
            try:
                frontmatter = yaml.load("\n".join(frontmatter_lines), Loader=yaml.Loader) if frontmatter_lines else {}
            except yaml.scanner.ScannerError:
                frontmatter = {}
                print(f"WARNING: could not extract frontmatter for {filename}!")
        
            content_lines = content[len(frontmatter_lines) + 2:]
        # no frontmatter, so we just return the content
        else:
            content_lines = content
            frontmatter = {}


        return (frontmatter, content_lines)

    def _save_file(file_path, frontmatter, content):
        with open(file_path, 'w', encoding='utf-8') as file:
            if frontmatter:
                file.write('---\n')
                file.write(yaml.dump(frontmatter, default_flow_style=False))
                file.write('---\n')
            file.writelines(content)

    def _print_preview(frontmatter, content):
        print('---')
        print(yaml.dump(frontmatter, default_flow_style=False), end='')
        print('---')
        print(''.join(content))
