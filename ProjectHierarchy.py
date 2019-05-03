import os
import os.path
import re
import argparse
import igraph as ig

parser = argparse.ArgumentParser()
parser.add_argument("-ph", "--generateprojecthierarchy", help="Generate project hierarchy in xml format for each cs-project file", action="store_true")
parser.add_argument("-sr", "--generatesolutionreadme", help="Generate solution readme in markdown format for each solution file", action="store_true")
parser.add_argument("-dg", "--generatedirectedgraph", help="Generate directed graph in dgml format for each cs-project file", action="store_true")
parser.add_argument("-gm", "--generategraphml", help="Generate directed graph  in GraphML (xml) format for each cs-project file", action="store_true")
args = parser.parse_args()

generateProjectHierarchy = args.generateprojecthierarchy
generateSolutionReadme = args.generatesolutionreadme
generateDirectedGraph = args.generatedirectedgraph
generateGraphML = args.generategraphml
generateSVG = False
generatePNG = False

class Project:
    def __init__(self, projectFilename: str, projectName: str, projectRootPath: str):
        self.ProjectFilename = projectFilename
        self.ProjectName = projectName
        self.ProjectRootPath = projectRootPath
        self.SubProjects = []
        self.TargetFramework = ""
        self.RootNamespace = ""
        self.Packages = []
        self.PackageDictionary = {}

class Solution:
    def __init__(self, solutionName: str):
        self.SolutionName = solutionName
        self.Packages = []

class Link:
    def __init__(self, source: str, target: str):
        self.Source = source
        self.Target = target

def GeneratedProjectHierarchy(subProjects: list, projectName: str, indent: int):
    indentation = " " * (indent * 3)
    displayName = projectName.replace(".csproj", "")
    if (len(subProjects) == 0):
        output = f"{indentation}<{displayName}/>\n"
    else:
        output = f"{indentation}<{displayName}>\n"
        for subProject in subProjects:
            result = GeneratedProjectHierarchy(subProject.SubProjects, subProject.ProjectName, indent+1)
            output = f"{output}{result}"
        output = f"{output}{indentation}</{displayName}>\n"
    return output

def GenerateDirectedGraphNodes(projects: list, projectName: str, includeLabel: bool, tagName: str, idAttr: str):
    label = ""
    if includeLabel:
        label = f" Label=\"{projectName}\""
    output = f"   <{tagName} {idAttr}=\"{projectName}\"{label}/>\n"
    if (len(projects) > 0):
        for subProject in projects:
            result = GenerateDirectedGraphNodes(subProject.SubProjects, subProject.ProjectName, includeLabel, tagName, idAttr)
            output = f"{output}{result}"
    return output

def GenerateDirectedGraphLinks(subProjects: list, displayName: str, parentDisplayName: str, tagName: str, sourceAttr: str, targetAttr: str):
    if len(parentDisplayName) > 0:
        output = f"   <{tagName} {sourceAttr}=\"{parentDisplayName}\" {targetAttr}=\"{displayName}\"/>\n"
    else:
        output = ""
    if (len(subProjects) > 0):
        for subProject in subProjects:
            result = GenerateDirectedGraphLinks(subProject.SubProjects, subProject.ProjectName, displayName, tagName, sourceAttr, targetAttr)
            output = f"{output}{result}"
    return output

def GenerateDirectedGraph(projects: list, projectName: str):
    nodes = GenerateDirectedGraphNodes(projects, projectName, True, "Node", "Id")
    links = GenerateDirectedGraphLinks(projects, projectName, "", "Link", "Source", "Target")
    output = f"<DirectedGraph xmlns=\"http://schemas.microsoft.com/vs/2009/dgml\">\n"\
      f"<Nodes>\n{nodes}</Nodes>\n"\
      f"<Links>\n{links}</Links>\n"\
      "</DirectedGraph>"
    return output

def GenerateGraphMLNodes(projects: list, projectName: str):
    width = len(projectName) * 6.3
    output = {f"   <node id=\"{projectName}\">\n"\
             f"     <data key=\"d0\">\n"\
             f"       <y:ShapeNode>\n"\
             f"         <y:Geometry height=\"30.0\" width=\"{width}\"/>\n"\
             f"         <y:NodeLabel visible=\"true\" autoSizePolicy=\"content\">{projectName}</y:NodeLabel>\n"\
             f"       </y:ShapeNode>\n"\
             f"     </data>\n"\
             f"   </node>"}
    if (len(projects) > 0):
        for subProject in projects:
            result = GenerateGraphMLNodes(subProject.SubProjects, subProject.ProjectName)
            output.update(output, result)
    return output

def GenerateGraphML(projects: list, projectName: str):
    nodes = "\n".join(list(GenerateGraphMLNodes(projects, projectName)))
    links = GenerateDirectedGraphLinks(projects, projectName, "", "edge", "source", "target")
    output = f"{nodes}\n{links}"
    output = output.replace("<edge", "<edge directed=\"true\"")
    return output

def GenerateIGraphLinks(subProjects: list, displayName: str, parentDisplayName: str):
    if len(parentDisplayName) > 0:
        #newLink = Link(parentDisplayName, displayName)
        output = {(parentDisplayName, displayName)}
    else:
        output = set()
    if (len(subProjects) > 0):
        for subProject in subProjects:
            result = GenerateIGraphLinks(subProject.SubProjects, subProject.ProjectName, displayName)
            output.update(output, result) 
    return output

def GenerateIGraphNodes(projects: list, projectName: str):
    output = {projectName}
    if (len(projects) > 0):
        for subProject in projects:
            result = GenerateIGraphNodes(subProject.SubProjects, subProject.ProjectName)
            output.update(output, result)
    return output
#https://www.youtube.com/watch?v=SpDI6-FvtJY
def GeneratePngOrSvg(projects: list, projectName: str, projectPath:str):
    nodes = list(GenerateIGraphNodes(projects, projectName))
    links = list(GenerateIGraphLinks(projects, projectName, ""))
    g = ig.Graph(directed=True)
    g.add_vertices(nodes)
    g.add_edges(links)
    g.vs["name"] = nodes
    g.vs["label"] = g.vs["name"]
    layout = g.layout_sugiyama()
    visual_style = {}
    visual_style["layout"] = layout
    print(f"{projectPath}\\{projectName}.png")
    if generatePNG:
        #ig.plot(g, f"{projectName}\\{projectName}.png", margin=(120, 20, 120, 20), **visual_style)
        ig.plot(g, f"{projectName}.png", margin=(120, 20, 120, 20), **visual_style)
    if generateSVG:
        #g.write_svg(f"{projectName}\\{projectName}.svg", layout)
        g.write_svg(f"{projectName}.svg", layout)

# find all files recursively under the current folder that ends with *.sln
solutionFilenames = [os.path.join(dp, f) for dp, dn, filenames in os.walk(".") for f in filenames if f.endswith(".sln")]
projectInSolutions = {}
for solutionFilename in solutionFilenames:
    f = open(solutionFilename)
    solutionName = os.path.basename(solutionFilename)
    line = f.readline() # skip first line that contains BOM info
    line = f.readline()
    while line:
        match = re.match(r".*\".*?\\(.*?\.csproj)\"", line, re.IGNORECASE)
        if match:
            projectFilename = match.group(1)
            if projectFilename in projectInSolutions:
                projectInSolutions[projectFilename] = f"{projectInSolutions[projectFilename]}, {solutionName}"
            else:
                projectInSolutions[projectFilename] = f"{solutionName}"
        line = f.readline()
    f.close()

# find all files recursively under the current folder that ends with *.csproj
projectFilenames = [os.path.join(dp, f) for dp, dn, filenames in os.walk(".") for f in filenames if f.endswith(".csproj")]

projectDictionary = {}
solutions = {}
for projectFilename in projectFilenames:
    projectName = os.path.basename(projectFilename)
    if projectName in projectDictionary:
        currentProject = projectDictionary[projectName]
        currentProject.ProjectFilename = projectFilename
    else:
        currentProject = Project(projectFilename, projectName, "")
    if projectName in projectInSolutions:
        solutionName = projectInSolutions[projectName]
    else:
        solutionName = "N/A"
    f = open(projectFilename)
    line = f.readline()
    while line:
        match = re.match(r".*<(?:Package)?Reference Include=\"(.*?)\"?,? Version=\"?(.*?)(?:,|\")", line, re.IGNORECASE)
        if match:
            package = match.group(1)
            version = match.group(2)
            currentProject.Packages.append(f"{package}|{version}")
            if not solutionName in solutions:
                newsolution = Solution(solutionName)
                newsolution.Packages.append(package)
                solutions[solutionName] = newsolution
            else:
                if not package in solutions[solutionName].Packages:
                    solutions[solutionName].Packages.append(package)
            currentProject.PackageDictionary[package] = version
        else:
            match = re.match(r".*<RootNamespace>(.*?)</RootNamespace>", line, re.IGNORECASE)
            if match:
                currentProject.RootNamespace = match.group(1)
            else:
              match = re.match(r".*<(?:TargetFramework|TargetFrameworkVersion)>(.*?)</(?:TargetFramework|TargetFrameworkVersion)>", line, re.IGNORECASE)
              if match:
                  currentProject.TargetFramework = match.group(1)
              else:
                  match = re.match(r".*ProjectReference Include=\"(.*)\\(.*?)\"", line, re.IGNORECASE)
                  if match:
                      subProjectName = match.group(2)
                      if subProjectName in projectDictionary:
                          subProject = projectDictionary[subProjectName]
                      else:
                          subProject = Project(f"{match.group(1)}\\{subProjectName}", subProjectName, os.path.dirname(projectFilename))
                          projectDictionary[subProjectName] = subProject
                      if not subProject in currentProject.SubProjects:
                          currentProject.SubProjects.append(subProject)
        line = f.readline()
    f.close()
    if not currentProject.ProjectName in projectDictionary:
        projectDictionary[projectName] = currentProject

# create a readme file for each project
fileFooter = f"This file was autogenerated by the tool: [https://github.com/CoderAllan/CSharpTools/blob/master/ProjectHierarchy.py](https://github.com/CoderAllan/CSharpTools/blob/master/ProjectHierarchy.py)"
projectsInSolution = {}
solutionReadmeContent = {}
solutionReadmeTOC = {}
projectNumber = 1
for projectName in projectDictionary:
    projectHeader = f"Project {projectName}"
    if projectDictionary[projectName].RootNamespace:
        rootNameSpace = projectDictionary[projectName].RootNamespace
    else:
        rootNameSpace = os.path.splitext(projectName)[0]
    projectBaseInfo = "| | |\n|-|-|\n"\
        f"|Root namespace|{rootNameSpace}|\n"\
        f"|Target framework| {projectDictionary[projectName].TargetFramework}|"
    projectRoot = os.path.dirname(projectDictionary[projectName].ProjectFilename)
    csharpFiles = [os.path.join(dp, f) for dp, dn, filenames in os.walk(projectRoot) for f in filenames if f.endswith(".cs")]
    projectCSFilenumber = f"|Number of C# files|{len(csharpFiles)}|"
    solutionName = ""
    if projectName in projectInSolutions:
        solutionName = projectInSolutions[projectName]
    projectIncludedIn = f"|Project included in|{solutionName}|"
    if solutionName in projectsInSolution:
        projectsInSolution[solutionName].append(projectName)
    else:
        projectsInSolution[solutionName] = [projectName,]
    packagesUsed = "|Package|Version|\n|-|-|"
    packagesInProject = sorted(projectDictionary[projectName].Packages, key = lambda s: s.lower())
    for package in packagesInProject:
        packagesUsed = f"{packagesUsed}\n|{package}|"
    projectStructure = GeneratedProjectHierarchy(projectDictionary[projectName].SubProjects, projectName, 0)
    projectStructure = f"The following structure shows the project hierarchy:\n\n```xml\n{projectStructure}```"
    anchor = projectName.lower().replace(' ', '-')

    newFilename = projectName.replace(".csproj", "")
    # Save the project readme file 
    if generateProjectHierarchy:
        outputFilename = projectDictionary[projectName].ProjectFilename.replace(projectName, f"ReadMe-ProjectStructure-{newFilename}.md")
        print(f"Generating ReadMe for project:  {projectName}, filename: {outputFilename}")
        file = open(outputFilename, "w")
        file.write(
            f"# {projectHeader}\n\n"\
            f"{projectBaseInfo}\n"\
            f"{projectCSFilenumber}\n"\
            f"{projectIncludedIn}\n\n"\
            f"## Packages\n\n"\
            f"{packagesUsed}\n\n"\
            f"## Project hierarchy\n\n"\
            f"{projectStructure}\n\n"\
            f"{fileFooter}"
        )
        file.close()

    # Save the project directed graph 
    if generateDirectedGraph:
        directedGraph = GenerateDirectedGraph(projectDictionary[projectName].SubProjects, projectName)
        outputFilename = projectDictionary[projectName].ProjectFilename.replace(projectName, f"ReadMe-ProjectStructure-{newFilename}.dgml")
        print(f"Generating directed graph (dgml) for project:  {projectName}, filename: {outputFilename}")
        file = open(outputFilename, "w")
        file.write(
            f"<?xml version='1.0' encoding='utf-8'?>\n"\
            f"{directedGraph}\n"
        )
        file.close()
 
    if generateGraphML:
        directedGraph = GenerateGraphML(projectDictionary[projectName].SubProjects, projectName)
        outputFilename = projectDictionary[projectName].ProjectFilename.replace(projectName, f"ReadMe-ProjectStructure-{newFilename}.graphml")
        print(f"Generating directed graph (GraphL) for project:  {projectName}, filename: {outputFilename}")
        file = open(outputFilename, "w")
        file.write(
            f"<?xml version=\"1.0\" encoding=\"UTF-8\"?>\n"\
            f"<graphml xmlns=\"http://graphml.graphdrawing.org/xmlns\"\n"\
            f"         xmlns:xsi=\"http://www.w3.org/2001/XMLSchema-instance\"\n"
            f"         xsi:schemaLocation=\"http://graphml.graphdrawing.org/xmlns http://www.yworks.com/xml/schema/graphml/1.1/ygraphml.xsd\"\n"
            f"         xmlns:y=\"http://www.yworks.com/xml/graphml\">\n"\
            f"    <key for=\"node\" id=\"d0\" yfiles.type=\"nodegraphics\"/>\n"\
            f"  <graph id='G' edgedefault='directed'>\n"
            f"{directedGraph}"\
            f"  </graph>\n"\
            f"</graphml>\n"
        )
        file.close()

    if generatePNG or generateSVG:
        GeneratePngOrSvg(projectDictionary[projectName].SubProjects, projectName, projectDictionary[projectName].ProjectRootPath)
    
    # Create content for solution readme
    # we use the GitHub standard for anchors in the markdown
    projectContent = f"## {projectHeader}<a name=\"{anchor}\"></a>\n\n"\
        f"{projectBaseInfo}\n\n"\
        f"{projectStructure}\n\n"
    if solutionName in solutionReadmeContent:
        solutionReadmeContent[solutionName] = solutionReadmeContent[solutionName] + projectContent
    else:
        solutionReadmeContent[solutionName] = projectContent
    if projectDictionary[projectName].RootNamespace:
        rootNameSpace = projectDictionary[projectName].RootNamespace
    else:
        rootNameSpace = os.path.splitext(projectName)[0]

    tocEntry = f"|[{projectName}](#{anchor})|{rootNameSpace}|{projectDictionary[projectName].TargetFramework}|\n"
    if solutionName in solutionReadmeTOC:
        solutionReadmeTOC[solutionName] = solutionReadmeTOC[solutionName] + tocEntry
    else:
        solutionReadmeTOC[solutionName] = f"|Project|Root namespace|Target framework|\n|-|-|-|\n{tocEntry}"
    projectNumber = projectNumber + 1

# create a readme file for each solution file
if generateSolutionReadme:
    for solutionName in solutionReadmeContent:
        if solutionName != "N/A" and len(solutionName) > 0:
            packagesUsedInSolution = sorted(solutions[solutionName].Packages, key = lambda s: s.lower())
            packageTableSeperator = "|-"
            packageTableHeader = "|Project"
            packageTableBody = ""
            for package in packagesUsedInSolution:
                packageTableHeader = f"{packageTableHeader}|{package}"
                packageTableSeperator = f"{packageTableSeperator}|-"
            for projectName in projectsInSolution[solutionName]:
                packages = projectDictionary[projectName].Packages
                packageTableBody = f"{packageTableBody}|{projectName}"
                for package in packagesUsedInSolution:
                    if package in projectDictionary[projectName].PackageDictionary:
                        packageTableBody = f"{packageTableBody}|{projectDictionary[projectName].PackageDictionary[package]}"
                    else:
                        packageTableBody = f"{packageTableBody}|"
                packageTableBody = f"{packageTableBody}|\n"
            packageTable = f"{packageTableHeader}|\n{packageTableSeperator}|\n{packageTableBody}|\n\n"
            newFilename = solutionName.replace(".sln", "")
            outputFilename = f"ReadMe-SolutionStructure-{newFilename}.md"
            print(f"Generating ReadMe for solution: {solutionName}, filename: {outputFilename}")
            file = open(outputFilename, "w")
            file.write(
                f"# {solutionName}\n\n"\
                f"## Projects\n\n{solutionReadmeTOC[solutionName]}\n"\
                f"## Packages\n\n"\
                f"{packageTable}"\
                f"{solutionReadmeContent[solutionName]}"\
                f"{fileFooter}"
            )
            file.close()
