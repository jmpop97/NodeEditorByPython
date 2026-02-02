import tkinter as tk
from NodeView.CenterFrame import NodeView # Add this import at the top of the file
from NodeListView.NodeListView import NodeListView
from NodeDetailView.NodeDetailView import NodeDetailView
class NodeEditor(tk.Tk):
    def __init__(self):
        super().__init__()
        self.title("Node Editor")
        self.geometry("1200x600")

        # Use PanedWindow to allow resizing between frames
        self.paned_window = tk.PanedWindow(self, orient=tk.HORIZONTAL)
        self.paned_window.pack(fill=tk.BOTH, expand=True)

        # Add frames to the PanedWindow
        nodeListView = NodeListView(self.paned_window, self)  # Pass self as parent
        nodeView = NodeView(self.paned_window, self)  # Pass self as parent
        nodeDetailView = NodeDetailView(self.paned_window, self)  # Pass self as parent

        self.nodeListView = nodeListView
        self.nodeView = nodeView
        self.nodeDetailView = nodeDetailView
        
        setattr(nodeView, 'nodeListView', nodeListView)
        setattr(nodeView, 'nodeDetailView', nodeDetailView)

        setattr(nodeListView, 'nodeView', nodeView)
        setattr(nodeListView, 'nodeDetailView', nodeDetailView)

        setattr(nodeDetailView, 'nodeView', nodeView)
        setattr(nodeDetailView, 'nodeListView', nodeListView)


        self.paned_window.add(nodeListView, stretch="always")
        self.paned_window.add(nodeView, stretch="always")
        self.paned_window.add(nodeDetailView, stretch="always")






if __name__ == "__main__":    
    app = NodeEditor()    
    app.mainloop()