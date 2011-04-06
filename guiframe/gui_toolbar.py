
import wx
import os
from wx import ToolBar as Tbar
from wx.lib.platebtn import PlateButton
from sans.guiframe.gui_style import GUIFRAME_ID
from sans.guiframe.gui_style import GUIFRAME_ICON
from wx.lib.platebtn import PB_STYLE_SQUARE, PB_STYLE_DROPARROW
#Control panel width 
import sys
if sys.platform.count("darwin")==0:
    FONT_VARIANT = 0
else:
    FONT_VARIANT = 1
    

def clear_image(image):
    w, h = image.GetSize()
    factor = 155
    compress = lambda x: int(x * factor/255.) + factor
    for y in range(h):
        for x in range(w):
            grey = compress(image.GetGreen(x, y))
            image.SetRGB(x, y, grey, grey, grey)
    if image.HasAlpha():
        image.ConvertAlphaToMask()
    return image

class GUIToolBar(Tbar):
    """
    Implement toolbar for guiframe
    """
    def __init__(self, parent,  *args, **kwds):
        Tbar.__init__(self, parent,  *args, **kwds)
        #Set window's font size 
        self.SetWindowVariant(variant=FONT_VARIANT)
        self.parent = parent
        self._bookmark_menu = None
        self._bookmark_bt = None
        self.do_layout()
        self.on_bind_button()
       
    def do_layout(self):
        """
        """
        tbar_size = (20, 15)
        button_type =  wx.ITEM_NORMAL

        self.AddSeparator()
        reset_im = GUIFRAME_ICON.RESET_ICON
        reset_im.Rescale(tbar_size[0], tbar_size[1], wx.IMAGE_QUALITY_HIGH)
        reset_bmp = reset_im.ConvertToBitmap()
        #disable_reset_bmp = clear_image(reset_im).ConvertToBitmap()
        disable_reset_bmp = wx.NullBitmap
        self.AddLabelTool(GUIFRAME_ID.RESET_ID, 'Reset', reset_bmp,
                   disable_reset_bmp, button_type,'Reset')
        self.AddSeparator()
        drag_im = GUIFRAME_ICON.DRAG_ICON
        drag_im.Rescale(tbar_size[0], tbar_size[1], wx.IMAGE_QUALITY_HIGH)
        drag_bmp = drag_im.ConvertToBitmap()
        self.AddSeparator()
        report_im = GUIFRAME_ICON.REPORT_ICON
        report_im.Rescale(tbar_size[0], tbar_size[1], wx.IMAGE_QUALITY_HIGH)
        report_bmp = report_im.ConvertToBitmap()
        #disable_report_bmp = clear_image(report_im).ConvertToBitmap()
        disable_report_bmp = wx.NullBitmap
        self.AddLabelTool(GUIFRAME_ID.PREVIEW_ID, 'Report', report_bmp,
                   disable_report_bmp, button_type,'Report')
        self.AddSeparator()
        print_im = GUIFRAME_ICON.PRINT_ICON
        print_im.Rescale(tbar_size[0], tbar_size[1], wx.IMAGE_QUALITY_HIGH)
        print_bmp = print_im.ConvertToBitmap()
        #disable_print_bmp = clear_image(print_im).ConvertToBitmap()
        disable_print_bmp = wx.NullBitmap
        self.AddLabelTool(GUIFRAME_ID.PRINT_ID, 'Print', print_bmp,
                          disable_print_bmp, button_type, 'Print')
        self.AddSeparator()
        undo_im = GUIFRAME_ICON.UNDO_ICON
        undo_im.Rescale(tbar_size[0], tbar_size[1], wx.IMAGE_QUALITY_HIGH)
        undo_bmp = undo_im.ConvertToBitmap()
        #disable_undo_bmp = clear_image(undo_im).ConvertToBitmap()
        disable_undo_bmp = wx.NullBitmap
        self.AddLabelTool(GUIFRAME_ID.UNDO_ID, 'Undo', undo_bmp,
                          disable_undo_bmp, button_type,'Undo')
        self.AddSeparator()
        redo_im = GUIFRAME_ICON.REDO_ICON
        redo_im.Rescale(tbar_size[0], tbar_size[1], wx.IMAGE_QUALITY_HIGH)
        redo_bmp = redo_im.ConvertToBitmap()
        #disable_redo_bmp = clear_image(redo_im).ConvertToBitmap()
        disable_redo_bmp = wx.NullBitmap
        self.AddLabelTool(GUIFRAME_ID.REDO_ID, 'Redo', redo_bmp,
                          disable_redo_bmp, button_type,'Redo')
        self.AddSeparator()
        #add button for the current application
        self.button_application = wx.StaticText(self, -1, 'Welcome')
        self.button_application.SetForegroundColour('black')
        self.button_application.SetBackgroundColour('#1874CD')
        hint = 'Active Application'
        self.button_application.SetToolTipString(hint)
        self.AddControl(self.button_application)
        self.AddSeparator()
         #add button for the panel on focus
        self.button_panel = wx.StaticText(self, -1, 'No Panel')
        self.button_panel.SetForegroundColour('black')
        self.button_panel.SetBackgroundColour('#90EE90')
        hint = 'Panel on Focus'
        self.button_panel.SetToolTipString(hint)
        self.AddControl(self.button_panel)
        self._bookmark_bt = PlateButton(self, -1, 'bookmark', 
                         GUIFRAME_ICON.BOOKMARK_ICON.ConvertToBitmap(), 
                         style=PB_STYLE_SQUARE|PB_STYLE_DROPARROW)
        self._bookmark_bt.Disable()
        self._bookmark_menu = wx.Menu()
        id = wx.NewId()
        self._bookmark_menu.Append(id, 'Add bookmark')
        self._bookmark_menu.AppendSeparator()
        wx.EVT_MENU(self, id, self.on_bookmark)
        
        self._bookmark_bt.SetMenu(self._bookmark_menu)
        self.AddControl(self._bookmark_bt)
       
        self.SetToolBitmapSize(tbar_size)
        self.Realize()
        
    def on_bind_button(self):
        """
        """
        if self.parent is not None:
            
            self.parent.Bind(wx.EVT_TOOL, self.parent.on_redo_panel,
                             id=GUIFRAME_ID.REDO_ID)
            self.parent.Bind(wx.EVT_TOOL, self.parent.on_undo_panel,
                             id=GUIFRAME_ID.UNDO_ID)
            self.parent.Bind(wx.EVT_TOOL, self.parent.on_reset_panel,
                             id=GUIFRAME_ID.RESET_ID)
            self.parent.Bind(wx.EVT_TOOL, self.parent.on_preview_panel,
                             id=GUIFRAME_ID.PREVIEW_ID)
            self.parent.Bind(wx.EVT_TOOL, self.parent.on_print_panel,
                             id=GUIFRAME_ID.PRINT_ID)
            
    def update_button(self, application_name='', panel_name=''):
        """
        """
        self.button_application.SetLabel(str(application_name))
        self.button_panel.SetLabel(str(panel_name))
        
    def update_toolbar(self, panel=None):
        """
        """
        if panel is None:
            self.EnableTool(GUIFRAME_ID.PRINT_ID, False)
            self.EnableTool(GUIFRAME_ID.UNDO_ID,False)
            self.EnableTool(GUIFRAME_ID.REDO_ID, False)
            self.EnableTool(GUIFRAME_ID.PREVIEW_ID, False)
            self.EnableTool(GUIFRAME_ID.RESET_ID, False)
            self._bookmark_bt.Disable()
            
        else:
            self.EnableTool(GUIFRAME_ID.PRINT_ID, panel.get_print_flag())
            self.EnableTool(GUIFRAME_ID.UNDO_ID, panel.get_undo_flag())
            self.EnableTool(GUIFRAME_ID.REDO_ID, panel.get_redo_flag())
            self.EnableTool(GUIFRAME_ID.PREVIEW_ID, panel.get_preview_flag())
            self.EnableTool(GUIFRAME_ID.RESET_ID, panel.get_reset_flag())
            self._bookmark_bt.Enable(panel.get_bookmark_flag())
        self.Realize()
        
    def enable_undo(self, panel):
        self.EnableTool(GUIFRAME_ID.UNDO_ID, panel.get_undo_flag())
        self.Realize()
        
    def enable_redo(self, panel):
        self.EnableTool(GUIFRAME_ID.REDO_ID, panel.get_redo_flag())
        self.Realize()
        
    def enable_print(self, panel):
        self.EnableTool(GUIFRAME_ID.PRINT_ID, panel.get_print_flag())
        self.Realize()
    
    def enable_zoom(self, panel):
        self.EnableTool(GUIFRAME_ID.ZOOM_ID, panel.get_zoom_flag())
        self.Realize()
        
    def enable_zoom_in(self, panel):
        self.EnableTool(GUIFRAME_ID.ZOOM_IN_ID, panel.get_zoom_in_flag())
        self.Realize()
        
    def enable_zoom_out(self, panel):
        self.EnableTool(GUIFRAME_ID.ZOOM_OUT_ID, panel.get_zoom_out_flag())
        self.Realize()
        
    def enable_bookmark(self, panel):
        flag =  panel.get_bookmark_flag()
        self._bookmark_bt.Enable(flag)
        self.Realize()
        
    def enable_save(self, panel):
        self.EnableTool(GUIFRAME_ID.SAVE_ID, panel.get_save_flag())
        self.Realize()
        
    def enable_reset(self, panel):
        self.EnableTool(GUIFRAME_ID.RESET_ID, panel.get_reset_flag())
        self.Realize()
    
    def enable_preview(self, panel):
        self.EnableTool(GUIFRAME_ID.PREVIEW_ID, panel.get_preview_flag())
        self.Realize()
    
    def on_bookmark(self, event):
        """
        add book mark
        """
        if self.parent is not None:
           self.parent.on_bookmark_panel(event)
           
    def append_bookmark(self, event):
        """
        receive item to append on the toolbar button bookmark
        """
        title = event.title
        hint = event.hint
        handler = event.handler
        id = wx.NewId()
        self._bookmark_menu.Append(id, str(title), str(hint))
        wx.EVT_MENU(self, id, handler)
       
