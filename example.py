from main import Vault
import os

def remove_cedrics_traces(frontmatter, content):
    if "authors" in frontmatter and "cedric" in frontmatter["authors"]:
        frontmatter["authors"].remove("cedric")
    
    return (frontmatter, content)

if __name__ == "__main__":
    VAULT_PATH = os.getcwd()
    my_vault = Vault(VAULT_PATH)
    my_vault.make_change(remove_cedrics_traces)
