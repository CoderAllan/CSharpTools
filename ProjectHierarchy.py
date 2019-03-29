import os
import os.path
import re

class Project:
    def __init__(self, projectFilename: str, projectName: str, projectRootPath: str, subprojects: list):
        self.ProjectFilename = projectFilename
        self.ProjectName = projectName
        self.ProjectRootPath = projectRootPath
        self.SubProjects = subprojects

def DisplayProject(subProjects: list, projectName: str, indent: int):
    indentation = " " * (indent * 3)
    displayName = projectName.replace(".csproj", "")
    if (len(subProjects) == 0):
        output = f"{indentation}<{displayName}></{displayName}>\n"
    else:
        output = f"{indentation}<{displayName}>\n"
        for subProject in subProjects:
            result = DisplayProject(subProject.SubProjects, subProject.ProjectName, indent+1)
            output = f"{output}{result}" 
        output = f"{output}{indentation}</{displayName}>\n"
    return output

# find all files recursively under the current folder that ends with *.csproj
projectFilenames = [os.path.join(dp, f) for dp, dn, filenames in os.walk(".") for f in filenames if f.endswith(".csproj")]

projectDictionary = {}
# print(projectFilenames)
for projectFilename in projectFilenames:
    projectName = os.path.basename(projectFilename)
    # print(f"projectName: {projectName}")
    if projectName in projectDictionary:
        currentProject = projectDictionary[projectName]
        currentProject.ProjectFilename = projectFilename
    else:
        currentProject = Project(projectFilename, projectName, "", [])
    f = open(projectFilename)
    line = f.readline()
    while line:
        match = re.match(r".*ProjectReference Include=\"(.*)\\(.*?)\"", line, re.IGNORECASE)
        if match:
            subProjectName = match.group(2)
            if subProjectName in projectDictionary:
                subProject = projectDictionary[subProjectName]
                # print(f"subProject: {subProjectName} - Found")
            else:
                subProject = Project(f"{match.group(1)}\\{subProjectName}", subProjectName, os.path.dirname(projectFilename), [])
                projectDictionary[subProjectName] = subProject
                # print(f"subProject: {subProjectName} - Not Found")
            if not subProject in currentProject.SubProjects:
                currentProject.SubProjects.append(subProject)
        line = f.readline()
    f.close()
    # print(f"Adding project: {projectName}")
    if not currentProject.ProjectName in projectDictionary:
        # print(f"currentProject.ProjectName: {currentProject.ProjectName} Not Found)
        projectDictionary[projectName] = currentProject

for projectName in projectDictionary:
    newFilename = projectName.replace(".csproj","")
    outputFilename = projectDictionary[projectName].ProjectFilename.replace(projectName, f"ReadMe-ProjectStructure-{newFilename}.md")
    print(f"projectName: {projectName}, Filename: {outputFilename}")
    output = DisplayProject(projectDictionary[projectName].SubProjects, projectName, 0)
    output = f"# Project hierachy for {projectName}\n\nThe following structure shows the project hierachy:\n\n```xml\n{output}```"
    file = open(outputFilename, "w")
    file.write(output)
    file.close()

