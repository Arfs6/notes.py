# Anotes  

Anotes is a utility that aims to reduce the friction in writing notes on laptop, especially when the filetypes might be different.  

I have some crazy ideas, like searching for notes, managing notes referencing, adding extensibility and perhaps a GUI. Let's see where this project is going to be in ... 2 years. Starting from Sunday 12th November 2023.  

## Quick Start  

You need `python` and `pandoc` to be able to run anotes. I built it using `python3.12`, but I think it should work with `python` versions up to 3.10.  

You can get python at the official python download page: <https://www.python.org/downloads/>.  

I use `pandoc` to convert the files to `HTML`. For example, `.tex` get converted to a `HTML` file. You can get `pandoc` at the official installation page: <https://pandoc.org/installing.html>.  

### Installation  

Install anotes via pip:  

```bash
python -m pip install git+https://github.com/arfs6/anotes
```

This will get anotes from this github repo and install it.  

### Commands  

- `anotes topic create`: Create a new topic.
- `anotes topic edit`: Edit the index page of a topic.
- `anotes create`: Create a new topic.
- `anotes edit`: edit an existing note.

## Features  

At this point, anotes supports writing markdown (`.md`) and `LaTeX` (`.tex`) notes. When you open a file for editing using anotes, it starts a local server at port 7777 and serve all your notes. Further more, anotes detect when you save your file and automatically re-compiles it. This means, when you save the file and refresh your browser, you'll get the latest version of the file.  

## Status  

anotes is currently on alpha stage, and most features haven't been implemented yet.  

## Todo  

Read the [todo](./TODO.md) to see what I have worked on and what I am goin to work on.  

## License  

This software is distributed under the GNU General Public License, you can find details of the license [here](./LICENSE).
