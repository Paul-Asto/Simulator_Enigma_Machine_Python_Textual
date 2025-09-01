from typing import Generator
from textual.widget import Widget
from textual.widgets import Static, Input

from textual.containers import  Horizontal



class ViewInfo(Widget):
    DEFAULT_CSS = '''
    ViewInfo{
    width: 90;
    height: 5;
    }
    
    ViewInfo  Static.title{
    text-align: center;
    margin-top: 1;
    width: 30;
    height: 1;
    }
    
    ViewInfo Horizontal.content{
    align-vertical: middle;
    border: solid;
    width: 90;
    height: 5;
    }
    '''
    
    def __init__(self, title: str, info: str = "") -> None:
        super().__init__()
        
        self.title = Static(title, classes="title")
        self.data = Input(info, disabled=True)
    
    
    def compose(self) -> Generator[Widget, None, None]:
        with Horizontal(classes="content"):
            yield self.title
            yield self.data
    
    
    def update(self, info: str) -> None:
        self.data.value = info