# CSharpTools ![GitHub top language](https://img.shields.io/github/languages/top/CoderAllan/CSharpTools.svg) ![GitHub](https://img.shields.io/github/license/CoderAllan/CSharpTools.svg) ![GitHub last commit](https://img.shields.io/github/last-commit/CoderAllan/CSharpTools.svg)

Collection of tools used when developing C# code

## ProjectHierarchy.py

This is a tool that traverses the directory structure of a C# solution and creates a MarkDown file beside every .csproj file with an overview of the structure of the project.

The tool also creates a MarkDown readme file for every .sln file with a table showing the rootnamespace and framework version for each project in the solution. All packages used in the projects in the solution is also shown in a matrix with project, packagename and the package version. This overview will make it easy to spot any mismatches between packages and packageversions.

### Usage

Run the python script from the root folder of your solution: `C:\Python\python.exe ..\CSharpTools\ProjectHierarchy.py`

## ProjectFileStructure.py

This is a tool for visualizing the folder structure of your project. The tool will exclude the following folders:

* bin
* obj
* node_modules
* dist
* packages
* .git
* .vs

### Usage

Run the python script from the root folder of your solution: `C:\Python\python.exe ..\CSharpTools\ProjectFileStructure.py`

### Example

The tool will print out the folder structure like this:

```txt
$ c:\Python\python.exe ..\ProjectFileStructure.py
./
    TestSolution/
        ClassLibrary1/
            Properties/
        CoreConsoleApp1/
        StandardClassLibrary2/
        StandardClassLibrary3/
        UnitTestProject1/
    TestSolution2012/
        ClassLibrary2/
            Properties/
            Scripts/
        ClassLibraryX1/
            Content/
            Properties/
            Scripts/
                esm/
                umd/
        ConsoleApplication1/
            Properties/
        TestSolution2012/
            Properties/
        WindowsService1/
            Properties/
```
