This small script makes it easy for you to bulk edit the metadata of files in a vault of markdown files with YAML frontmatters.

# How to use it

Consider this example from `example.py`:

```python3
if __name__ == "__main__":
    VAULT_PATH = os.getcwd()
    my_vault = Vault(VAULT_PATH)
    my_vault.make_change(remove_cedrics_traces)
```

I first create a `Vault` object using the path to my vault (backup your vault before you do this!). I then use this `Vault` object to call the function `remove_cedrics_traces`.

The code of this function is:

```python3
def remove_cedrics_traces(frontmatter, content):
    if "authors" in frontmatter and "cedric" in frontmatter["authors"]:
        frontmatter["authors"].remove("cedric")
    
    return (frontmatter, content)
```

The function takes a frontmatter and content as an argument and returns a tuple of a frontmatter and content. The frontmatter is a dictionary, the content a list of strings. In this function I specify the change that I want to make to an individual file. When I call `make_change` the `Vault` object will execute this change for each file in the vault.

You can alternatively call `preview_change`. This won't change the files. Instead it will print the frontmatter and content that it would give the files to the console.

Now you can define your own function, pass it to `make_change` and bulk edit your vault in any way you see fit! :smile:
