# PDF Compiler version 3.2
A Java program (that uses AWT/Swing as the GUI) that compiles multiple PDF files into one PDF. We have rewritten the whole
code base from our Python source code to Java, for the application to become operating system independent and easier to create
binaries for all platforms.

**System Requirements:**
- <a href="https://java.com/">Oracle Java Runtime</a> (version 11 or higher)
- Windows 7 or later; MacOS X 10.6 and later; Linux with a graphical interface.
- Memory: 512MB (minimum)

## Release 1.1
Initial introduction of PDF Compiler v1.0 under the 1.1 git versioning system. This version introduces the core and 
essential parts of a functioning PDF combiner for multiple files.

### Release 1.1.2
Implements the functionality of PDF compression of the dummy checkbox "PDF compression" and makes minor changes in moving
documents up and down the list

## Release 2.0 (Dec 2023)
Introduce a preview window for the PDFs, page selection, merge specific pages (for multipaged PDFs), and drag-n'-drop 
functionality. A rewrite of the user interface from tkinter (Python's default library) to PyQt 6, as our code becomes a 
bit more complex. Removal of PDF compression (for now).

## Release 3.0 (Spring 2024)
We have rewritten the whole code base from our Python source code to Java, for the application to become operating system independent and easier to create binaries for all platforms. No new features are introduced in this version. Some features
from previous versions may not be working due to the rewrite, but will be implemented in 3.x versions in the upcoming months.

### Release 3.1 (Part of Spring 2024)
Rewrote drag-n-drop in Java for PDF Compiler to easily drag and drop files. Squashed some bugs.

### Release 3.2 (2026)
Sets the Nimbus look and feel as the default UI theme for a consistent, modern appearance across Windows, macOS, and Linux.
General codebase cleanup (lambda event handlers, shared drag-and-drop/file-chooser logic, case-insensitive `.pdf`
matching, and consolidated error handling). Adds automated GitHub Actions release builds that compile a runnable,
self-contained JAR and publish it as a release asset on every `v*` tag.

(c) 2023 - 2026 Morales Research Inc

(c) 2023 - 2025 The University of Texas at Austin, Department of Computer Science
