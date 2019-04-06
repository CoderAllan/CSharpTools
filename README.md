# CSharpTools

Collection of tools used when developing C# code

## ProjectHierarchy.py

This is a tool that traverses the directory structure of a C# solution and creates a MarkDown file beside every .csproj file with an overview of the structure of the project.

The tool also creates a MarkDown readme file for every .sln file with a table showing the rootnamespace and framework version for each project in the solution. All packages used in the projects in the solution is also shown in a matrix with project, packagename and the package version. This overview will make it easy to spot any mismatches between packages and packageversions.

Usage:

Run the python script from the root folder of your solution: `C:\Python\python.exe ..\CSharpTools\ProjectHierarchy.py`
