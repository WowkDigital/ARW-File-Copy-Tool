📂 ARW File Copy Tool (GUI)
A modern Python desktop application built with **CustomTkinter** for quickly selecting and copying **.ARW** files based on a pasted **.enc** list.

The tool automatically matches files like `n_X.enc` → `n_X.ARW` and copies them to a dedicated folder (selected by default).
---
## ✨ Features
* Modern GUI using **CustomTkinter**
* Paste a list of **.enc** files (e.g., from another system or export)
* Automatically finds corresponding **.ARW** files in the source folder
* Copies matched files into a selected subfolder
* Warnings for missing files
* Clean, user-friendly workflow

---
## 🚀 How It Works
1.  **Select** the source folder containing **.ARW** files
2.  **Paste** the file list (with **.enc** names, e.g. `0004_n_3.enc`)
3.  The app:
    * **Extracts** numbers from patterns like `n_X.enc`
    * **Matches** them with files like `n_X.ARW`
    * **Copies** found files to `[source]/selected` (or another destination if changed)
4.  If some files are missing, the app warns you after completion.

---
## 🖼️ GUI Preview
(add your screenshot here, for example)

![App Screenshot](docs/screenshot.png)
