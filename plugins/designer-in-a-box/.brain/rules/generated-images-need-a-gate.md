THE RULE

A diffusion model is an external service. Nothing is sent to it until the owner approves that exact set of requests, and the request carries only what the designer specified.

- The request holds slot, prompt, negative, style, aspect and seed. No post copy, names, contact details, links or files.
- The designer's brief is sent as written; the image role adds nothing to it.
- The owner sees the whole request set and its hash first; the approval covers that set only.
- Images hold no lettering (text is typeset by the renderer) and are recorded with provider and request hash.

WHY

Trigger: someone asks for a model-generated image, illustration or hero picture.

The provider may keep what it receives, and personal material never goes out without a yes for that move (the owner's rule on outward actions). Binding the approval to a hash makes an edited request fail instead of slipping through.

HOW TO APPLY

Run `scripts/generate-image.py` as a dry run, show `image-requests.json` and the hash, and send with `--send --provider <name> --authorize <hash>` only after the owner says yes.

EXCEPTIONS

None for personal material. A request that is generic (an abstract background) still needs the approval; it is not a free pass.

RELATED

Skill: image-generator. Script: plugins/designer-in-a-box/scripts/generate-image.py.
