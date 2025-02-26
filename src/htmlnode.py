class HTMLNode:

    def __init__(self, tag=None, value=None, children=None, props=None) -> None:
        self.tag = tag
        self.value = value
        self.children = children
        self.props = props

    def __repr__(self) -> str:
        tag = f"{self.tag}"
        value = f"{self.tag}"
        children = f"{self.children}"
        props = self.propsToHTML()
        return f"tag:{tag}\nvalue:{value}\nchildren:{children}\nprops:{props}"

    def toHTML(self):
        raise NotImplementedError

    def propsToHTML(self):
        if self.props == None:
            return ""
        propString = ""
        for prop in self.props:
            propString += f' {prop}="{self.props[prop]}"'
        return propString
