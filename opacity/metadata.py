import os
import re
import json
from pathlib import Path

import ipywidgets
from IPython.display import display, Javascript
import solara

__all__ = ['Metadata']

tab_style = {
    'text-transform': 'capitalize'
}
value_style = {
    'padding-left': '8em',
    'padding-top': '0.5em',
    'padding-bottom': '0.5em',
}


metadata_desc_path = os.path.join(
    os.path.dirname(__file__),
    'data',
    'metadata_descriptions.json'
)

with open(metadata_desc_path, 'r') as meta:
    metadata_desc = json.load(meta)


def copy_button(text):
    output = ipywidgets.Output()

    def on_button_click(_, text=text):
        with output:
            output.clear_output()
            display(Javascript(f'navigator.clipboard.writeText("{text}")'))

    button = ipywidgets.Button(description="", icon="copy")
    button.on_click(on_button_click)
    button.layout.width = '30pt'
    button.layout.font_size = '1pt'
    button.style.button_color = "transparent"
    button.style.text_color = "#037ffc"

    return ipywidgets.HBox([button, output])


def unpack_dict(d):
    tab_order = [
        'linelist', 'calculation', 'broadener_H2',
        'broadener_He', 'compression', 'source',
    ]
    for tab_key, tab_value in d.items():
        if tab_key in ['molecule', 'unit']:
            continue

        if tab_key in tab_order:
            with solara.lab.Tab(f"{tab_key}", style=tab_style):
                with solara.Div(style={'padding-left': '3em'}):
                    unpack_dict(tab_value)
                    continue

        else:
            if tab_key == 'todo' or tab_value == '':
                continue

            solara.Markdown(f"#### {tab_key}")

            if tab_key.startswith('calculation_type'):
                desc = metadata_desc['broadening']['calculation_options'][tab_value]['description']
                solara.Markdown(f"{desc}", style={'color': '#5A5A5A'})

            with solara.Row(margin=0):

                if tab_key.startswith('usr_warning'):
                    if tab_value == 0:
                        solara.Markdown("No warnings.", style=value_style)
                    else:
                        desc = metadata_desc['broadening']['usr_warnings'][str(tab_value)]
                        solara.Markdown(f"{desc} ({tab_value})", style=value_style)
                else:
                    value_markdown, copy_text = to_markdown(tab_value)
                    solara.Markdown(
                        value_markdown,
                        style=value_style
                    )
                    if copy_text:
                        # with solara.Tooltip("Markdown", color="white"):
                        solara.display(copy_button(copy_text))


def to_markdown(text):
    text_href_markdown, href_url = latex_href_to_markdown(str(text))
    text_markdown, doi_url = doi_to_markdown(text_href_markdown)

    if href_url is not None:
        copy_text = href_url
    elif doi_url is not None:
        copy_text = doi_url
    elif '$' in text_markdown or text_markdown.startswith('['):
        copy_text = text_markdown
    else:
        copy_text = None

    return str(text_markdown), copy_text


def latex_href_to_markdown(text):
    if not isinstance(text, str) or 'href' not in text:
        return text, None

    pattern = r"\\href\{([^}]*)\}\{([^}]*)\}"
    replacement_html = r'<a href=\1 target="_blank">\2</a>'
    replacement_markdown = r"[\2](\1)"
    return (
        re.sub(pattern, replacement_html, text),
        re.sub(pattern, replacement_markdown, text)
    )


def doi_to_markdown(text):
    if not isinstance(text, str) or 'DOI' not in text:
        return text, None

    pattern = r"DOI=\[(.*?)\]"
    replacement_html = r'<a href=https://doi.org/\1 target="_blank">\1</a>'
    replacement_markdown = r'[\1](https://doi.org/\1)'
    return (
        re.sub(pattern, replacement_html, text),
        re.sub(pattern, replacement_markdown, text)
    )


@solara.component
def Metadata(cross_section):
    solara.Markdown(f"## Metadata: {cross_section.attrs['molecule']}")
    with solara.lab.Tabs(
        vertical=True, lazy=True, color="#C5F8FD",
        dark=True, background_color="#13457B",
        slider_color="#A0F7FF"
    ):
        tab_order = [
            'linelist', 'calculation', 'broadener_H2',
            'broadener_He', 'compression', 'source',
        ]
        dictionary = {
            ordered_key: cross_section.attrs[ordered_key]
            for ordered_key in tab_order
        }
        unpack_dict(dictionary)
