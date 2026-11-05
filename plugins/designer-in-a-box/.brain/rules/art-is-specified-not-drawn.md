THE RULE

A designed piece is a specification that a script renders. The model writes the art-spec; code validates it and draws the pixels.

- Format, tokens, layouts, text and image slots live in the art-spec.
- Contrast, minimum font size, safe zone and character limits are checked by `scripts/render-art.py`, not argued.
- A change to a piece is a change to the spec, then a re-render.

WHY

Trigger: someone asks for a post, carousel, banner or cover to be made.

A piece that follows a fixed model every time is produced by code (CONVENTIONS section 9), and a spec can be reviewed, versioned and reproduced where hand-edited pixels cannot.

HOW TO APPLY

`post-designer` writes the spec, `art-renderer` runs the script, `design-reviewer` judges what code cannot check and fixes go back into the spec.

RELATED

Skills: post-designer, art-renderer, design-reviewer. Script: plugins/designer-in-a-box/scripts/render-art.py.
