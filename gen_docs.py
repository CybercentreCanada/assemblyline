from importlib.machinery import SourceFileLoader
from inspect import isclass
from assemblyline.odm.base import Model
from collections import defaultdict
from sys import argv

import os
import yaml
import regex

odm_docs = defaultdict(list)


def main(root_dir, site_prefix=None):
    BASE_PATH = f"{root_dir}/assemblyline-base/assemblyline/"
    DOCS_BASE_PATH = f"{root_dir}/assemblyline4_docs/"
    DOCS_DOCS_PATH = os.path.join(DOCS_BASE_PATH, "docs/")

    def render_markdown(file) -> None:
        if not file.endswith(".py"):
            return
        lib = SourceFileLoader(file, file).load_module()
        markdown_list = [(c.markdown(), c.__name__) for c in lib.__dict__.values() if isclass(
            c) and issubclass(c, Model) and not (c.__module__.startswith("assemblyline.odm.models"))]

        if markdown_list:
            # Bring last item to the front
            name = markdown_list[-1][1]
            compiled_md = "\n\n".join(m[0] for m in markdown_list)
            if len(markdown_list) > 1:
                compiled_md = markdown_list.pop(-1)[0]
                # Check if other models were part of the first render
                for md, md_name in markdown_list:
                    # Add if missing
                    if not regex.search(f"# {md_name}\n>", compiled_md):
                        compiled_md += f"\n\n{md}"

            doc_path = file.replace(BASE_PATH, DOCS_DOCS_PATH).replace(".py", ".md")
            if site_prefix:
                compiled_md = compiled_md.replace('/odm/', f'{site_prefix}/odm/')
            open(doc_path, 'w').write(compiled_md)
            return doc_path, name
        return None, None

    def create_ODM_docs(base, models):
        for item in sorted(os.listdir(base)):
            path = os.path.join(base, item)
            if os.path.isfile(path):
                if not item.endswith(".py"):
                    continue
                # Render ODM to Markdown
                doc_path, name = render_markdown(path)
                if doc_path:
                    # Add entry into nav config
                    rel_path = doc_path.replace(DOCS_DOCS_PATH, "")
                    models.append({name: rel_path})
            elif item != "__pycache__":
                # Perform a recursive call to look for ODM files
                os.makedirs(path.replace(BASE_PATH, DOCS_DOCS_PATH), exist_ok=True)
                submodel = []
                create_ODM_docs(path, submodel)
                if item.lower() == item:
                    item = item.title()
                models.append({item: submodel})

    create_ODM_docs(os.path.join(BASE_PATH, "odm/models"), odm_docs['models'])
    create_ODM_docs(os.path.join(BASE_PATH, "odm/messages"), odm_docs['messages'])

    yaml.add_multi_constructor('', lambda loader, suffix, node: None)

    mkdocs = yaml.load(open(os.path.join(DOCS_BASE_PATH, "mkdocs.yml"), "r").read(), Loader=yaml.Loader)
    mkdocs['nav'][7]['Data Ontology'][1]['Models'] = odm_docs['models']
    mkdocs['nav'][7]['Data Ontology'][2]['Messages'] = odm_docs['messages']
    yaml.dump(mkdocs, open(os.path.join(DOCS_BASE_PATH, "mkdocs.yml"), "w"), allow_unicode=True)


if __name__ == "__main__":
    if len(argv) != 3:
        raise ValueError("Missing:\nroot directory containing: assemblyline-base, assemblyline4_docs\nsite prefix")
    root_dir = argv[1]
    site_prefix = argv[2]
    if site_prefix[0] != '/':
        raise ValueError('Site prefix must start with "/"')
    elif "assemblyline-base" not in os.listdir(root_dir):
        raise ValueError(f"Can't find assemblyline-base in given directory: {root_dir}")
    elif "assemblyline4_docs" not in os.listdir(root_dir):
        raise ValueError(f"Can't find assemblyline4_docs in given directory: {root_dir}")

    main(root_dir=root_dir, site_prefix=site_prefix)
