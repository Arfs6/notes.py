# notes.py  

Notes.py is a utility that aims to reduce the friction in writing notes on laptop, especially when the filetypes might be different.  

The process of writing a note with notes.py should be:  

- Type `notes.py create` in your command line.  
- Select a topic this note is based on.  
- Give the note a title (name).  
- Optionally supply the filetype of the note, defaults to markdown.  
- Begin editing your note with your favourite text editor.  
- Save the file and exit your text editor.  
- notes.py will then compile your notes into the format you specified in your configuration file, defaults to html.
- Additionally, you can supply the `-q` argument to create a quick note and edit / move it later.  

Notes.py is going to take care of creating the files for you to write your notes in, compiling the files and optionally updating it.  

I have some crazy ideas, like searching for notes, managing notes referencing, adding extensibility and perhaps a GUI. Let's see where this project is going to be in ... 2 years.  

## Stage  

notes.py is currently on alpha stage, and most features haven't been implemented yet.  

## Todo  

Read the [todo](./TODO.md) to see what I have worked on and what I am goin to work on.  

## License  

This software is distributed under the GNU General Public License, you can find details of the license [here](./LICENSE).
