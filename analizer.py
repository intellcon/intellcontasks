dom = xml.dom.minidom.parse(src)
        dom.normalize()
        tasks = dom.getElementsByTagName("Task")
        for task in tasks:
            childTags = task.childNodes
            for child in childTags:
                if child.nodeType == child.TEXT_NODE:
                    print(child.nodeValue)
                else:
                    print(child.nodeName)
                    print(child.childNodes[0].nodeValue)