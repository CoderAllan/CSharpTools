# TestSolution2012.sln

## Projects

|Project|Root namespace|Target framework|
|-|-|-|
|[ClassLibrary2.csproj](#classlibrary2.csproj)|ClassLibrary2.Test|v4.6.2|
|[ClassLibraryX1.csproj](#classlibraryx1.csproj)|ClassLibrary1.Test|v4.7.2|
|[WindowsService1.csproj](#windowsservice1.csproj)|WindowsService1|v4.5|
|[TestSolution2012.csproj](#testsolution2012.csproj)|TestSolution2012|v4.5|

## Packages

|Project|EntityFramework|EntityFramework.SqlServer|itextsharp|RestSharp|
|-|-|-|-|-|
|ClassLibrary2.csproj|6.0.0.0|6.0.0.0||106.6.9.0|
|ClassLibraryX1.csproj|||||
|WindowsService1.csproj|||5.5.13.0||
|TestSolution2012.csproj|||5.5.13.0||
|

## Project ClassLibrary2.csproj<a name="classlibrary2.csproj"></a>

| | |
|-|-|
|Root namespace|ClassLibrary2.Test|
|Target framework| v4.6.2|

The following structure shows the project hierarchy:

```xml
<ClassLibrary2/>
```

## Project ClassLibraryX1.csproj<a name="classlibraryx1.csproj"></a>

| | |
|-|-|
|Root namespace|ClassLibrary1.Test|
|Target framework| v4.7.2|

The following structure shows the project hierarchy:

```xml
<ClassLibraryX1/>
```

## Project WindowsService1.csproj<a name="windowsservice1.csproj"></a>

| | |
|-|-|
|Root namespace|WindowsService1|
|Target framework| v4.5|

The following structure shows the project hierarchy:

```xml
<WindowsService1>
   <ClassLibraryX1/>
</WindowsService1>
```

## Project TestSolution2012.csproj<a name="testsolution2012.csproj"></a>

| | |
|-|-|
|Root namespace|TestSolution2012|
|Target framework| v4.5|

The following structure shows the project hierarchy:

```xml
<TestSolution2012>
   <WindowsService1>
      <ClassLibraryX1/>
   </WindowsService1>
</TestSolution2012>
```

This file was autogenerated by the tool: [https://github.com/CoderAllan/CSharpTools/blob/master/ProjectHierarchy.py](https://github.com/CoderAllan/CSharpTools/blob/master/ProjectHierarchy.py)