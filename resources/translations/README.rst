The files in this directory are traduction files. 
If you want to add/supress traductions, follow the following procedure :

1) Add your modifications in the code : mark the strings subject to translations thanks to the translate() or tr() methods.

2) Update the \*.ts file to signify the new changes (command "lupdate app.pro").

3) If you need to, add the traductions manually thanks to the Qt Linguist UI. This will modify the \*.ts files

4) Compile the \*.ts to obtain the files loaded by the code, the \*.qm files (command "lrelease app.pro")

Note that the emplacement of the traduction files must be told to the qt main configuration file (here a \*.pro)
