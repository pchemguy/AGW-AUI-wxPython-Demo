This project attempts to freshen and reorganize the [AGW-AUI][] wxPython demo module as a wxPython learning exercise. My other goal is the preparation of a structured GUI app skeleton.

To me, the extensive official wxPython demo collection is a strong attraction point. This collection demonstrates a great variety of wxPython GUI widgets, but it also includes several complex demos, such as the two similar AUI modules *AUI_DockingWindowMgr.py* and *agw/AUI.py*. Almost all of the code of these demos is monolithic and placed in single Python modules. While the demo code does illustrate how individual features can be implemented, it is difficult to reuse the whole demo or a large part of it because it lacks structure and modularity. Therefore, I attempted to restructure the code into loosely coupled components. With minor exceptions, I reproduce almost all features/functionality of the "agw/AUI.py" module. I removed several minor dependencies on other demo modules to enable independent execution of the restructured code. I have not made any attempt to preserve compatibility with Python 2. In fact, this project uses recent features where beneficial, so Python 3.10 is required, and I also use the latest wxPython 4.2.0. The present version is a relatively early attempt, and it lacks documentation. I plan to keep working on both of these aspects and improve them. For now, I am interested to see if there might be an interest in such a project and would appreciate feedback on the project structure.



<!-- References -->
[AGW-AUI]: https://github.com/wxWidgets/Phoenix/blob/master/demo/agw/AUI.py
